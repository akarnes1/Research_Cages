# import RPI.GPIO as gpio


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
        text(self.word,self.x + (self.wid/2), self.y + (self.hei / 2))
        
    def hover(self):
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
    global cageNumber, revolutions
    cageNumber = 1
    revolutions = [1,2,3,4,5,6,7,8]
    size(640, 480)
    this.getSurface().setResizable(True)
    f = createFont("Georgia", 48)
    textFont(f)

def draw():
    global cageNumber, revolutions, leftButton, rightButton
    background(0)
    fill(255,255,255)
    textAlign(CENTER)
    text("Cage: " + str(cageNumber),width/2,height/10)
    text("Revolutions: " + str(revolutions[cageNumber-1]),width/2,(width/10)+50)
    leftButton = button(width/2-105,height - 105,75,75,125,125,125,"<<")
    rightButton = button(width/2 + 5,height - 105,75,75,125,125,125,">>")

def mousePressed():
    global cageNumber
    if (leftButton.hover()):
        if(cageNumber > 1):
            cageNumber = cageNumber - 1
    if (rightButton.hover()): 
        if(cageNumber < 8):
            cageNumber = cageNumber + 1
