add_library('RPi.GPIO')
import time
import csv
import smtplib
from threading import Thread

#Constants used for setting up the GPIO pins on the breakout board
CONST_PWM_FREQUENCY = 50
CONST_SENSORS = [19, 21, 23, 29, 31, 33, 35, 37]
CONST_FEEDERS = [18, 38, 24, 26, 32, 36, 22, 40]
CONST_FOOD_POSITIONS = [11.75, 10.85, 9.6, 8.4, 7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5]

#Global variables that are used in the other methods a lot.
cageNumber = 1
passes = [0, 0, 0, 0, 0, 0, 0, 0]
currentRevolutions = [0, 0, 0, 0, 0, 0, 0, 0]
revsPerFood = ["10", "10", "10", "10", "10", "10", "10", "10"]
emailAddress = ""
pwm = []
sensors = []
servoQueue = []
foodQueue = []
email = 0

#Attempt at making the interrupts used for counting revolutions better.
class interrupt():
    def __init__(self,index, pin):
        self.index = index
        GPIO.setup(pin,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.update(), bouncetime = 10)
        
    def update(self):
        global passes
        passes[self.index] = passes[self.index] + 1
        
#An attempt at making the feeder servos easier to create.
class feeder():
    def __init__(self,pin,startPos,freq):
        GPIO.setup(pin,GPIO.OUT)
        self.freq = freq
        self.pwm = GPIO.PWM(pin,freq)
        self.pwm.start(startPos)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(0)
        
    def handOff(self):
        return self.pwm
        
#A class to run the servo movement code while not delaying the execution of the rest of the environment
class servoThread(Thread):
    def __init__(self, servo, food):
        Thread.__init__(self)
        self.daemon = False
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
        
#The code to send an email while not delaying the rest of the code
class emailThread(Thread):
    def __init__(self, cageNumber):
        Thread.__init__(self)
        self.daemon = True
        self.cage = cageNumber

    def run(self):
        global emailAddress
        if(emailAddress != ""):
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login("researchcages@gmail.com", "This is the password.")
            msg = "Cage " + str(self.cage) + " has triggered the food dispenser."
            server.sendmail("researchcages@gmail.com", emailAddress, msg)
            server.quit()
            print("Email sent")
        else:
            print("Email Address is not a value")
        
#The code to save the current variables to a csv for use in data analysis
class csvThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        global currentRevolutions, revsPerFood
        with open('log.csv', 'a') as csvfile:
            csvwrite = csv.writer(csvfile, delimiter=',')
            for index, item in enumerate(passes):
                csvwrite.writerow([index + 1] + [currentRevolutions[index]] + [revsPerFood[index]] + [currentRevolutions[index] / int(revsPerFood[index])] +  [time.asctime(time.localtime(time.time()))])
        print "CSV Done"

#A class to save the settings.        
class saveThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        
    def run(self):
        global revsPerFood, emailAddress
        data = loadJSONObject("startSettings.json")
        data.setString("emailAddress",emailAddress)
        jsonRevs = data.getJSONArray("revsPerFood")
        for i in range(0,8):
            jsonRevs.setString(i,revsPerFood[i])
            
        # data.setJSONObject("settings",data)
        saveJSONObject(data,"startSettings.json")
        print("Saved Settings")

#A class to make on screen buttons easy to call, update, and listen to.
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
        text(self.word,self.x + (self.wid/2), self.y + (self.hei / 2) - 12)
    
    #The code that changes a buttons color on mouse over.    
    def hover(self):
        textAlign(CENTER,CENTER)
        if (mouseX >= self.x and mouseX <= self.x+self.wid and mouseY >= self.y and mouseY <= self.y+self.hei):
            fill(255,255,255)
            rect(self.x,self.y,self.wid,self.hei)
            fill(self.r,self.g,self.b)        
            text(self.word,self.x + (self.wid/2), self.y + (self.hei / 2) - 12)
            return True;
        else:
            fill(self.r,self.g,self.b)
            rect(self.x,self.y,self.wid,self.hei)
            fill(255,255,255)
            text(self.word,self.x + (self.wid/2), self.y + (self.hei / 2) - 12)
            return False;
        
#The code to run once before everythin else begins
def setup():
    global currentRevolutions, revsPerFood, emailAddress, csvStart, email, move, update, sensors, pwm
    size(1280, 720)
    this.getSurface().setResizable(True)
    f = createFont("Helvetica", 48)
    textFont(f)
    frameRate(1000)
    
    #The code to load in the defined settings.
    data = loadJSONObject('startSettings.json')
    emailAddress = data.getString("emailAddress")
    jsonRevs = data.getJSONArray("revsPerFood")
    for i in range(0,8):
        revsPerFood[i] = jsonRevs.getString(i)
        
    csvStart = time.time() - 601
    servoStart = time.time()
    
    email = 0
    move = True
    
    for index, item  in enumerate(CONST_SENSORS):
        sensors[index] = interrupt(index,item)
        print("Interrupt: " + str(index))
        
    for index, item in enumerate(CONST_FEEDERS):
        pwm[index] = feeder(item,CONST_FOOD_POSITIONS[0],CONST_PWM_FREQUENCY)
        time.sleep(500)
        print("Servo: " + str(index))

#This code runs in an infinite loop after setup is called.     
def draw():
    global cageNumber, currentRevolutions, leftButton, rightButton, saveButton, revsPerFood, servoQueue, foodQueue, email, csvStart    
    
    #This is where the display gets rendered from
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
    text(int(frameRate),20,20)
    leftButton = button(textX + 150,height/10 -20,50,50,150,150,150,"-")
    rightButton = button(textX + 210,height/10 - 20,50,50,150,150,150,"+")
    saveButton = button(textX,textY + 300, 300, 60,150,150,150,"Save Settings")
    leftButton.hover()
    rightButton.hover()
    saveButton.hover()
    
    #This is what updates the current revolutions based on the passes array
    for index, item in enumerate(passes):
        if(item >= 6):
            currentRevs[index] = currentRevs[index] + 1
            passes[index] = passes[index] - 6
            print "ID: " + str(index + 1) + " Revs: " + \
                str(currentRevs[index]) + " Dispense: " + \
                str(dispenseRevs[index])
            if (currentRevs[index] % dispenseRevs[index] == 0):
                servoQueue.append(pwm[index])
                foodIndex = currentRevs[index] / dispenseRevs[index]
                foodQueue.append(food[foodIndex])
                email = index

        #this calls the servo to move only one at a time
        if len(servoQueue) > 0 and move == True:
            move = False
            thread = servoThread(servoQueue.pop(), foodQueue.pop())
            thread.start()

        #this starts sending an email when a cage triggers the food
        if email != 0:
            thread = emailThread(email)
            thread.start()
            email = 0

        #This saves the variables currentRevolutions, revsPerFood, and number of times dispensed to a csv for analysis
        if(csvStart + 600 < time.time()):
            csvStart = time.time()
            print("CSV Thread: " + str(time.asctime(time.localtime(time.time()))))
            thread = csvThread()
            thread.start()


def mousePressed():
    global cageNumber
    if (leftButton.hover()):
        if(cageNumber > 1):
            cageNumber = cageNumber - 1
    if (rightButton.hover()): 
        if(cageNumber < 8):
            cageNumber = cageNumber + 1
    if (saveButton.hover()):
        print("Begun saving settings")
        thread = saveThread()
        thread.start()
 
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
