#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk

rev1 = [0,0,0,0,0,0,0,0]
foodRevs = [10,10,10,10,10,10,10,10]
index = 0

class HelloWorld:

    def saveInfo(self, widget, revEntry):
        entry_text = revEntry.get_text()
        global foodRevs
        foodRevs[index] = entry_text
        global rev1
        rev1[index] = rev1[index] + 100
        print str(foodRevs[index])
        print "Entry contents: %s\n" % entry_text

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
        revText.set_text(str(rev1[index]))
        revEntry.set_text(str(foodRevs[index]))
        indexText.set_text(str(index + 1))
        

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
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
        revText.set_text(str(rev1[index]))
        frame.add(revText)
        vbox.pack_start(frame,True,True,0)
        revText.show()

        frame = gtk.Frame("Revolutions per food")
        revEntry = gtk.Entry()
        revEntry.set_max_length(6)
        revEntry.set_text(str(foodRevs[index]))
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

##        self.refresh = gtk.Button("Refresh")
##        self.refresh.connect("pressed", self.refreshWindow, revEntry, revText, indexText)
##        vbox.pack_start(self.refresh,True,True,0)
##        self.refresh.show()

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

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
