import ast
import datetime
import os
import time

from Crypto.PublicKey import RSA

MACHINEID = "1"
mPath = "/home/project/.linuxCNC/"


def is_license_valid():
    rem = get_remaining_time()
    if rem:
        if rem == "Unlimited":
            return True
        if rem >= 0:
            return True
    return False


def get_remaining_time():
    keyFile = open(mPath + "ENCRYPT.PEM", "r")
    key = keyFile.read()
    keyFile.close()
    mKey = RSA.importKey(key)
    try:
        os.stat(mPath + "license.info")
    except:
        return False
    licFile = open(mPath + "license.info", "r")
    try:
        mLicense = mKey.decrypt(ast.literal_eval(str(licFile.read())))
        licFile.close()
        ts = time.time()
        st = str(datetime.datetime.fromtimestamp(ts)).split(" ")[0]
        mLicense = mLicense.split("\n")
        vLicense = mLicense[0].split("-")
        flag = True
        if mLicense[1] != MACHINEID:
            flag = False
        for v in vLicense:
            if not (v.isdigit() or v == "permanent"):
                flag = False
        if flag:
            if mLicense[0] == "permanent":
                return "Unlimited"
            y = int(vLicense[0])
            m = int(vLicense[1])
            d = int(vLicense[2])
            vDate = st.split("-")
            y1 = int(vDate[0])
            m1 = int(vDate[1])
            d1 = int(vDate[2])
            date1 = datetime.date(y, m, d)
            date2 = datetime.date(y1, m1, d1)
            return int(str(date1 - date2).split(" ")[0])
    except:
        return False


print
get_remaining_time()
print
is_license_valid()
