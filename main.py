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
from machine import WDT


temper_in = 0
temper_out = 0
old_temper_in = 0
old_temper_out = 0

time_work_device = 0

servo_open = True
servo_close = True

timer = machine.Timer(0)

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


def handleInterrupt(timer):
    global old_temper_in, old_temper_out, temper_in, temper_out, time_work_device
    temp.convert_temp()
    temper_in = int(temp.read_temp(roms[0]))
    temper_out = int(temp.read_temp(roms[1]))
    if old_temper_out != temper_out:
        old_temper_out = temper_out
        lcd.puts(temper_out, 0, 1)
    if old_temper_in != temper_in:
        old_temper_in = temper_in
        lcd.puts(temper_in, 0, 0)
    time_work_device = time_work_device+1
    lcd.puts('time: '+ str(time_work_device), 10, 0)





timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=handleInterrupt)
