import os
import time
import RPi.GPIO as GPIO
import time
from threading import Thread
import hot_water_pump
from LCD_libV2 import writetemp
from RPLCD.i2c import CharLCD


lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
                  cols=16, rows=2,
                  charmap='A02',
                  backlight_enabled=True)

out = 0
GPIO.setmode(GPIO.BOARD)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = '/sys/bus/w1/devices/28-03149779237c/w1_slave'
temp_sensor1 = '/sys/bus/w1/devices/28-0314977912af/w1_slave'
GPIO.setup(37,GPIO.OUT)#red1
GPIO.setup(11,GPIO.OUT)#blue1
GPIO.setup(40,GPIO.OUT)#red 2
GPIO.setup(38,GPIO.OUT)#blue 2
GPIO.setup(18,GPIO.OUT)#motor pin
GPIO.setup(16,GPIO.OUT)

GPIO.output(37,GPIO.LOW)#red1
GPIO.output(11,GPIO.LOW)#blue1
GPIO.output(40,GPIO.LOW)#red 2
GPIO.output(38,GPIO.LOW)#blue 2
GPIO.output(18,GPIO.LOW)#motor pin
GPIO.output(16,GPIO.LOW)

def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines
def temp_raw1():
    f = open(temp_sensor1, 'r')
    lines = f.readlines()
    f.close()
    return lines
def read_temp():#cancer senor

    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        lines = temp_raw()
    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
def read_temp1():#healthy sensor

    lines = temp_raw1()
    while lines[0].strip()[-3:] != 'YES':
        lines = temp_raw1()
    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def main():
    inittemp1 = read_temp()
    inittemp2 = read_temp1()
    while True:
        inittemp1 = read_temp1()
        inittemp2 = read_temp()
        while True:
            temp1 = read_temp()
            temp2 = read_temp1()
            #print("sensor1",temp1,";","sensor2",temp2,"initial temp = ", inittemp1)
            print("sensor2",temp2,"initial temp = ", inittemp1)
            #writetemp(round(temp1),round(temp2),lcd)
            writetemp(round(temp1),26,lcd)
            if round(temp1) >= 30:
                time.sleep(5)
                #GPIO.output(37,GPIO.HIGH)
                GPIO.output(11,GPIO.HIGH)
                #GPIO.output(11,GPIO.LOW)
                GPIO.output(38,GPIO.HIGH)
                GPIO.output(18,GPIO.LOW)
                GPIO.output(40,GPIO.LOW)
                time.sleep(6)
                GPIO.output(40,GPIO.HIGH)
                GPIO.output(38,GPIO.LOW)
                GPIO.output(18,GPIO.HIGH)
                time.sleep(15)
                GPIO.output(18,GPIO.LOW)
                GPIO.output(40,GPIO.LOW)
                GPIO.output(37,GPIO.LOW)
                break
                
                
            elif temp2-inittemp1 < 3:
                GPIO.output(11,GPIO.HIGH)
                GPIO.output(37,GPIO.LOW)
                GPIO.output(38,GPIO.HIGH)
                GPIO.output(18,GPIO.LOW)



if __name__ == "__main__": 
    # creating processes 
    p1 = Thread(target=hot_water_pump.bt_control).start()
    p2 = Thread(target=main).start()

      










        
