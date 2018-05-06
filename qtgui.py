#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont


class Example():

    def __init__(self):
        self.cageNum = 1
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
        self.revolutionsText.setText("Revolutions: " + str(self.cageNum))

        # The food dispense revs text
        self.foodRevolutionsText = QLabel(window)
        self.foodRevolutionsText.setFont(font)
        self.foodRevolutionsText.setText("Food: " + str(self.cageNum))

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

        # The overall window layout
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(numBox)
        vbox.addLayout(revBox)
        vbox.addLayout(foodBox)
        vbox.addLayout(btnBox)
        vbox.addStretch(1)
        window.setLayout(vbox)

        # Display the window to the user
        window.setWindowTitle("Research Cages")
        window.show()
        sys.exit(app.exec_())

    def rightButton(self):
        if(self.cageNum < 8):
            self.cageNum += 1
        self.cageNumText.setText("Cage number: " + str(self.cageNum))
        self.revolutionsText.setText("Revolutions: " + str(self.cageNum))
        self.foodRevolutionsText.setText("Food: " + str(self.cageNum))

    def leftButton(self):
        if(self.cageNum > 1):
            self.cageNum -= 1
        self.cageNumText.setText("Cage number: " + str(self.cageNum))
        self.revolutionsText.setText("Revolutions: " + str(self.cageNum))
        self.foodRevolutionsText.setText("Food: " + str(self.cageNum))


if __name__ == '__main__':
    ex = Example()
