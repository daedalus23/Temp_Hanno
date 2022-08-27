#!/usr/bin/python

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



if __name__ == '__main__':
    write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
    write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
    write_byte(2, 0b00000000) # Continuous sampling

    scale = 0.92
    
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0

    xOffset = 0
    yOffset = 0

    AvgXoffset = []
    AvgYoffset = []

    fileName = time.ctime().replace(" ", "_").replace(":", ".")
    data = []
    fields = [
        "x_out",
        "y_out",
        "minx",
        "maxx",
        "miny",
        "maxy",
        "x offset",
        "y offset"
    ]

    for i in range(0,500):
        x_out = read_word_2c(3)
        y_out = read_word_2c(7)
        z_out = read_word_2c(5)
 
        payload = {
            "x_out": x_out,
            "y_out": y_out,
            "minx": minx,
            "maxx": maxx,
            "miny": miny,
            "maxy": maxy,
            "x offset": (maxx + minx) / 2,
            "y offset": (maxy + miny) / 2
        }

        sys.stdout.write(f"\rX_OUT: {x_out}, Y_OUT: {y_out}")

        if x_out < minx:
            minx=x_out
        if y_out < miny:
            miny=y_out
        if x_out > maxx:
            maxx=x_out
        if y_out > maxy:
            maxy=y_out

        time.sleep(0.1)
        data.append(payload)

        xOffset = (maxx + minx) / 2
        yOffset = (maxy + miny) / 2

    print()
    print("minx: ", minx)
    print("miny: ", miny)
    print("maxx: ", maxx)
    print("maxy: ", maxy)
    print("x offset: ", (maxx + minx) / 2)
    print("y offset: ", (maxy + miny) / 2)


    with open(fileName + ".csv", "w") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

