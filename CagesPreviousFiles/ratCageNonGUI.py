import time
import smtplib
import RPi.GPIO as GPIO
import csv

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

freq = 50

sensors = [19,21,23,29,31,33,35,37]
feeders = [18,22,24,26,32,36,38,40]
pwm = [0,0,0,0,0,0,0,0]
passes = [0,0,0,0,0,0,0,0]
currentRevs = [1,1,1,1,1,1,1,1]
dispenseRevs = [10,10,10,10,10,10,10,10]
food = [0,0,0,0,0,0,0,0]
csvStart = time.time()
servoStart = time.time()
email = False


def sensor1(channel):
    passes[0] = passes[0] + 1

def sensor2(channel):
    passes[1] = passes[1] + 1
    print str(passes[1])

def sensor3(channel):
    passes[2] = passes[2] + 1

def sensor4(channel):
    passes[3] = passes[3] + 1

def sensor5(channel):
    passes[4] = passes[4] + 1

def sensor6(channel):
    passes[5] = passes[5] + 1

def sensor7(channel):
    passes[6] = passes[6] + 1

def sensor8(channel):
    passes[7] = passes[7] + 1

calls = [sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8]

for i in range(len(sensors)):
    GPIO.setup(sensors[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(sensors[i],GPIO.FALLING,callback=calls[i], bouncetime=50)

for i in range(len(feeders)):
    GPIO.setup(feeders[i], GPIO.OUT)
    pwm[i] = GPIO.PWM(feeders[i], freq)

while 1:
    for index, item in enumerate(passes):
        if(item >= 6):
            currentRevs[index] = currentRevs[index] + 1
            passes[index] = 0
            print "ID: " + str(index + 1) + " Revs: " + str(currentRevs[index])
            if(currentRevs[index]%dispenseRevs[index] == 0) and (email == False):
                pwm[i].start(11.75 - (food[i] * 1.25))
                food[index] = food[index] + 1
                email = True
                servoStart = time.time()
            
        if(email):
            server = smtplib.SMTP('smtp.gmail.com')
            server.starttls()
            server.login("researchcages@gmail.com","This is the password.")
            msg = "Cage " + str(index + 1) + " has triggered the food dispenser."
            server.sendmail("researchcages@gmail.com","akarnes1@asu.edu",msg)
            server.quit()
            print "Email sent"
            email = False

        if(servoStart + 1.5 > time.time()):
            pwm[index].start(11.75 -(1.25*food[index]))
        elif(servoStart + 3 > time.time()):
            pwm[index].start(11.75)
        else:
            pwm[index].stop()  

    if(csvStart + 600 > time.time()):
        with open('log.csv','wb') as csvfile:
            csvwrite = csv.writer(csvfile, delimiter=',')
            for index, item in enumerate(passes):
                csvwrite.writerow([index] + [currentRevs[index]] + [dispenseRevs[index]] + [food[index]] + [time.time()])
        csvStart = time.time()
            
for i in range(len(pwm)):
    pwm[i].stop()
GPIO.cleanup()


