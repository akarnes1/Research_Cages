from Tkinter import *
import time
import smtplib
import RPi.GPIO as GPIO
import csv
from threading import Thread

currentRevs = [1,1,1,1,1,1,1,1]
dispenseRevs = [3,3,10,10,10,10,10,10]
passes = [0,0,0,0,0,0,0,0]
food = [0,0,0,0,0,0,0,0]
pwm = [0,0,0,0,0,0,0,0]
index = 0
email = 0
move = True

servoQueue = []
foodQueue = []

top = Tk()
cageFrame = LabelFrame(top,text="Current Cage",font = 18)
cageFrame.pack()
currentFrame = LabelFrame(top, text = "Current Revolutions",font = 18)
currentFrame.pack()
foodFrame = LabelFrame(top,text="Revolutions per food",font = 18)
foodFrame.pack()
selectFrame = Frame(top)
selectFrame.pack()
saveFrame = Frame(top)
saveFrame.pack()

def save():
   global dispenseRevs
   entered = foodEntry.get()[0:6]
   dispenseRevs[index] = int(entered)

def indexDown():
   global index
   if index > 0:
      index = index - 1
   foodEntry.delete(0,END)
   foodEntry.insert(0,str(dispenseRevs[index]))
   print str(index)

def indexUp():
   global index
   if index < 7:
      index = index + 1
   foodEntry.delete(0,END)
   foodEntry.insert(0,str(dispenseRevs[index]))
   print str(index)

def refresh():
   global index, currentRevs, dispenseRevs
   cageEntry.delete(0,END)
   cageEntry.insert(0,str(index + 1))
   currentEntry.delete(0,END)
   currentEntry.insert(0,str(currentRevs[index]))
   top.after(1000, refresh)

def sequence(*functions):
   def func(*args, **kwargs):
      return_value = None
      for function in functions:
         return_value = function(*args, **kwargs)
      return return_value
   return func

cageEntry = Entry(cageFrame, bd = 1,font = 18)
cageEntry.insert(0,str(index + 1))
cageEntry.pack()
currentEntry = Entry(currentFrame, bd = 1,font = 18)
currentEntry.insert(0,str(currentRevs[index]))
currentEntry.pack()
foodEntry = Entry(foodFrame,bd=1,font = 18)
foodEntry.insert(0,str(dispenseRevs[index]))
foodEntry.pack(side=BOTTOM)
selectLeft = Button(selectFrame, text = "<", command = sequence(indexDown,refresh),font = 18)
selectLeft.pack(side=LEFT)
selectRight = Button(selectFrame, text = ">", command = sequence(indexUp,refresh),font = 18)
selectRight.pack(side=RIGHT)
saveButton = Button(saveFrame, text ="Save", command = sequence(save,refresh),font = 18)
saveButton.pack()

if __name__ == "__main__":
   top.mainloop()
