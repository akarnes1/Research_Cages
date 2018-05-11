import RPi.GPIO as GPIO
import csv
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import traceback
import time
from pprint import pprint
from threading import Thread

import colorama

move = True


class main():

    def __init__(self):
        colorama.init(autoreset=True)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.PWM_FREQUENCY = 50
        self.FOOD = [11.75, 10.85, 9.6, 8.4, 7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5]
        self.SENSORS_GPIO_PINS = [19, 21, 23, 29, 31, 33, 35, 37]
        self.FEEDER_MOTOR_GPIO_PINS = [40,38,36,32,26,24,22,18]
        self.pwm = [0, 0, 0, 0, 0, 0, 0, 0]
        self.passes = [0, 0, 0, 0, 0, 0, 0, 0]
        self.currentRevolutions = [1, 1, 1, 1, 1, 1, 1, 1]
        self.revolutionsPerFood = [10, 10, 10, 10, 10, 10, 10, 10]

        self.emailAddress = "akarnes1@asu.edu"

        self.csvStart = time.time() - 601
        self.resetTime = time.time()
        self.servoQueue = []
        self.foodQueue = []

        self.email = 0

        with open('startSettings.json', 'r') as json_file:
            settings = json.load(json_file)

        self.emailAddress = settings["emailAddress"]
        print(self.emailAddress)

        for index, item in enumerate(settings["revsPerFood"]):
            self.revolutionsPerFood[index] = int(item)
            print(self.revolutionsPerFood[index])

        self.initGPIO()

        print("Done Initializing")

        self.main()

    def sensor1(self, channel):
        self.passes[0] = self.passes[0] + 1

    def sensor2(self, channel):
        self.passes[1] = self.passes[1] + 1

    def sensor3(self, channel):
        self.passes[2] = self.passes[2] + 1

    def sensor4(self, channel):
        self.passes[3] = self.passes[3] + 1

    def sensor5(self, channel):
        self.passes[4] = self.passes[4] + 1

    def sensor6(self, channel):
        self.passes[5] = self.passes[5] + 1

    def sensor7(self, channel):
        self.passes[6] = self.passes[6] + 1

    def sensor8(self, channel):
        self.passes[7] = self.passes[7] + 1

    def initGPIO(self):
        self.calls = [self.sensor1, self.sensor2, self.sensor3, self.sensor4,
                      self.sensor5, self.sensor6, self.sensor7, self.sensor8]

        for i in range(len(self.SENSORS_GPIO_PINS)):
            GPIO.setup(self.SENSORS_GPIO_PINS[i],
                       GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(self.SENSORS_GPIO_PINS[i], GPIO.FALLING,
                                  callback=self.calls[i], bouncetime=20)

        for i in range(len(self.FEEDER_MOTOR_GPIO_PINS)):
            GPIO.setup(self.FEEDER_MOTOR_GPIO_PINS[i], GPIO.OUT)
            self.pwm[i] = GPIO.PWM(
                self.FEEDER_MOTOR_GPIO_PINS[i], self.PWM_FREQUENCY)
            self.pwm[i].start(self.FOOD[0])
            time.sleep(1)
            self.pwm[i].ChangeDutyCycle(0)

    def main(self):
        global move
        titleColor = colorama.Fore.CYAN
        valueColor = colorama.Fore.GREEN
        try:
            while 1:
                for i, item in enumerate(self.passes):
                    if(item >= 6):
                        self.currentRevolutions[i] = self.currentRevolutions[i] + 1
                        self.passes[i] = self.passes[i] - 6
                        print(titleColor + "ID: " + valueColor + str(i + 1) +
                              titleColor + " Revs: " + valueColor +
                              str(self.currentRevolutions[i]) + titleColor + " Dispense: " +
                              valueColor + str(self.revolutionsPerFood[i]))
                        if (self.currentRevolutions[i] % self.revolutionsPerFood[i] == 0):
                            self.servoQueue.append(self.pwm[i])
                            foodIndex = int(
                                self.currentRevolutions[i] / self.revolutionsPerFood[i])
                            self.foodQueue.append(self.FOOD[foodIndex])
                            self.email = i

                    if len(self.servoQueue) > 0 and move == True:
                        move = False
                        thread = servoThread(
                            self.servoQueue.pop(), self.foodQueue.pop(), self.FOOD)
                        thread.start()

                    if self.email != 0:
                        thread = emailThread(self.email, self.emailAddress)
                        thread.start()
                        self.email = 0

                    if(self.csvStart + 600 < time.time()):
                        self.csvStart = time.time()
                        print(valueColor + "CSV Thread")
                        thread = csvThread(
                            self.passes, self.currentRevolutions, self.revolutionsPerFood)
                        thread.start()

        except KeyboardInterrupt:
            self.cleanup()
        except Exception:
            traceback.print_exc(file=sys.stdout)
        sys.exit(0)

    def cleanup(self):
        for i in range(len(self.pwm)):
            self.pwm[i].ChangeDutyCycle(self.FOOD[0])
            time.sleep(1.5)
            self.pwm[i].ChangeDutyCycle(0)
            time.sleep(1.5)
            self.pwm[i].ChangeDutyCycle(self.FOOD[0])
            time.sleep(1.5)
            self.pwm[i].stop()

        GPIO.cleanup()


class emailThread(Thread):
    def __init__(self, cageNumber, emailAddress):
        Thread.__init__(self)
        self.daemon = True
        self.cage = cageNumber
        self.emailAddress = emailAddress
        self.fromEmail = "researchcages@gmail.com"

    def run(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.fromEmail, "This is the password.")

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Food dispensed for a cage"
        msg['From'] = self.fromEmail
        msgBody = "Cage " + str(self.cage) + \
            " has triggered the food dispenser." + "\n" + \
            "Attached is the log from within the last 10 minutes"

        filename = "log.csv"
        f = open(filename)
        attachment = MIMEText(f.read())
        attachment.add_header('Content-Disposition',
                              'attachment', filename=filename)

        content = MIMEText(msgBody, 'plain')
        msg.attach(content)
        msg.attach(attachment)

        server.sendmail(self.fromEmail, self.emailAddress, msg.as_string())
        server.quit()
        print("Email sent")


class servoThread(Thread):
    def __init__(self, servo, foodLocation, FOOD):
        Thread.__init__(self)
        self.daemon = True
        self.servo = servo
        self.foodLocation = foodLocation
        self.FOOD = FOOD
        print("Food pos: " + str(self.foodLocation))

    def run(self):
        global move
        print("Servo Start")
        for i in range(2):
            if self.foodLocation < len(self.FOOD):
                self.servo.start(self.foodLocation)
                time.sleep(1.5)
                self.servo.ChangeDutyCycle(self.FOOD[0])
                time.sleep(1.5)
        self.servo.ChangeDutyCycle(0)
        print("Servo Done")
        move = True


class csvThread(Thread):
    def __init__(self, passes, currentRevs, dispenseRevs):
        Thread.__init__(self)
        self.daemon = True
        self.passes = passes
        self.currentRevolutions = currentRevs
        self.revolutionsPerFood = dispenseRevs

    def run(self):
        with open('log.csv', 'a', newline='') as csvfile:
            csvwrite = csv.writer(csvfile, delimiter=',')
            for index, item in enumerate(self.passes):
                csvwrite.writerow([index + 1] + [self.currentRevolutions[index]] + [self.revolutionsPerFood[index]] +
                                  [time.asctime(time.localtime(time.time()))])
        print("CSV Done")


if __name__ == "__main__":
    main()
