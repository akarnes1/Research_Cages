import time
import smtplib
import RPi.GPIO as GPIO
import csv
import json
import sys
from threading import Thread
import colorama


colorama.init(autoreset=True)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

freq = 50

sensors = [19, 21, 23, 29, 31, 33, 35, 37]
feeders = [18, 38, 24, 26, 32, 36, 22, 40]
pwm = [0, 0, 0, 0, 0, 0, 0, 0]
passes = [0, 0, 0, 0, 0, 0, 0, 0]
currentRevs = [1, 1, 1, 1, 1, 1, 1, 1]
dispenseRevs = [10, 10, 10, 10, 10, 10, 10, 10]
food = [11.75, 10.85, 9.6, 8.4, 7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5]
csvStart = time.time() - 601
servoStart = time.time()
servoQueue = []
foodQueue = []

index = 0
email = False
move = True


def sensor1(channel):
    global passes
    passes[0] = passes[0] + 1


def sensor2(channel):
    global passes
    passes[1] = passes[1] + 1
    print(str(passes[1]))


def sensor3(channel):
    global passes
    passes[2] = passes[2] + 1


def sensor4(channel):
    global passes
    passes[3] = passes[3] + 1


def sensor5(channel):
    global passes
    passes[4] = passes[4] + 1


def sensor6(channel):
    global passes
    passes[5] = passes[5] + 1


def sensor7(channel):
    global passes
    passes[6] = passes[6] + 1


def sensor8(channel):
    global passes
    passes[7] = passes[7] + 1


class emailThread(Thread):
    def __init__(self, cageNumber):
        Thread.__init__(self)
        self.daemon = True
        self.cage = cageNumber

    def run(self):
        server = smtplib.SMTP('smtp.gmail.com')
        server.starttls()
        server.login("researchcages@gmail.com", "This is the password.")
        msg = "Cage " + str(self.cage) + " has triggered the food dispenser."
        server.sendmail("researchcages@gmail.com", "akarnes1@asu.edu", msg)
        server.quit()
        print("Email sent")


class servoThread(Thread):
    def __init__(self, servo, food):
        Thread.__init__(self)
        self.daemon = True
        self.servo = servo
        self.food = food
        print("Food pos: " + str(self.food))

    def run(self):
        global move
        print("Servo Start")
        self.servo.start(self.food)
        time.sleep(1.5)
        self.servo.ChangeDutyCycle(11.75)
        time.sleep(1.5)
        self.servo.start(self.food)
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
        with open('log.csv', 'a') as csvfile:
            csvwrite = csv.writer(csvfile, delimiter=',')
            for index, item in enumerate(passes):
                csvwrite.writerow([index + 1] + [currentRevs[index]] + [dispenseRevs[index]] + 
                                  [food[index]] + [time.asctime(time.localtime(time.time()))])
        print("CSV Done")


calls = [sensor1, sensor2, sensor3, sensor4,
         sensor5, sensor6, sensor7, sensor8]

for i in range(len(sensors)):
    GPIO.setup(sensors[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(sensors[i], GPIO.FALLING,
                          callback=calls[i], bouncetime=20)

for i in range(len(feeders)):
    GPIO.setup(feeders[i], GPIO.OUT)
    pwm[i] = GPIO.PWM(feeders[i], freq)
    pwm[i].start(food[0])
    time.sleep(1)
    pwm[i].ChangeDutyCycle(0)

with open('startSettings.json') as json
    settings = json.loads(json)
    
print("Done Initializing")


while 1:
    for i, item in enumerate(passes):
        if(item >= 6):
            currentRevs[i] = currentRevs[i] + 1
            passes[i] = passes[i] - 6
            print(colorama.Fore.BLUE + "ID: " + colorama.Fore.GREEN + str(i + 1) + 
                  colorama.Fore.BLUE + " Revs: " + colorama.Fore.GREEN +
                  str(currentRevs[i]) + colorama.Fore.BLUE + " Dispense: " + 
                  colorama.Fore.GREEN + str(dispenseRevs[i]))
            if (currentRevs[i] % dispenseRevs[i] == 0):
                servoQueue.append(pwm[i])
                foodIndex = int(currentRevs[i] / dispenseRevs[i])
                foodQueue.append(food[foodIndex])
                email = i

        if len(servoQueue) > 0 and move == True:
            move = False
            thread = servoThread(servoQueue.pop(), foodQueue.pop())
            thread.start()

        if email != 0:
            thread = emailThread(email)
            thread.start()
            email = 0

        if(csvStart + 600 < time.time()):
            csvStart = time.time()
            print(colorama.Fore.GREEN + "CSV Thread")
            thread = csvThread()
            thread.start()


for i in range(len(pwm)):
    pwm[i].stop()
GPIO.cleanup()
