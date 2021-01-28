# -*- coding: utf-8 -*-
import socket
import network
import json
import time
from machine import Timer
from machine import I2C, Pin
from mp_i2c_lcd1602 import LCD1602
from ds18x20 import DS18X20
from onewire import OneWire



# ИНИЦИАЛИЗАЦИЯ ПИНОВ
#   датчики температуры
sensor_DS18X20 = Pin(25, Pin.IN, Pin.PULL_UP)  # первый датчик


# инициализация экрана
i2c = I2C(1, sda=Pin(21), scl=Pin(22))
lcd = LCD1602(i2c)

# инициализация DS18B20 на пине №
ow = OneWire(sensor_DS18X20)
temp = DS18X20(ow)
roms = temp.scan()
temp.convert_temp()


while True:
    time.sleep(1)
    temp.convert_temp()
    lcd.puts(int(temp.read_temp(roms[0])), 0, 0)
    lcd.puts(int(temp.read_temp(roms[1])), 0, 1)




