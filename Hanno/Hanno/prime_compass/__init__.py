from module import Module

from Hanno.configreader import Configuration
from math import sqrt

import time
import csv
import sys


configPath = r"Hanno/bin/compass_config.ini"
configCache = Configuration(configPath)


device = Module(configCache)

device.write_byte(0, 0b00110000)  # Set to 8 samples @ 15Hz
device.write_byte(1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
device.write_byte(2, 0b00000000)

for i in range(0, 500):
    x_out = device.read_word_2c(3)
    y_out = device.read_word_2c(7)
    z_out = device.read_word_2c(5)

    sys.stdout.write(f"\rx_out: {x_out}, y_out: {y_out}, z_out: {z_out}")

    time.sleep(0.1)
