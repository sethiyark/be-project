#!/usr/bin/env python
# 
#
# This example creates a test panel
# using a led custom widget
#
# 

import gtk
import gobject
import cairo
import math
import hal

# this creates the HAL component
# you could also create the pins here if you 
# know before hand what you need

class hal_interface:
    def __init__(self):   
        self.c = hal.component("testpanel")      

# This holds the data for widgets
class Data:
    def __init__(self):
        self.inv = []
        self.swch =[]
        self.led = []
    def __getitem__(self, item):
        return getattr(self, item)
    def __setitem__(self, item, value):
        return setattr(self, item, value)

# This creates the custom LED widget
class LED(gtk.DrawingArea):

    def __init__(self, parent):
        self.par = parent       
        super(LED, self).__init__() 
        self._dia = 10
        self._state = 0
        self._on_color = [0.3, 0.4, 0.6]
        self._off_color = [0.9, 0.1, 0.1]
        self.set_size_request(25, 25)
        self.connect("expose-event", self.expose)
        

    # This method draws our widget
    # it draws a black circle for a rim around LED
    # Then depending on self.state
    # fills in that circle with on or off colour.
    # the diameter depends on self.dia
    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        cr.set_line_width(3)
        cr.set_source_rgb(0, 0, 0.0)    
        self.set_size_request(self._dia*2+5, self._dia*2+5)           
        w = self.allocation.width
        h = self.allocation.height
        cr.translate(w/2, h/2)
        cr.arc(0, 0, self._dia, 0, 2*math.pi)
        cr.stroke_preserve()
        if self._state:
            cr.set_source_rgb(self._on_color[0],self._on_color[1],self._on_color[2])
        else:
            cr.set_source_rgb(self._off_color[0],self._off_color[1],self._off_color[2])
        cr.fill()
        
        return False
      
    # This sets the LED on or off
    # and then redraws it
    # Usage: ledname.set_active(True) 
    def set_active(self, data ):
        self._state = data
        self.queue_draw()
    
    # This allows setting of the on and off colour
    # red,green and blue are float numbers beteen 0 and 1
    # Usage: ledname.set_color("off",[r,g,b])

    def set_color(self, state, color = [0,0,0] ):
        if state == "off":
            self._off_color = color
        elif state == "on":
            self._on_color = color
        else:
            return
    # This alows setting the diameter of the LED
    # Usage: ledname.set_dia(10)
    def set_dia(self, dia):
        self._dia = dia
        self.queue_draw()
 
class PyApp(gtk.Window): 

    # This is a general call back that sets the HAL output pins
    # according to the button and ivert pin
    # if the inverse widget calls then we force the button to 
    # update again
    def callback(self, widget, component , number, data=None):   
        print component,number,data
        if component == "switch":
            invrt = self.data["inv%d" % (number)].get_active()
            if (data and not invrt ) or (not data and invrt):
                self.hal.c["switch-%d"% number] = True
            else:
                self.hal.c["switch-%d"% number] = False
        if component == "invert":
            self.callback(None,"switch",number,False)

    # We must kill the HAL component before closing 
    def quit(self,widget):
        self.hal.c.exit()
        gtk.main_quit()

    # This updates the LED HAL pins 
    # Gobject_timeout points here
    def update(self):
        for i in (0,24,48):
            for j in range(0,12):
                self.data["led%d"%(i+j)].set_active(self.hal.c["led-%d"% (i+j)])      
        return True # keep running this event
    
    # This is for placing an LED and label into a specified 
    # container. It also creates a HAL pin and sets new On and Off
    # colours. 
    def make_led(self,container,number):
        ledname = "led-%d" % (number)
        self.hal.c.newpin(ledname, hal.HAL_BIT, hal.HAL_IN)
        self.data["led%d" % (number)] = LED(self)
        self.data["led%d" % (number)].set_color("off",[1,0,0]) # red
        self.data["led%d" % (number)].set_color("on",[1,1,0]) # Yellow
        container.pack_start(self.data["led%d"% (number)], False, False, 10)
        label = gtk.Label("<--GPIO-%d"% (number))
        container.pack_start(label, False, False, 10)

    # This is for placing a switch and an invert check box into
    # a specified container. It also creates the HAL pin
    # and connects some signals. 
    def make_switch(self,container,number):
        # add button to container using number as a reference
        switchname = "switch-%d" % number
        self.data["swch%d" % (number)]= gtk.Button("OUT-%d"% number)
        container.pack_start(self.data["swch%d"% (number)], False, False, 10)
        # connect signals
        self.data["swch%d" % (number)].connect("pressed", self.callback, "switch",number,True)
        self.data["swch%d" % (number)].connect("released", self.callback, "switch",number,False)
        # make a HAL pin
        self.hal.c.newpin(switchname, hal.HAL_BIT, hal.HAL_OUT)
        # add invert switch
        self.data["inv%d" % (number)]= gtk.CheckButton("Invert")
        container.pack_start(self.data["inv%d"% (number)], False, False, 10) 
        self.data["inv%d" % (number)].connect("toggled", self.callback, "invert",number,None)      

    # This is the main loop to display what we have done
    # We build a window with notebook pages and popuate them
    # with LEDs and switches
    # connect the signals and gobject timer to update the HAL pins
    # and tell HAl we are finished with self.Hal.c.ready()
    def __init__(self):
        super(PyApp, self).__init__()
        self.data = Data()
        self.hal = hal_interface()
        self.set_title("Test Panel")
        self.set_size_request(350, 400)        
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", self.quit)
        gobject.timeout_add(100, self.update)
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        notebook.show()
        self.add(notebook)       
        for con in (0,24,48):    
            table = gtk.Table(12, 3, False)
            seperator = gtk.VSeparator()
            table.attach(seperator, 1, 2, 0, 12,True)
            for i in range(0,12):
                h = gtk.HBox(False,2)
                self.make_led(h,con+i)
                table.attach(h, 0, 1, i, i+1,True)
                h = gtk.HBox(False,2)
                self.make_switch(h,con+i+12)
                table.attach(h, 2, 3, i, i+1)
            label = gtk.Label("Connector %d"% (con/24))      
            notebook.append_page(table, label)               
        self.show_all()       
        self.hal.c.ready()
PyApp()
gtk.main()

