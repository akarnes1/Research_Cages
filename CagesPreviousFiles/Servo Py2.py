import RPi.GPIO as GPIO

import time
pin = 38
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)


def moveServo (currentPos, moveTo):
    while (currentPos > moveTo):
        currentPos -= 0.01
        pwm.start(currentPos)
        time.sleep(0.01)
    return;

freq = 50
pwm = GPIO.PWM(pin, freq)

left = 0.75
right = 2.9
mid = (right - left) / 2 + left

position = [left, mid, right, mid]

mspc = 1000/ freq

##while 1:
####    moveServo(right*100/mspc,left*100/mspc)
##    food = 0
##    while food < 8:
##        print str(food)
##        pwm.start(11.75 -(1.25*food)) ##14.5
##        time.sleep(1)
##        food = food + 1
    


    
food = [11.75,10.85,9.6,8.4,7.5,6.5,5.5,4.5,3.5,2.5,1.5]
    
for index, item in enumerate(food):
    pwm.start(item)
    time.sleep(5)

##pwm.start(1.5)
##time.sleep(1.5)
pwm.stop()

GPIO.cleanup()
#White
#11.75
#10.85
#9.6
#8.4
#7.5
#6.5
#5.5
#4.5
#3.5
#2.5
#1.5



#Blue
#2.75
#3.75
#4.5
#5.15
#5.75
#6.45
#7.25
#8.05
#8.85
#9.65
#10.45
