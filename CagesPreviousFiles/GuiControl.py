import time
import smtplib
import RPi.GPIO as GPIO
import csv
from threading import Thread
import pygtk
pygtk.require('2.0')
import gtk

currentRevs = [1,1,1,1,1,1,1,1]
dispenseRevs = [10,10,10,10,10,10,10,10]
passes = [0,0,0,0,0,0,0,0]
food = [0,0,0,0,0,0,0,0]
pwm = [0,0,0,0,0,0,0,0]
index = 0
email = False
start = 0

def sensor1(channel):
    passes[1] = passes[1] + 1
    ##print "1"

def sensor2(channel):
    passes[2] = passes[2] + 1
    ##print "2"

def sensor3(channel):
    passes[3] = passes[3] + 1
    ##print "3"

def sensor4(channel):
    passes[4] = passes[4] + 1
    ##print "4"

def sensor5(channel):
    passes[5] = passes[5] + 1
    ##print "5"

def sensor6(channel):
    passes[6] = passes[6] + 1
    ##print "6"

def sensor7(channel):
    passes[7] = passes[7] + 1
    ##print "7"

def sensor8(channel):
    passes[8] = passes[8] + 1
    ##print "8"

def GPIOinit():
    global pwm
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    freq = 50

    sensors = [19,21,23,29,31,33,35,37]
    feeders = [18,22,24,26,32,36,38,40]

    calls = [sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8]

    for i in range(len(sensors)):
        GPIO.setup(sensors[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(sensors[i],GPIO.FALLING,callback=calls[i], bouncetime=50)

    for i in range(len(feeders)):
        GPIO.setup(feeders[i], GPIO.OUT)
        pwm[i] = GPIO.PWM(feeders[i], freq)

    global start
    start = time.time()

def GPIOrun():
    while True:
        global passes
        global email
        global currentRevs
        global food
        global csvStart, servoStart, pwm, start
        for index, item in enumerate(passes):
            if(item >= 12):
                currentRevs[index] = currentRevs[index] + 1
                passes[index] = 0
                print "ID: " + str(index) + " Revs: " + str(currentRevs[index])
                if(currentRevs[index]%dispenseRevs[index] == 0) and (email == False):
                    pwm[index].start(11.75 - (food[index] * 1.25))
                    food[index] = food[index] + 1
                    email = True
                
            if(email):
                server = smtplib.SMTP('smtp.gmail.com')
                server.starttls()
                server.login("researchcages@gmail.com","This is the password.")
                msg = "Cage " + str(index) + " has triggered the food dispenser."
                server.sendmail("researchcages@gmail.com","akarnes1@asu.edu",msg)
                server.quit()
                print "Email sent"
                email = False

        if(start + 600 < time.time()):
            with open('log.csv','a') as csvfile:
                csvwrite = csv.writer(csvfile, delimiter=',')
                for index, item in enumerate(passes):
                    csvwrite.writerow([index + 1] + [currentRevs[index]] + [dispenseRevs[index]] + [food[index]] + [time.time()])
            start = time.time()
            
    for i in range(len(pwm)):
        pwm[i].stop()
    GPIO.cleanup()

class GUI(Thread):
    def saveInfo(self, widget, revEntry):
        entry_text = revEntry.get_text()
        global dispenseRevs
        dispenseRevs[index] = entry_text
        print "ID: " + str(index) + " Dispense Revs: " + str(dispenseRevs[index])

    def left(self, widget, data=None):
        global index
        if not index <= 0:
           index = index - 1
           print "Index Down"
           
    def right(self, wdiget, data=None):
        global index
        if not index >= 7:
           index = index + 1
           print "Index up"

    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False

    def refreshWindow(self, widget, revEntry, revText, indexText):
        revText.set_text(str(currentRevs[index]))
        revEntry.set_text(str(dispenseRevs[index]))
        indexText.set_text(str(index + 1))
        

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        # Sets the border width of the window.
        self.window.set_border_width(5)
        self.window.set_title("Cage settings")

        vbox = gtk.VBox(False,0)
        hbox = gtk.HBox(False,0)
        self.window.add(vbox)
        vbox.show()

        frame = gtk.Frame("Cage")
        indexText = gtk.Entry()
        indexText.set_editable(False)
        indexText.set_text(str(index + 1))
        frame.add(indexText)
        vbox.pack_start(frame,True,True,0)
        indexText.show()

        frame = gtk.Frame("Current revolutions")
        revText = gtk.Entry()
        revText.set_editable(False)
        revText.set_text(str(currentRevs[index]))
        frame.add(revText)
        vbox.pack_start(frame,True,True,0)
        revText.show()

        frame = gtk.Frame("Revolutions per food")
        revEntry = gtk.Entry()
        revEntry.set_max_length(6)
        revEntry.set_text(str(dispenseRevs[index]))
        frame.add(revEntry)
        vbox.pack_start(frame,True,True,0)
        revEntry.show()
        
        vbox.add(hbox)
        hbox.show()

        # Creates a new button with the label "Hello World".
        self.save = gtk.Button("Save")
        self.save.connect("pressed", self.saveInfo, revEntry)
        self.save.connect("pressed", self.refreshWindow, revEntry, revText, indexText)
        vbox.pack_start(self.save,True,True,0)
        self.save.show()

    ##    self.refresh = gtk.Button("Refresh")
    ##    self.refresh.connect("pressed", self.refreshWindow, revEntry, revText, indexText)
    ##    vbox.pack_start(self.refresh,True,True,0)
    ##    self.refresh.show()

        self.leftBut = gtk.Button("<")
        self.leftBut.connect("pressed", self.left)
        self.leftBut.connect("pressed", self.refreshWindow, revEntry, revText, indexText)
        hbox.pack_start(self.leftBut,True,True,0)
        self.leftBut.show()

        self.rightBut = gtk.Button(">")
        self.rightBut.connect("pressed", self.right)
        self.rightBut.connect("pressed", self.refreshWindow, revEntry, revText, indexText)
        hbox.pack_start(self.rightBut,True,True,0)
        self.rightBut.show()

        # and the window
        self.window.show_all()

    def run(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
##def run(self):
##    if __name__ == "__main__":
##        global hello
##        hello = GUIThread()
##        hello.main()


GPIOinit()
thread1 = Thread(target=GPIOrun)
thread1.start()
GUI()
