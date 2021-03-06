#!/user/bin/python
'''
    buzzer.py
    ~~~~~~~~~~~~~~~~
    buzzer warning  module.
    :copyright: (c) 2017 by jxg.
'''

import RPi.GPIO as GPIO
import time

def buzz(buzztime):
    #buzztime = 5
    GPIO_PIN = 23;
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN,GPIO.OUT);
    GPIO.output(GPIO_PIN,GPIO.LOW);
    time.sleep(buzztime);               #只有震动才会发声，所以需要暂停
    GPIO.output(GPIO_PIN,GPIO.HIGH);
    GPIO.cleanup();

