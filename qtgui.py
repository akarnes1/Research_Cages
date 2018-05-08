#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import smtplib
import sys
import time
from threading import Thread

from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QLineEdit)

import RPi.GPIO as GPIO


class Example():

    def __init__(self):
        self.initSettings()
        print("Settings Imported")
        self.initGPIO()
        print("GPIO Started")
        self.updateWindow()
        print("Update Called")
        self.initGUI()
        print("GUI Shown")

    def initSettings(self):
        # The code to load in the defined settings.
        self.emailAddress = "akarnes1@asu.edu"
        # TODO: Add in JSON reading here

    def initGUI(self):
        self.cageNum = 1
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateWindow)
        self.timer.start(200)
        app = QApplication(sys.argv)
        font = QFont("Times", 48)
        window = QWidget()
        window.setGeometry(30, 30, 720, 640)

        # The Cage number text
        self.cageNumText = QLabel(window)
        self.cageNumText.setFont(font)
        self.cageNumText.setText("Cage number: " + str(self.cageNum))

        # The Revolutions text
        self.revolutionsText = QLabel(window)
        self.revolutionsText.setFont(font)
        self.revolutionsText.setText(
            "Revolutions: " + str(self.currentRevolutions[self.cageNum - 1]))

        # The food dispense revs text
        self.foodRevolutionsText = QLabel(window)
        self.foodRevolutionsText.setFont(font)
        self.foodRevolutionsText.setText(
            "Food: " + str(self.revolutionsPerFood[self.cageNum - 1]))

        # The Food dispense revs text box
        self.foodRevolutionsEdit = QLineEdit()
        self.foodRevolutionsEdit.setFont(font)
        self.foodRevolutionsEdit.setText(str(self.cageNum))
        self.foodRevolutionsEdit.textChanged[str].connect(self.textChanged)

        # The right Button
        rightBtn = QPushButton(">>", window)
        rightBtn.setFont(font)
        rightBtn.move(120, 70)
        rightBtn.clicked.connect(self.rightButton)

        # The left button
        leftBtn = QPushButton("<<", window)
        leftBtn.setFont(font)
        leftBtn.move(50, 70)
        leftBtn.clicked.connect(self.leftButton)

        # The positioning of the buttons
        btnBox = QHBoxLayout()
        btnBox.addWidget(leftBtn)
        btnBox.addWidget(rightBtn)

        # The positioning of the cage number
        numBox = QHBoxLayout()
        numBox.addStretch(1)
        numBox.addWidget(self.cageNumText)
        numBox.addStretch(1)

        # The centering of the revolutions text
        revBox = QHBoxLayout()
        revBox.addStretch(1)
        revBox.addWidget(self.revolutionsText)
        revBox.addStretch(1)

        # The placement of the food text
        foodBox = QHBoxLayout()
        foodBox.addStretch(1)
        foodBox.addWidget(self.foodRevolutionsText)
        foodBox.addStretch(1)

        # The placement of the food edit
        editBox = QHBoxLayout()
        editBox.addStretch(1)
        editBox.addWidget(self.foodRevolutionsEdit)
        editBox.addStretch(1)

        # The overall window layout
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(numBox)
        vbox.addLayout(revBox)
        vbox.addLayout(foodBox)
        vbox.addLayout(editBox)
        vbox.addLayout(btnBox)
        vbox.addStretch(1)
        window.setLayout(vbox)

        # Display the window to the user
        window.setWindowTitle("Research Cages")
        window.show()
        sys.exit(app.exec_())

    def initGPIO(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.FREQUENCY = 50
        self.SENSORS = [19, 21, 23, 29, 31, 33, 35, 37]
        self.FEEDERS = [18, 38, 24, 26, 32, 36, 22, 40]
        self.pwm = [0, 0, 0, 0, 0, 0, 0, 0]
        self.passes = [0, 0, 0, 0, 0, 0, 0, 0]
        self.currentRevolutions = [1, 1, 1, 1, 1, 1, 1, 1]
        self.revolutionsPerFood = [10, 10, 10, 10, 10, 10, 10, 10]
        self.FOODPOSITIONS = [11.75, 10.85, 9.6,
                              8.4, 7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5]
        self.csvStart = time.time() - 601
        self.servoQueue = []
        self.foodQueue = []
        self.email = False
        self.move = True
        self.update = True
        self.calls = [self.sensor1, self.sensor2, self.sensor3,
                      self.sensor4, self.sensor5, self.sensor6,
                      self.sensor7, self.sensor8]

        for i in range(len(self.SENSORS)):
            GPIO.setup(self.SENSORS[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(self.SENSORS[i], GPIO.FALLING,
                                  callback=self.calls[i], bouncetime=20)

        for i in range(len(self.FEEDERS)):
            GPIO.setup(self.FEEDERS[i], GPIO.OUT)
            self.pwm[i] = GPIO.PWM(self.FEEDERS[i], self.FREQUENCY)
            self.pwm[i].start(self.FOODPOSITIONS[0])
            time.sleep(1)
            self.pwm[i].ChangeDutyCycle(0)

        print("Done Initializing")

    def textChanged(self, value):
        if(value != ""):
            self.revolutionsPerFood[self.cageNum - 1] = int(value)
            self.foodRevolutionsText.setText(
                "Food: " + str(self.revolutionsPerFood[self.cageNum - 1]))

        self.cageNumText.setText("Cage number: " + str(self.cageNum))
        self.revolutionsText.setText(
            "Revolutions: " + str(self.currentRevolutions[self.cageNum - 1]))
        self.foodRevolutionsEdit.setText(
            str(self.revolutionsPerFood[self.cageNum - 1]))

    def updateWindow(self):
        for index, item in enumerate(self.passes):
            if(item >= 6):
                self.currentRevolutions[index] = self.currentRevolutions[index] + 1
                item = item - 6
            if self.update == True:
                self.update = False
                # thread = updateThread(index, self.currentRevolutions[index])
                # thread.start()
            print("ID: " + str(index + 1) + " Revs: " +
                  str(self.currentRevolutions[index]) + " Dispense: " +
                  str(self.revolutionsPerFood[index]))
            if (self.currentRevolutions[index] % self.revolutionsPerFood[index] == 0):
                self.servoQueue.append(self.pwm[index])
                foodIndex = self.currentRevolutions[index] / \
                    self.revolutionsPerFood[index]
                self.foodQueue.append(self.FOODPOSITIONS[foodIndex])
                # email = index
        # if len(self.servoQueue) > 0 and self.move == True:
        #     self.move = False
        #     # thread = servoThread(servoQueue.pop(), foodQueue.pop())
        #     # thread.start()
        # if email != 0:
        #     # thread = emailThread(email)
        #     # thread.start()
        #     email = 0
        # if(self.csvStart + 600 < time.time()):
        #     self.csvStart = time.time()
        #     print("CSV Thread")
            # thread = csvThread()
            # thread.start()
        print("Update Window values")
        self.textChanged
    
    def    sensor1(self, channel):

        self.passes[0] = self.passes[0] + 1
        # print "1"

    def sensor2(self, channel):
        self.passes[1] = self.passes[1] + 1
        # print str(self.passes[1])

    def sensor3(self, channel):
        self.passes[2] = self.passes[2] + 1
        # print "3"

    def sensor4(self, channel):
        self.passes[3] = self.passes[3] + 1
        # print "4"

    def sensor5(self, channel):
        self.passes[4] = self.passes[4] + 1
        # print "5"

    def sensor6(self, channel):
        self.passes[5] = self.passes[5] + 1
        # print "6"

    def sensor7(self, channel):
        self.passes[6] = self.passes[6] + 1
        # print "7"

    def sensor8(self, channel):
        self.passes[7] = self.passes[7] + 1
        # print "8"

    def rightButton(self):
        if(self.cageNum < 8):
            self.cageNum += 1
        self.cageNumText.setText("Cage number: " + str(self.cageNum))
        self.revolutionsText.setText(
            "Revolutions: " + str(self.passes[self.cageNum - 1]))
        self.foodRevolutionsEdit.setText(
            str(self.revolutionsPerFood[self.cageNum - 1]))

    def leftButton(self):
        if(self.cageNum > 1):
            self.cageNum -= 1
        self.cageNumText.setText("Cage number: " + str(self.cageNum))
        self.revolutionsText.setText(
            "Revolutions: " + str(self.passes[self.cageNum - 1]))
        self.foodRevolutionsEdit.setText(
            str(self.revolutionsPerFood[self.cageNum - 1]))


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


class csvThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        with open('log.csv', 'a') as csvfile:
            csvwrite = csv.writer(csvfile, delimiter=',')
            for index in enumerate(self.passes):
                csvwrite.writerow([index + 1] + [self.currentRevolutions[index]] + [self.revolutionsPerFood[index]] + [
                                  food[index]] + [time.asctime(time.localtime(time.time()))])
        print("CSV Done")


class saveThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        data = loadJSONObject("startSettings.json")
        data.setString("emailAddress", emailAddress)
        jsonRevs = data.getJSONArray("revsPerFood")
        for i in range(0, 8):
            jsonRevs.setString(i, revsPerFood[i])

        # data.setJSONObject("settings",data)
        saveJSONObject(data, "startSettings.json")
        print("Saved Settings")


if __name__ == '__main__':
    ex = Example()
