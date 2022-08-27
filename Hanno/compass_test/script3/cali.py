#!/usr/bin/python

from math import sqrt

import RPi.GPIO as GPIO
import smbus
import time
import csv
import sys

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

address = 0x1e

def avg(lst):
    """Return average of list"""
    try:
        return sum(lst) / len(lst)
    except ZeroDivisionError:
        return 0
 
def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)

def findCircle(lst):
    x1, y1 = lst[0]
    x2, y2 = lst[1]
    x3, y3 = lst[2]

    x12 = x1 - x2
    x13 = x1 - x3
    y12 = y1 - y2
    y13 = y1 - y3
    y31 = y3 - y1
    y21 = y2 - y1
    x31 = x3 - x1
    x21 = x2 - x1

    # x1^2 - x3^2
    sx13 = pow(x1, 2) - pow(x3, 2)
    # y1^2 - y3^2
    sy13 = pow(y1, 2) - pow(y3, 2)
    sx21 = pow(x2, 2) - pow(x1, 2)
    sy21 = pow(y2, 2) - pow(y1, 2)

    f = (((sx13) * (x12) + (sy13) *
          (x12) + (sx21) * (x13) +
          (sy21) * (x13)) // (2 *
          ((y31) * (x12) - (y21) * (x13))))

    g = (((sx13) * (y12) + (sy13) * (y12) +
          (sx21) * (y13) + (sy21) * (y13)) //
          (2 * ((x31) * (y12) - (x21) * (y13))))

    c = (-pow(x1, 2) - pow(y1, 2) -
         2 * g * x1 - 2 * f * y1)

    # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
    # where centre is (h = -g, k = -f) and
    # radius r as r^2 = h^2 + k^2 - c
    h = -g
    k = -f
    sqr_of_r = h * h + k * k - c

    # r is the radius *optional return value currently not needed
    r = sqrt(sqr_of_r)
    return (h, k)

def write_file(fields, data):
    """Write data to CSV"""
    fileName = time.ctime().replace(" ", "_").replace(":", ".")
    with open(fileName + ".csv", "w") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

def duplicate_check(lst):
    """Check for duplicates and return unique"""
    seen = set()
    uniq = []
    for item in lst:
        if item not in seen:
            uniq.append(item)
            seen.add(item)
    return uniq


def main():
    write_byte(0, 0b00110000) # Set to 8 samples @ 15Hz
    write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
    write_byte(2, 0b00000000) # Continuous sampling
    
    data = []
    fields = [
        "x_out",
        "y_out",
        "x_mid",
        "y_mid",
        "x_mid_avg",
        "y_mid_avg",
        "x_calied",
        "y_calied"
    ]

    sampleScale = 10
    Offset = []
    xOffset = []
    yOffset = []
    xMid = 0
    yMid = 0

    for i in range(0,500):
        raw_x_out = read_word_2c(3)
        raw_y_out = read_word_2c(7)
        z_out = read_word_2c(5)

        x_calculated = raw_x_out - avg(xOffset)
        y_calculated = raw_y_out - avg(yOffset)

        sys.stdout.write(f"\rX_OUT: {raw_x_out}, Y_OUT: {raw_y_out}, X_MID: {xMid}, Y_MID: {yMid}")
        
        if i%(sampleScale * 3) == 0:
            Offset = []

        if i%sampleScale == 0:
            Offset.append((raw_x_out, raw_y_out))
            if len(duplicate_check(Offset)) == 3:
                try:
                    xMid, yMid = findCircle(Offset)
                    xOffset.append(xMid)
                    yOffset.append(yMid)
                except ZeroDivisionError:
                    pass
 
        payload = {
            "x_out": raw_x_out,
            "y_out": raw_y_out,
            "x_mid": xMid,
            "y_mid": yMid,
            "x_mid_avg": avg(xOffset),
            "y_mid_avg": avg(yOffset),
            "x_calied": x_calculated,
            "y_calied": y_calculated
        }

        time.sleep(0.1)
        data.append(payload)
    write_file(fields, data)


if __name__ == '__main__':
    main()
