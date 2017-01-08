#!/usr/bin/python3

# see the datasheet: https://cdn-shop.adafruit.com/datasheets/TCS34725.pdf
# http://bradsrpi.blogspot.de/2013/05/tcs34725-rgb-color-sensor-raspberry-pi.html
# https://github.com/adafruit/Adafruit_Python_TCS34725/blob/master/Adafruit_TCS34725/TCS34725.py

import smbus
import time

TCS34725_ADDRESS          = 0x29
TCS34725_ID               = 0x12 # 0x44 = TCS34721/TCS34725, 0x4D = TCS34723/TCS34727

# Register addresses must be OR'ed with 0x80
TCS34725_COMMAND_BIT      = 0x80

TCS34725_ENABLE           = 0x00
TCS34725_ENABLE_AIEN      = 0x10 # RGBC Interrupt Enable
TCS34725_ENABLE_WEN       = 0x08 # Wait enable - Writing 1 activates the wait timer
TCS34725_ENABLE_AEN       = 0x02 # RGBC Enable - Writing 1 actives the ADC, 0 disables it
TCS34725_ENABLE_PON       = 0x01 # Power on - Writing 1 activates the internal oscillator, 0 disables it
TCS34725_ATIME            = 0x01 # Integration time
TCS34725_CDATAL           = 0x14 # Clear channel data

bus = smbus.SMBus(3)

# i2c helpers

def read_reg(reg):
    bus.write_byte(TCS34725_ADDRESS, TCS34725_COMMAND_BIT|reg)
    return bus.read_byte(TCS34725_ADDRESS)

def write_reg(reg, val):
    bus.write_byte(TCS34725_ADDRESS, TCS34725_COMMAND_BIT|reg)
    bus.write_byte(TCS34725_ADDRESS, val)

# lib api

def get_chip_id():
    return read_reg(TCS34725_ID)

def get_atime():
    return read_reg(TCS34725_ATIME)

def set_atime(val):
    write_reg(TCS34725_ATIME, val)

def enable_processing():
    write_reg(TCS34725_ENABLE, TCS34725_ENABLE_PON|TCS34725_ENABLE_AEN)
    time.sleep(0.25) # avoid that we get a (0,0,0,0) reading

def main():
    chip_id = get_chip_id()
    # version # should be 0x44
    if chip_id == 0x44:
      print("Device found")
      print("default ATIME: 0x%02x" % get_atime())
      set_atime(0xC0)

      enable_processing()

      last_hexcolor=""
      # start reading from reg 14 (cdata), first LSB, then MSB
      bus.write_byte(TCS34725_ADDRESS, TCS34725_COMMAND_BIT|TCS34725_CDATAL)
      while True:
        data = bus.read_i2c_block_data(TCS34725_ADDRESS, 0)
        # Max values depend on ATIME (integration time, def=0x00)
        # C: 'clear': 16bit value from unfiltered photo diodes: brightness
        # R,G,B     : 16bit color intensity
        clear = clear = data[1] << 8 | data[0]
        red = data[3] << 8 | data[2]
        green = data[5] << 8 | data[4]
        blue = data[7] << 8 | data[6]
        hexcolor = "#%02x%02x%02x" % (red>>8, green>>8, blue>>8)
        if last_hexcolor != hexcolor:
            print("%s: C: %s, R: %s, G: %s, B: %s" % (hexcolor, clear, red, green, blue))
            last_hexcolor = hexcolor
        time.sleep(0.5)  # for ATIME=0xC0, we need to wait at least 154 ms
    else:
      print("Device not found, chip_id=0x%02x" % chip_id)

if __name__ == "__main__":
    main()
