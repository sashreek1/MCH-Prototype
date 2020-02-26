from bluedot import BlueDot
import RPi.GPIO as GPIO

def bt_control():
    state = 0
    bd = BlueDot()
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(31,GPIO.OUT)
    GPIO.setup(29,GPIO.OUT)

    GPIO.output(31,GPIO.LOW)   
    GPIO.output(29,GPIO.LOW)

    while True:
        bd.wait_for_press()
        if state == 0:
            state = 1
        else:
            state = 0


        if state == 1:
            GPIO.output(31,GPIO.HIGH)   
            GPIO.output(29,GPIO.LOW)
            print("on")
        if state == 0:
            GPIO.output(31,GPIO.LOW)   
            GPIO.output(29,GPIO.LOW)
            print("off")
