import time
import smtplib
import RPi.GPIO as GPIO
import csv
import socket
import sys
from threading import Thread

passes = 0
revs = 0

def sensor(channel):
    global passes
    passes = passes + 1

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

channel = 37
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(channel, GPIO.FALLING,callback=sensor,bouncetime=1)

while 1:
    if(passes >= 6):
        revs = revs + 1
        passes = passes - 6
        print "revs:   ", str(revs)
        print "passes: ", str(passes)
