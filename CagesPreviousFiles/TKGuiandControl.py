from tkinter import *
import time
import smtplib
import RPi.GPIO as GPIO
import csv
from threading import Thread

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

currentRevs = [1,1,1,1,1,1,1,1]
dispenseRevs = [3,3,10,10,10,10,10,10]
passes = [0,0,0,0,0,0,0,0]
food = [0,0,0,0,0,0,0,0]
pwm = [0,0,0,0,0,0,0,0]
index = 0
email = 0
move = True
csvStart = 0

sensors = [19,21,23,29,31,33,35,37]
feeders = [18,22,24,26,32,36,38,40]

def sensor1(channel):
   index = 0
   passes[index] = passes[index] + 1
   if (passes[index] >= 12):
      currentRevs[index] = currentRevs[index] + 1
      passes[index] = 0
      print("ID: " + (index + 1) + " Revs: " + str(currentRevs[index]))
      if(currentRevs[index]%dispenseRevs[index] == 0) and (email == 0):
         food[index] = food[index] + 1
         servoQueue.append(pwm[index])
         foodQueue.append(food[index])
         email = index + 1
         print("Servo and Email")

def sensor2(channel):
   index = 1
   passes[index] = passes[index] + 1
   if (passes[index] >= 12):
      currentRevs[index] = currentRevs[index] + 1
      passes[index] = 0
      print("ID: " + (index + 1) + " Revs: " + str(currentRevs[index]))
      if(currentRevs[index]%dispenseRevs[index] == 0) and (email == 0):
         food[index] = food[index] + 1
         servoQueue.append(pwm[index])
         foodQueue.append(food[index])
         email = index + 1
         print("Servo and Email")

def sensor3(channel):
   index = 2
   passes[index] = passes[index] + 1
   if (passes[index] >= 12):
      currentRevs[index] = currentRevs[index] + 1
      passes[index] = 0
      print("ID: " + (index + 1) + " Revs: " + str(currentRevs[index]))
      if(currentRevs[index]%dispenseRevs[index] == 0) and (email == 0):
         food[index] = food[index] + 1
         servoQueue.append(pwm[index])
         foodQueue.append(food[index])
         email = index + 1
         print("Servo and Email")

def sensor4(channel):
   index = 3
   passes[index] = passes[index] + 1
   if (passes[index] >= 12):
      currentRevs[index] = currentRevs[index] + 1
      passes[index] = 0
      print("ID: " + (index + 1) + " Revs: " + str(currentRevs[index]))
      if(currentRevs[index]%dispenseRevs[index] == 0) and (email == 0):
         food[index] = food[index] + 1
         servoQueue.append(pwm[index])
         foodQueue.append(food[index])
         email = index + 1
         print("Servo and Email")

def sensor5(channel):
   index = 4
   passes[index] = passes[index] + 1
   if (passes[index] >= 12):
      currentRevs[index] = currentRevs[index] + 1
      passes[index] = 0
      print("ID: " + (index + 1) + " Revs: " + str(currentRevs[index]))
      if(currentRevs[index]%dispenseRevs[index] == 0) and (email == 0):
         food[index] = food[index] + 1
         servoQueue.append(pwm[index])
         foodQueue.append(food[index])
         email = index + 1
         print("Servo and Email")

def sensor6(channel):
   index = 5
   passes[index] = passes[index] + 1
   if (passes[index] >= 12):
      currentRevs[index] = currentRevs[index] + 1
      passes[index] = 0
      print("ID: " + (index + 1) + " Revs: " + str(currentRevs[index]))
      if(currentRevs[index]%dispenseRevs[index] == 0) and (email == 0):
         food[index] = food[index] + 1
         servoQueue.append(pwm[index])
         foodQueue.append(food[index])
         email = index + 1
         print("Servo and Email")

def sensor7(channel):
   index = 6
   passes[index] = passes[index] + 1
   if (passes[index] >= 12):
      currentRevs[index] = currentRevs[index] + 1
      passes[index] = 0
      print("ID: " + (index + 1) + " Revs: " + str(currentRevs[index]))
      if(currentRevs[index]%dispenseRevs[index] == 0) and (email == 0):
         food[index] = food[index] + 1
         servoQueue.append(pwm[index])
         foodQueue.append(food[index])
         email = index + 1
         print("Servo and Email")

def sensor8(channel):
   index = 7
   passes[index] = passes[index] + 1
   if (passes[index] >= 12):
      currentRevs[index] = currentRevs[index] + 1
      passes[index] = 0
      print("ID: " + (index + 1) + " Revs: " + str(currentRevs[index]))
      if(currentRevs[index]%dispenseRevs[index] == 0) and (email == 0):
         food[index] = food[index] + 1
         servoQueue.append(pwm[index])
         foodQueue.append(food[index])
         email = index + 1
         print("Servo and Email")

calls = [sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8]

for index, item in enumerate(sensors):
   GPIO.setup(item, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
   GPIO.add_event_detect(item,GPIO.FALLING,callback=calls[index], bouncetime=50)

for index, item in enumerate(feeders):
   GPIO.setup(item, GPIO.OUT)
   pwm[index] = GPIO.PWM(item, 50)

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
   print(str(index))

def indexUp():
   global index
   if index < 7:
      index = index + 1
   foodEntry.delete(0,END)
   foodEntry.insert(0,str(dispenseRevs[index]))
   print(str(index))

def cleanup():
   for i in range(len(pwm)):
      pwm[i].stop()
      GPIO.cleanup()

def refresh():
   global index, currentRevs, dispenseRevs, move, email, csvStart
   cageEntry.delete(0,END)
   cageEntry.insert(0,str(index + 1))
   currentEntry.delete(0,END)
   currentEntry.insert(0,str(currentRevs[index]))
   if len(servoQueue) > 0 and move == True:
      move = False
      thread = servoThread(servoQueue.pop(), foodQueue.pop())
      print("Servo Thread")
      thread.start()

   email = 0   
   if email != 0:
      thread = emailThread(email)
      thread.start()
      email = 0
       
   if(csvStart + 600 < time.time()):
      csvStart = time.time()
      print("CSV Thread")
      thread = csvThread()
      thread.start()
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

class emailThread(Thread):
   def __init__(self, cageNumber):
      Thread.__init__(self)
      self.daemon = True
      self.cage = cageNumber

   def run(self):
       server = smtplib.SMTP('smtp.gmail.com')
       server.starttls()
       server.login("researchcages@gmail.com","This is the password.")
       msg = "Cage " + str(self.cage) + " has triggered the food dispenser."
       server.sendmail("researchcages@gmail.com","akarnes1@asu.edu",msg)
       server.quit()
       print("Email sent")


class servoThread(Thread):
   def __init__(self,servo,food):
      Thread.__init__(self)
      self.daemon = True
      self.servo = servo
      self.food = food
      print("Food pos: " + str(self.food))

   def run(self):
      global move
      print("Servo Start: ")
      self.servo.start(11.75 -(1.25*self.food))
      time.sleep(1.5)
      self.servo.start(11.75)
      time.sleep(1.5)
      self.servo.stop()
      print("Servo Done")
      move = True


class csvThread(Thread):
   def __init__(self):
      Thread.__init__(self)
      self.daemon = True

   def run(self):
      global index, currentRevs, dispenseRevs
      with open('log.csv','a') as csvfile:
         csvwrite = csv.writer(csvfile, delimiter=',')
         for index, item in enumerate(passes):
            csvwrite.writerow([index + 1] + [currentRevs[index]] + [dispenseRevs[index]] + [food[index]] + [time.asctime(time.localtime(time.time()))])
      
if __name__ == "__main__":
   top.mainloop()
