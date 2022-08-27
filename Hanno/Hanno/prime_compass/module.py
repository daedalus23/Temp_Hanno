#!/usr/bin/python

import RPi.GPIO as GPIO
import smbus


"""
Module controls Raspberry Pi I2C device, intended to read & write byte
data. Designed for 8 byte messages read from device with hex registers
and addresses. 
"""


class Module:


    high_result = None
    low_result = None
    byte_result = None

    def __init__(self, configCache):
        self.register = int(
            configCache.content["smbus"]["register"],
            int(configCache.content["smbus"]["base_convert"])
        )
        self.bus = self.rev_bus_check()

    def read_byte(self, address):
        """Read exact byte data from module address|register"""
        return self.bus.read_byte_data(self.register, address)

    def read_word(self, address):
        """Read high & low byte data from module address|register"""
        self.high_result = self.bus.read_byte_data(self.register, address)
        self.low_result = self.bus.read_byte_data(self.register, address+1)
        self.byte_result = (self.high_result << 8) + self.low_result

    def read_word_2c(self, address):
        """Process module byte data"""
        self.read_word(address)
        if self.byte_result >= 0x8000:
            return -((65535 - self.byte_result) + 1)

    @staticmethod
    def rev_bus_check():
        """Check GPIO revision & assign correct smbus"""
        rev = GPIO.RPI_REVISION
        if rev == 2 or rev == 3:
            return smbus.SMBus(1)
        else:
            return smbus.SMBus(0)

    def write_byte(self, address, value):
        """Write byte data to module"""
        self.bus.write_byte_data(self.register, address, value)
