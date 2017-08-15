import time
import RPi.GPIO as GPIO
from Tkinter import *

inputPin = 21

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(inputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


food = 0
pwmHome = 11.75

start = 0

passes = 0
totalRev = 1

current = 0
previous = 1

freq = 50
pwm = GPIO.PWM(18, freq)

left = 0.75
right = 2.9
mid = (right - left) / 2 + left

position = [left, mid, right, mid]

mspc = 1000/ freq

##top = Tk()
##text = Text(top)
##text.insert(INSERT,str(totalRev))
##text.pack()
##top.mainloop()

##def update_text():
##    txt.delete(1.0)
##    txt.insert(1.0,totalRev)
##    txt.update_idletasks()
##
##top.after(1000,update_text)
##
##while 1:
##    totalRev = totalRev + 1
    

while 1:
    ##print "Current: ", current, " Previous: ", previous
    
    previous = current
    current = GPIO.input(inputPin)
    if(current != previous):
        print "GPIO Changed"
        passes = passes + 1
        if(passes >= 12):
            totalRev = totalRev + 1
            passes = 0
            print "Total Rev: ", totalRev

            if(totalRev%10 == 0):
                start = time.time()
                food = food + 1
                
        
    if(start + 1.5 > time.time()):
        print str(start + 1.5) + " Time: " + str(time.time()) + " Feed"
        pwm.start(11.75 -(1.25*food))
    elif(start + 3 > time.time()):
        print str(start + 3) + " Time: " + str(time.time()) + " Close" 
        pwm.start(11.75)
    else:
        pwm.stop()    

pwm.stop()
GPIO.cleanup()

##Start is 11.75
## 1st 10.5
## 2nd 9.25
## 3rd 8
## 4th 6.75
## 5th 5.5
## 6th 4.25
## 7th 3



