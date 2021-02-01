# -*- coding: utf-8 -*-
import socket
import machine
import network
import json
import time
from machine import Timer
from machine import I2C, Pin, PWM
from mp_i2c_lcd1602 import LCD1602
from ds18x20 import DS18X20
from onewire import OneWire


temper_in = 0
temper_out = 0

servo_open = True
servo_close = True


# ИНИЦИАЛИЗАЦИЯ ПИНОВ
sensor_DS18X20 = Pin(25, Pin.IN, Pin.PULL_UP)  # датчики температуры
pin_servo = Pin(17, Pin.OUT)  # управление засчлонкой
enable_servo = Pin(5, Pin.OUT)  # включение питания заслонки

# инициализация прина управления сервоприводом
servo = machine.PWM(pin_servo, freq=50)

# инициализация экрана
i2c = I2C(1, sda=Pin(21), scl=Pin(22))
lcd = LCD1602(i2c)

# инициализация DS18B20 на пине №
ow = OneWire(sensor_DS18X20)
temp = DS18X20(ow)
roms = temp.scan()
temp.convert_temp()


# Управление сервоприводом 1-откр 0-закр
def servo_state(state=0):
    global servo_open, servo_close
    if state == 1 and servo_open:
        enable_servo.off()
        servo.duty(40)
        time.sleep(0.5)
        enable_servo.on()
        servo_open = False
        servo_close = True

    if state == 0 and servo_close:
        enable_servo.off()
        servo.duty(90)
        time.sleep(0.5)
        enable_servo.on()
        servo_open = True
        servo_close = False


servo_state(1)
lcd.puts('open ', 0, 3)

while True:
    temp.convert_temp()
    temper_in = int(temp.read_temp(roms[0]))
    temper_out = int(temp.read_temp(roms[1]))
    lcd.puts(temper_in, 0, 0)
    lcd.puts(temper_out, 0, 1)
    if temper_out > 35:
        servo_state(0)
        lcd.puts('close ', 0, 3)
    elif temper_out < 33:
        servo_state(1)
        lcd.puts('open ', 0, 3)










