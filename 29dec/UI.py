from Tkinter import *
#from Tkinter import tkMessageBox
import test as mCNC

# #################################     Window     ##################################

theUI = Tk()
theUI.pack_slaves()


def forward_call(distance):
    val = mobj.goforward(distance, 1)
    print("val", val)


def backward_call(distance):
    val = mobj.gobackward(distance, 0)
    print("val", val)


# #################################  Distance I/P  ##################################

# Label
distanceLabel_var = StringVar()
distanceLabel_var.set("Distance: ")
distanceLabel = Label(theUI, textvariable=distanceLabel_var)
distanceLabel.grid(row=0, column=0)

# Entry
distanceEntry = Entry(theUI, bd=3)
distanceEntry.grid(row=0, column=1)

forwardButton = Button(theUI,
                       text="--->",
                       command=lambda:
                       forward_call(int(distanceEntry.get())))
backwardButton = Button(theUI,
                        text="<---",
                        command=lambda:
                        backward_call(int(distanceEntry.get())))
forwardButton.grid(columnspan=2, row=3, column=0, sticky=EW)
backwardButton.grid(columnspan=2, row=4, column=0, sticky=EW)
mobj = mCNC.kinematics()
theUI.mainloop()
