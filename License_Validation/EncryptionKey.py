#!/usr/bin/python

import ftplib
import hashlib
import importlib
import os

try:
    importlib.import_module("Crypto")
except ImportError:
    import pip

    pip.main(['install', "pycrypto"])
finally:
    globals()["RSA"] = importlib.import_module("Crypto.PublicKey.RSA")
    globals()["Random"] = importlib.import_module("Crypto.Random")

kPath = "/home/" + os.getlogin() + "/.linuxCNC"
try:
    os.stat(kPath)
except:
    os.mkdir(kPath)
kPath += "/"


def generate_checksum(linuxCNC_path):
    md5 = hashlib.md5()
    with open(linuxCNC_path + "/bin/axis", "r") as f:
        for chunk in f.readlines():
            md5.update(chunk)
    with open(linuxCNC_path + "/share/axis/tcl/axis.tcl", "r") as f:
        for chunk in f.readlines():
            md5.update(chunk)
    with open(kPath + "/machineID", "r") as f:
        for chunk in f.readlines():
            md5.update(chunk)
    digest = md5.hexdigest()

    checksum = open(kPath + "/checksum", "w")
    checksum.write(digest)
    checksum.close()


def send_key(client, key_path):
    try:
        session = ftplib.FTP('ftp.indusrobotics.com', 'keys@indusrobotics.com', 'IRkeys123$%')
        file = open(key_path, 'rb')  # file to send
        fname = client + ".PEM"
        session.storbinary('STOR ' + fname, file)  # send the file
        file.close()  # close file and FTP
        session.quit()
        return True
    except:
        return False


def generate_key(cID):
    random_generator = Random.new().read
    eKey = RSA.generate(1024, random_generator)  # generate pub and priv key

    cKey = eKey.publickey()  # pub key export for exchange

    encKey = eKey.exportKey(format='DER')
    clientKey = cKey.exportKey(format='DER')

    mFile = open(kPath + "machineID", "w")
    mFile.write(cID)
    mFile.close()

    pPath = kPath + "ENCRYPT.PEM"
    cPath = cID + ".PEM"
    prv_file = open(pPath, "w")
    prv_file.write(encKey)
    prv_file.close()
    pub_file = open(cPath, "w")
    pub_file.write(clientKey)
    pub_file.close()

    response = send_key(cID, cPath)
    os.remove(cPath)
    return response

# generate_key("1")
