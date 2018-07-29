import datetime
import os
import time

for i in range(0, 1):
    fLog = open("event.log", "a")
    ts = time.time()
    tStamp = str(datetime.datetime.fromtimestamp(ts))
    fLog.write(tStamp + " Open LinuxCNC\n")
    fLog.close()

statinfo = os.stat("event.log")
size = int(statinfo.st_size)
if size > 10240000:
    cLog = open("event.log", "r")
    nLog = open("event.log.bk", "w")
    rLog = cLog.readlines()[2000:-1]
    for l in rLog:
        nLog.write(l)
    cLog.close()
    nLog.close()
    os.remove("event.log")
    os.rename("event.log.bk", "event.log")
