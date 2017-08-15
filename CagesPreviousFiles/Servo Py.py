import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(15, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

GPIO.output(19,GPIO.LOW)

freq = 50
pwm = GPIO.PWM(11, freq)

left = 0.75
right = 2.5
mid = (right - left) / 2 + left

position = [left, mid, right, mid]

mspc = 1000/ freq

for i in range(3):
    for pos in position:
        dutypercent= pos* 100/ mspc
        print "Position" + str(pos)
        print "Duty Cycle: " + str(dutypercent) + "%"
        print ""
        pwm.start(dutypercent)
        time.sleep(.5)
        
pwm.stop()

GPIO.cleanup()
