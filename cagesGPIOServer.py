import time
import smtplib
import RPi.GPIO as GPIO
import csv
import socket
import sys
from threading import Thread

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8615)
print "connecting to %s port %s" % server_address
sock.connect(server_address)
print sock.recv(128)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

freq = 50

sensors = [19,21,23,29,31,33,35,37]
feeders = [18,38,24,26,32,36,22,40]
pwm = [0,0,0,0,0,0,0,0]
passes = [0,0,0,0,0,0,0,0]
currentRevs = [1,1,1,1,1,1,1,1]
dispenseRevs = [10,10,10,10,10,10,10,10]
food = [11.75,10.85,9.6,8.4,7.5,6.5,5.5,4.5,3.5,2.5,1.5]
csvStart = time.time() - 601
servoStart = time.time()
servoQueue = []
foodQueue = []
email = "akarnes1@asu.edu"

email = False
move = True
update = True

HOST = ''
PORT = 8615
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
s.listen(10)
print 'Socket now listening'

def sensor1(channel):
    global passes
    passes[0] = passes[0] + 1
    #print "1"

def sensor2(channel):
    global passes
    passes[1] = passes[1] + 1
    print str(passes[1])

def sensor3(channel):
    global passes
    passes[2] = passes[2] + 1
    #print "3"

def sensor4(channel):
    global passes
    passes[3] = passes[3] + 1
    #print "4"

def sensor5(channel):
    global passes
    passes[4] = passes[4] + 1
    #print "5"

def sensor6(channel):
    global passes
    passes[5] = passes[5] + 1
    #print "6"

def sensor7(channel):
    global passes
    passes[6] = passes[6] + 1
    #print "7"

def sensor8(channel):
    global passes
    passes[7] = passes[7] + 1
    #print "8"

def clientthread(conn):
    conn.send('Connected')
    reply = "1"
     
    while True:  
        data = conn.recv(128)
        client = data.split(',')
        print str(client)
        index = int(client[1])
        if client[0] == "disp":
            reply = str(dispenseRevs[index])
            conn.sendall(reply)
            print reply
        elif client[0] == "current":
            reply = str(currentRevs[index])
            conn.sendall(reply)
            print reply
        elif client[0] == "save":
            dispenseRevs[index] = int(client[2])
        elif client[0] == "update":
            currentRevs[index] = int(client[2])
            
        if not data: 
            break
        
    conn.close()


class emailThread(Thread):
   def __init__(self, cageNumber, foodNumber):
      Thread.__init__(self)
      self.daemon = True
      self.cage = cageNumber
      self.food = foodNumber

   def run(self):
       global email
       print("Email Start")
       server = smtplib.SMTP('smtp.gmail.com')
       server.starttls()
       server.login("researchcages@gmail.com","This is the password.")
       msg = "Cage " + str(self.cage) + " has triggered the food dispenser " + str(self.food) + " times."
       print(msg)
       server.sendmail("researchcages@gmail.com",email,msg)
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
      print("Servo Start")
      self.servo.ChangeDutyCycle(self.food)
      time.sleep(1.5)
      self.servo.ChangeDutyCycle(11.75)
      time.sleep(1.5)
      self.servo.ChangeDutyCycle(self.food)
      time.sleep(1.5)
      self.servo.ChangeDutyCycle(11.75)
      time.sleep(1.5)
      self.servo.ChangeDutyCycle(0)
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
      print "CSV Done"


calls = [sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8]

for i in range(len(sensors)):
    GPIO.setup(sensors[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(sensors[i],GPIO.FALLING,callback=calls[i], bouncetime=20)

for i in range(len(feeders)):
    GPIO.setup(feeders[i], GPIO.OUT)
    pwm[i] = GPIO.PWM(feeders[i], freq)
    pwm[i].start(food[0])
    time.sleep(1)
    pwm[i].ChangeDutyCycle(0)

print "Done Initializing"

while 1:
    for index, item in enumerate(passes):
        if(item >= 6):
            currentRevs[index] = currentRevs[index] + 1
            passes[index] = passes[index] - 6
            if update == True:
                update = False
                thread = updateThread(index,currentRevs[index])
                thread.start()   
            print "ID: " + str(index + 1) + " Revs: " + str(currentRevs[index]) + " Dispense: " + str(dispenseRevs[index])
            if (currentRevs[index] % dispenseRevs[index] == 0):
                servoQueue.append(pwm[index])
                foodIndex = currentRevs[index] / dispenseRevs[index]
                foodQueue.append(food[foodIndex])
                email = (index,foodIndex)
            
        if len(servoQueue) > 0 and move == True:
            move = False
            thread = servoThread(servoQueue.pop(), foodQueue.pop())
            thread.start()
  
        if email != 0:
            #print("Email Thread")
            thread = emailThread(email[0],email[1])
            thread.start()
            email = 0
               
        if(csvStart + 600 < time.time()):
            csvStart = time.time()
            print("CSV Thread")
            thread = csvThread()
            thread.start()

    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientthread ,(conn,))

            
for i in range(len(pwm)):
    pwm[i].stop()
GPIO.cleanup()


