import time
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


input = GPIO.input(11)

while 1:
    if (GPIO.input(11)):
        GPIO.output(37,GPIO.HIGH)
        print "Port 3 is 1/GPIO.HIGH/True"
        time.sleep(.01)
    else:
        GPIO.output(37,GPIO.LOW)
        print "Port 3 is 0/GPIO.LOW/False"
        time.sleep(.01)
    

GPIO.cleanup()
