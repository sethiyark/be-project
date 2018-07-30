from CNC_Machine import myOtherFunction
from CNC_Machine import myOtherFunction1
import math
import time
import datetime
# import HaIndusIOcard
class kinematics:
    def __init__(self):
        self.thePitch = 5
        self.pulse_per_rotation = 2000
        self.endDistance = 500
        self.curDistance = 0
        self.theFrequency = 0
        self.pulses_per_mm = self.pulse_per_rotation / self.thePitch
        self.isForward = -1
        self.distancetoTravel = 0
        self.per_pulse_distance=float(1)/400
        self.acceleration = 500
        self.theVelocity = 80
        self.total_pulses=0
    	# self.obj=HaIndusIOcard.Parallel_ports()
    	
    def printval(self,DELAY):
        print("delay",DELAY)
        
    def onoff(self,cur):
       	self.obj.setPin(4)
    	time.sleep(cur)
    	self.obj.clearPin(4)
    	time.sleep(cur)
    	   
        
    def calculateDelay(self,initialVelocity,acceleration,pulses,totaldist):
        delay=0
        fdelay=0
        cdelay=time.time()
        while(initialVelocity<self.theVelocity and self.curDistance<=(totaldist/2)):
            finalVelocity,delay=myOtherFunction(initialVelocity)
            fdelay+=delay
            cur = (delay - (time.time() - cdelay)) / 2
            self.onoff(cur)
            #self.printval(cur)
            cdelay=time.time()
            pulses-=1
            #sleep fncn
            initialVelocity=finalVelocity
            self.curDistance += self.per_pulse_distance
            # self.printval(delay)
        print "after increasing:",pulses
    
        if(initialVelocity>=self.theVelocity):
            twotimesdist=0
            while(self.curDistance<=totaldist/2):
                #finalVelocity,delay=myOtherFunction(initialVelocity)
                cur = (delay - (time.time() - cdelay)) / 2
                #call delay
                
                self.onoff(cur)
                #self.printval(cur)
                cdelay = time.time()
                pulses -= 1
                self.curDistance += self.per_pulse_distance
                twotimesdist+=1
            while(twotimesdist>=0):
                #finalVelocity,delay=myOtherFunction(initialVelocity)
                cur = (delay - (time.time() - cdelay)) / 2
                #call delay
                
                self.onoff(cur)
                # self.printval(cur)
                cdelay = time.time()
                pulses -= 1
                self.curDistance += self.per_pulse_distance
                twotimesdist -= 1
        print "steady mode:",pulses
        if(self.curDistance<totaldist):
            while(pulses>0):
                finalVelocity,delay=myOtherFunction1(initialVelocity)
                fdelay+=delay
                cur = (delay - (time.time() - cdelay)) / 2
                
                self.onoff(cur)
                # self.printval(cur)
                cdelay=time.time()
                pulses-=1
                #sleep fncn
                initialVelocity=finalVelocity
                self.curDistance += self.per_pulse_distance
        print "after decreasing:",pulses
        print("Final distance:",self.curDistance)
        print("Delay addition:",fdelay)
    def goforward(self,dist, direc):
        if (dist <= self.endDistance):
            self.distancetoTravel = dist
            self.total_pulses=dist*self.pulses_per_mm
            a=datetime.datetime.now()
            #self.onoff()
            self.calculateDelay(0,self.acceleration,self.total_pulses,dist)
            b=datetime.datetime.now()
            print "time needed:",b-a
            return 1
        else:
            return 0
