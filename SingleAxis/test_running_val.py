import math
import threading
import time

from Tkinter import *

theUI = Tk()
theUI.pack_slaves()
theUI.geometry("500x500")


def onoff(cur):
    # print "delay val:",cur
    # self.obj.setPin(4)
    time.sleep(cur)
    # self.obj.clearPin(4)
    time.sleep(cur)


class testvar(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    # print "thread initialized"

    def run(self):
        print
        "Starting " + self.name
        # Get lock to synchronize threads
        # threadLock.acquire()
        if self.threadID == 1:
            start_motor(1)
        elif self.threadID == 0:
            start_motor(0)
        # Free lock to release next thread
        # threadLock.release()


def setvar(self):
    self.running = 1


def clearvar(self):
    self.running = 0


def returnvar(self):
    return self.running


def checkval(event, val):
    thread = testvar(val, "threadID")
    thread.start()


running = 0
initialVelocity = 0
curDistance = 0
acceleration = 80
totaldist = 0  # initialized to zero, changed in else part of outer if statement
finalVelocity = 0
pulses = 0


def start_motor(var):
    global running
    global initialVelocity
    global curDistance
    global acceleration
    global pulses
    global finalVelocity

    curDistance = 0

    if var == 1:
        running = 1
        while (initialVelocity < 50 and running != 0):
            finalVelocity = math.sqrt(initialVelocity * initialVelocity + (2 * acceleration * 0.0025))
            dela = (finalVelocity - initialVelocity) / acceleration
            onoff(dela)
            pulses -= 1
            initialVelocity = finalVelocity
            curDistance += 0.0025
            print
            "increasing vel :", finalVelocity
        if (initialVelocity >= 50):
            while (running != 0):
                onoff(dela)
                pulses -= 1
                curDistance += 0.0025
                print
                "constant vel :", finalVelocity
    else:
        running = 0
        # if(curDistance<totaldist):
        while (finalVelocity > 1):
            # print "initialVelocity :",initialVelocity
            finalVelocity = math.sqrt(initialVelocity * initialVelocity - (2 * acceleration * 0.0025))
            # print "final velocity",finalVelocity
            dela = (initialVelocity - finalVelocity) / acceleration
            onoff(dela)
            pulses -= 1
            initialVelocity = finalVelocity
            curDistance += 0.0025
            print
            "decreaing vel :", finalVelocity
    print
    "distance :", curDistance
    # else:


def fixedDistance():
    global initialVelocity
    global curDistance
    global acceleration
    global totaldist
    global pulses
    global finalVelocity

    initialVelocity = 0
    curDistance = 0
    acceleration = 80
    finalVelocity = 0
    pulses = 0
    totaldist = int(distanceEntry.get())
    pulses = totaldist * 400
    while (initialVelocity < 50 and curDistance <= (totaldist / float(2))):
        finalVelocity = math.sqrt(initialVelocity * initialVelocity + (2 * acceleration * 0.0025))
        dela = (finalVelocity - initialVelocity) / acceleration
        onoff(dela)
        pulses -= 1
        initialVelocity = finalVelocity
        curDistance += 0.0025
        # print finalVelocity,pulses,curDistance
    # print "distance :",curDistance
    # print "after increasing:",pulses
    if (initialVelocity >= 50):
        twotimesdist = 0
        while (curDistance <= (totaldist / 2)):
            # finalVelocity,delay=myOtherFunction(initialVelocity)
            onoff(dela)
            pulses -= 1
            curDistance += 0.0025
            twotimesdist += 1
            print
            "constant vel 1 :", finalVelocity
        while (twotimesdist >= 0):
            # finalVelocity,delay=myOtherFunction(initialVelocity)
            onoff(dela)
            pulses -= 1
            curDistance += 0.0025
            twotimesdist -= 1
            print
            "constant vel 2", finalVelocity
    print
    "pulses", pulses
    if (curDistance < totaldist):
        while (pulses > 1):
            # print "initialVelocity :",initialVelocity
            finalVelocity = math.sqrt((initialVelocity * initialVelocity) - (2 * acceleration * 0.0025))
            # print "final velocity",finalVelocity
            dela = (initialVelocity - finalVelocity) / acceleration
            onoff(dela)
            pulses -= 1
            initialVelocity = finalVelocity
            curDistance += 0.0025
            # print finalVelocity,pulses,curDistance
            # print "pulses",pulses
            # print "decreaing vel :",finalVelocity
    print
    "distance :", curDistance

    # print("final distance:",curDistance)


def stop_motor(event):
    testobj.clearvar()
    print
    "stopping.."


def backward_call():
    global running
    while running == 1:
        print
        "running.."
    print
    "stopping..."


def fakefncn(event):
    print
    "nothing"


maxVelocityLabel_var = IntVar()
maxVelocityLabel_var.set("Maximum Velocity: ")
maxVelocityLabel = Label(theUI, textvariable=maxVelocityLabel_var, font=("Helvetica", 12))
maxVelocityLabel.grid(rowspan=2, row=0, column=0, sticky=EW)
accelerationEntry = Entry(theUI, bd=3, font=("Helvetica", 12))
accelerationEntry.grid(rowspan=2, row=0, column=1, sticky=EW)

accelerationLabel_var = IntVar()
accelerationLabel_var.set("Acceleration: ")
accelerationLabel = Label(theUI, textvariable=accelerationLabel_var, font=("Helvetica", 12))
accelerationLabel.grid(rowspan=2, row=2, column=0, sticky=EW + NS)
pitchEntry = Entry(theUI, bd=3, font=("Helvetica", 12))
pitchEntry.grid(rowspan=2, row=2, column=1, sticky=EW)

pitchLabel_var = IntVar()
pitchLabel_var.set("Pitch: ")
pitchLabel = Label(theUI, textvariable=pitchLabel_var, font=("Helvetica", 12))
pitchLabel.grid(rowspan=2, row=4, column=0, sticky=EW)
pitchEntry = Entry(theUI, bd=3, font=("Helvetica", 12))
pitchEntry.grid(rowspan=2, row=4, column=1, sticky=EW)

# Label
distanceLabel_var = IntVar()
distanceLabel_var.set("Distance: ")
distanceLabel = Label(theUI, textvariable=distanceLabel_var, font=("Helvetica", 12))
distanceLabel.grid(rowspan=2, row=6, column=0, sticky=EW)
distanceEntry = Entry(theUI, bd=3, font=("Helvetica", 12))
distanceEntry.grid(rowspan=2, row=6, column=1, sticky=EW)

goButton = Button(theUI, text="Go!", command=lambda:
fixedDistance(), font=("Helvetica", 12))

forwardButton = Button(theUI,
                       text="--->", font=("Helvetica", 12))
# backwardButton = Button(theUI,
#                       text="<---",
#                       command=lambda:
#			backward_call(int(distanceEntry.get())))
backwardButton = Button(theUI,
                        text="<---", font=("Helvetica", 12))
# theUI.bind("<backwardButton>",backward_call(10))
var1 = 1
var0 = 0
dist = distanceEntry.get()
backwardButton.bind('<Button-1>', lambda event, arg=var1: checkval(event, var1))
backwardButton.bind('<ButtonRelease-1>', lambda event, arg=var0: checkval(event, var0))
goButton.grid(rowspan=2, columnspan=2, row=8, column=0, sticky=EW + NS)
forwardButton.grid(rowspan=2, columnspan=2, row=10, column=0, sticky=EW + NS)
backwardButton.grid(rowspan=2, columnspan=2, row=12, column=0, sticky=EW + NS)

theUI.grid_columnconfigure(0, weight=1)
theUI.grid_columnconfigure(1, weight=1)
theUI.grid_rowconfigure(0, weight=1)
theUI.grid_rowconfigure(1, weight=1)
theUI.grid_rowconfigure(2, weight=1)
theUI.grid_rowconfigure(3, weight=1)
theUI.grid_rowconfigure(4, weight=1)
theUI.grid_rowconfigure(5, weight=1)
theUI.grid_rowconfigure(6, weight=1)
theUI.grid_rowconfigure(7, weight=1)
theUI.grid_rowconfigure(8, weight=1)
theUI.grid_rowconfigure(9, weight=1)
theUI.grid_rowconfigure(10, weight=1)
theUI.grid_rowconfigure(11, weight=1)
theUI.grid_rowconfigure(12, weight=1)
theUI.grid_rowconfigure(13, weight=1)
# theUI.grid_rowconfigure(14, weight=1)

theUI.mainloop()
