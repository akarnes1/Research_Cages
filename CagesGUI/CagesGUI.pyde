# import RPi.GPIO as gpio
import time
import csv
import json
from threading import Thread

class interrupt():
    def __init__(self,index, pin):
        self.index = index
        gpio.setup(pin,gpio.IN, pull_up_down = gpio.PUD_DOWN)
        gpio.add_event_detect(pin, gpio.FALLING, callback=self.update(), bouncetime = 10)
        
    def update(self):
        global passes
        passes[self.index] = passes[self.index] + 1
        
class feeder():
    def __init__(self,pin,startPos,freq):
        gpio.setup(pin,gpio.OUT)
        self.freq = freq
        self.pwm = gpio.PWM(pin,freq)
        self.pwm.start(startPos)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(0)
        
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
        
class emailThread(Thread):
    def __init__(self, cageNumber):
        Thread.__init__(self)
        self.daemon = True
        self.cage = cageNumber

    def run(self):
        global emailAddress
        server = smtplib.SMTP('smtp.gmail.com')
        server.starttls()
        server.login("researchcages@gmail.com", "This is the password.")
        msg = "Cage " + str(self.cage) + " has triggered the food dispenser."
        server.sendmail("researchcages@gmail.com", emailAddress, msg)
        server.quit()
        print("Email sent")
        
class csvThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        global index, currentRevs, dispenseRevs
        with open('log.csv', 'a') as csvfile:
            csvwrite = csv.writer(csvfile, delimiter=',')
            for index, item in enumerate(passes):
                csvwrite.writerow([index + 1] + [currentRevs[index]] + [dispenseRevs[index]] + [
                                  food[index]] + [time.asctime(time.localtime(time.time()))])
        print "CSV Done"


class button():
    
    def __init__(self,xLoc,yLoc,wide,tall,colr,colg,colb,word):
        self.x = xLoc
        self.y = yLoc
        self.wid = wide
        self.hei = tall
        self.r = colr
        self.g = colg
        self.b = colb
        self.word = word
        fill(self.r,self.g,self.b)
        rect(self.x,self.y,self.wid,self.hei)
        fill(255,255,255)
        textAlign(CENTER,CENTER)
        text(self.word,self.x + (self.wid/2), self.y + (self.hei / 2))
        
    def hover(self):
        textAlign(CENTER,CENTER)
        if (mouseX >= self.x and mouseX <= self.x+self.wid and mouseY >= self.y and mouseY <= self.y+self.hei):
            fill(255,255,255)
            rect(self.x,self.y,self.wid,self.hei)
            fill(self.r,self.g,self.b)        
            text(self.word,self.x + (self.wid/2), self.y + (self.hei / 2))
            return True;
        else:
            fill(self.r,self.g,self.b)
            rect(self.x,self.y,self.wid,self.hei)
            fill(255,255,255)
            text(self.word,self.x + (self.wid/2), self.y + (self.hei / 2))
            return False;
        
    
def setup():
    global cageNumber, currentRevolutions, revsPerFood
    cageNumber = 1
    size(640, 480)
    this.getSurface().setResizable(True)
    f = createFont("Georgia", 48)
    textFont(f)
    
    CONST_PWM_FREQUENCY = 50
    CONST_SENSORS = [19, 21, 23, 29, 31, 33, 35, 37]
    CONST_FEEDERS = [18, 38, 24, 26, 32, 36, 22, 40]
    CONST_FOOD_POSITIONS = [11.75, 10.85, 9.6, 8.4, 7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5]
    pwm = [0, 0, 0, 0, 0, 0, 0, 0]
    passes = [0, 0, 0, 0, 0, 0, 0, 0]
    currentRevolutions = [0, 0, 0, 0, 0, 0, 0, 0]
    revsPerFood = ["10", "10", "10", "10", "10", "10", "10", "10"]
    csvStart = time.time() - 601
    servoStart = time.time()
    servoQueue = []
    foodQueue = []
    
    email = False
    move = True
    update = True

def draw():
    global cageNumber, currentRevolutions, leftButton, rightButton, revsPerFood
    background(175)
    stroke(0,0,0)
    textX = width/2 -150
    textY = height/10
    fill(255,255,255)
    rect(textX,textY+35,300,45)
    rect(textX,textY+135,300,45)
    rect(textX,textY+235,300,45)
    fill(0,0,0)
    textAlign(LEFT,CENTER)
    text("Cage: ",textX,textY)
    text(str(cageNumber),textX,textY + 50)
    text("Current revolutions: ",textX,textY + 100)
    text(str(currentRevolutions[cageNumber-1]),textX,textY + 150)
    text("Revolutions per food: ",textX,textY + 200)
    text(str(revsPerFood[cageNumber - 1]),textX,textY + 250)
    leftButton = button(textX + 150,height/10 -20,50,50,150,150,150,"-")
    rightButton = button(textX + 210,height/10 - 20,50,50,150,150,150,"+")
    leftButton.hover()
    rightButton.hover()

def mousePressed():
    global cageNumber
    if (leftButton.hover()):
        if(cageNumber > 1):
            cageNumber = cageNumber - 1
    if (rightButton.hover()): 
        if(cageNumber < 8):
            cageNumber = cageNumber + 1
 
def keyPressed():
    global revsPerFood, cageNumber
    if (key == BACKSPACE):
        if (len(revsPerFood[cageNumber - 1]) > 0):
                revsPerFood[cageNumber - 1] = revsPerFood[cageNumber - 1][0: len(revsPerFood[cageNumber - 1])-1]
    elif (key == DELETE):
        revsPerFood[cageNumber - 1] = 0
    elif (keyCode == LEFT):
        if(cageNumber > 1):
            cageNumber = cageNumber - 1
    elif (keyCode == RIGHT):
        if(cageNumber < 8):
            cageNumber = cageNumber + 1
            
    if(len(revsPerFood[cageNumber - 1]) < 6):
        if (key >= '0' and key <= '9'):
            try: 
                revsPerFood[cageNumber - 1] = revsPerFood[cageNumber - 1] + str(int(chr(keyCode)))
            except:
                print("invalid")
