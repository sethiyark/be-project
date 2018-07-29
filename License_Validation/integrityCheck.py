import hashlib
import os

kPath = os.path.expanduser("~")
kPath += "/.linuxCNC"
try:
    os.stat(kPath)
except:
    os.mkdir(kPath)
kPath += "/"

md5 = hashlib.md5()
linuxCNC_path = "/home/project/linuxcnc-master/"
with open(linuxCNC_path + "bin/axis", "r") as f:
    for chunk in f.readlines():
        md5.update(chunk)
with open(linuxCNC_path + "share/axis/tcl/axis.tcl", "r") as f:
    for chunk in f.readlines():
        md5.update(chunk)
with open(kPath + "machineID", "r") as f:
    for chunk in f.readlines():
        md5.update(chunk)
digest = md5.hexdigest()

checksum = open(kPath + "checksum", "r")
oDigest = checksum.read()
checksum.close()

if digest == oDigest:
    print
    "OK"
else:
    print
    "Tampered"
