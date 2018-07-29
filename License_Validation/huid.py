import hashlib
import os
import platform as p
import uuid

halFile = "/home/project/linuxcnc-master/configs/sim/axis/vismach/puma/puma560_sim_6.hal"


def get_fingerprint(md5=False):
    """
    Fingerprint of the current operating system/platform.
    If md5 is True, a digital fingerprint is returned.
    """
    dev_id = []
    dev_path = "/sys/bus/usb/devices"
    for dirs in (os.listdir(dev_path)):
        dev_path1 = dev_path + "/" + dirs
        for files in os.listdir(dev_path1):
            file_path = dev_path1 + "/" + files
            if files == "product":
                f = open(file_path, "r")
                dname = f.read()
                if dname[0:3] == "UDA":
                    vf = open(dev_path1 + "/idVendor", "r")
                    pf = open(dev_path1 + "/idProduct", "r")
                    dev_id.append(vf.read().rstrip('\n'))
                    dev_id.append(pf.read().rstrip('\n'))
                    vf.close()
                    pf.close()
                    dev_id.append(dname.rstrip('\n'))
                f.close()
    sb = [p.node(), p.architecture()[0], p.architecture()[1], p.machine(), p.processor(), p.system(),
          str(uuid.getnode())]
    text = '#'.join(dev_id)
    if md5:
        md5 = hashlib.md5()
        md5.update(text)
        return md5.hexdigest()
    else:
        return text


def getStatus():
    return True


hID = get_fingerprint(True)
print
hID

isValid = getStatus()

if isValid:
    exit()
else:
    exit()
