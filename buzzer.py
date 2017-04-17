#!/user/bin/python

import RPi.GPIO as GPIO
import time

def buzz():
	buzztime = 5
	GPIO_PIN = 23;
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(GPIO_PIN,GPIO.OUT);
	GPIO.output(GPIO_PIN,GPIO.LOW);
	time.sleep(buzztime);
	GPIO.output(GPIO_PIN,GPIO.HIGH);

	GPIO.cleanup();

