import socket
import sys
from Tkinter import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8888)
print "connecting to %s port %s" % server_address
sock.connect(server_address)
print sock.recv(128)

index = 0
email = 0
move = True

servoQueue = []
foodQueue = []

top = Tk()
cageFrame = LabelFrame(top,text="Current Cage",font = 18)
cageFrame.pack()
currentFrame = LabelFrame(top, text = "Current Revolutions",font = 18)
currentFrame.pack()
foodFrame = LabelFrame(top,text="Revolutions per food",font = 18)
foodFrame.pack()
selectFrame = Frame(top)
selectFrame.pack()
saveFrame = Frame(top)
saveFrame.pack()

def save():
   entered = foodEntry.get()[0:6]
   sock.sendall(str("save," + str(index) + "," + entered))
   print sock.recv(128)

def indexDown():
   global index
   if index > 0:
      index = index - 1
   sock.sendall(str("disp," + str(index)))
   foodEntry.delete(0,END)
   foodEntry.insert(0,str(sock.recv(128)))
   print str(index)

def indexUp():
   global index
   if index < 7:
      index = index + 1
   sock.sendall(str("disp," + str(index)))
   foodEntry.delete(0,END)
   foodEntry.insert(0,str(sock.recv(128)))
   print str(index)

def refresh():
    global index
    cageEntry.delete(0,END)
    cageEntry.insert(0,str(index + 1))
    sock.sendall(str("current," + str(index)))
    currentEntry.delete(0,END)
    currentEntry.insert(0,str(sock.recv(128)))
    top.after(1000, refresh)

def sequence(*functions):
   def func(*args, **kwargs):
      return_value = None
      for function in functions:
         return_value = function(*args, **kwargs)
      return return_value
   return func

cageEntry = Entry(cageFrame, bd = 1,font = 18)
cageEntry.insert(0,str(index + 1))
cageEntry.pack()
currentEntry = Entry(currentFrame, bd = 1,font = 18)
currentEntry.insert(0,"1")
currentEntry.pack()
foodEntry = Entry(foodFrame,bd=1,font = 18)
foodEntry.insert(0,"100")
foodEntry.pack(side=BOTTOM)
selectLeft = Button(selectFrame, text = "<", command = sequence(indexDown,refresh),font = 18)
selectLeft.pack(side=LEFT)
selectRight = Button(selectFrame, text = ">", command = sequence(indexUp,refresh),font = 18)
selectRight.pack(side=RIGHT)
saveButton = Button(saveFrame, text ="Save", command = sequence(save,refresh),font = 18)
saveButton.pack()

if __name__ == "__main__":
   top.mainloop()
