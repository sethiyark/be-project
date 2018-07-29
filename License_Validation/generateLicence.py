#!/usr/bin/python

import datetime
import ftplib
import importlib
import os
import time
import urllib

import tkMessageBox
import ttk

try:
    importlib.import_module("Crypto")
except ImportError:
    import pip

    pip.main(['install', "pycrypto"])
finally:
    globals()["RSA"] = importlib.import_module("Crypto.PublicKey.RSA")
from Tkinter import *


def send_license(client, license_path):
    try:
        session = ftplib.FTP('ftp.indusrobotics.com', 'keys@indusrobotics.com', 'IRkeys123$%')
        file = open(license_path, 'rb')  # file to send
        fname = "license" + client + ".info"
        session.storbinary('STOR ' + fname, file)  # send the file
        file.close()  # close file and FTP
        session.quit()
    except:
        return


def get_key(client):
    try:
        fname = client + ".PEM"
        urllib.urlretrieve("http://www.indusrobotics.com/keys/" + fname, "tmp.PEM")
        cKey = open("tmp.PEM", "r")
        key = cKey.read()
        cKey.close()
        try:
            mKey = RSA.importKey(key)
            return mKey
        except:
            return get_key(client)
    except:
        return False


class GenerateLicense:
    def __init__(self, master):
        self.rDay = 86400
        self.ui = master
        client_id_var = StringVar()
        client_id_var.set("Client ID: ")
        client_id_label = Label(master, textvariable=client_id_var)
        client_id_label.grid(row=0, column=0)
        self.client_id_entry = Entry(master, bd=3)
        self.client_id_entry.grid(row=0, column=1)
        self.client_id_entry.focus()
        box_var = StringVar()
        box_var.set("Validity: ")
        box_label = Label(master, textvariable=client_id_var)
        box_label.grid(row=0, column=0)
        self.box_value = StringVar()
        self.box = ttk.Combobox(master, textvariable=self.box_value)
        self.box['values'] = ('7', '10', '15', '20', '30', '60', '90', '180', '360', 'Lifetime')
        self.box.current(4)
        self.box.grid(row=1, column=1)
        generate_button = Button(master, text="Generate", command=lambda: self.generate_call())
        generate_button.grid(columnspan=2, row=2, column=0, sticky=EW)

    def generate_call(self):
        try:
            if self.client_id_entry.get() == "":
                tkMessageBox.showerror("Alert", "Enter Client ID...")
                return
        except:
            tkMessageBox.showwarning("Something Wrong...")
            self.client_id_entry.delete(0, 'end')
            return
        client_id = self.client_id_entry.get()
        m_key = get_key(client_id)
        try:
            ts = time.time()
            expiry = self.box.get()
            if expiry != 'Lifetime':
                ts += int(expiry) * self.rDay
                expiry = str(datetime.datetime.fromtimestamp(ts)).split(" ")[0]
            elif expiry == 'Lifetime':
                expiry = "permanent"
            license_path = "license.info"
            m_license = m_key.encrypt(expiry + "\n" + client_id, 32)
            license_file = open(license_path, "w")
            license_file.write(str(m_license))
            license_file.close()
        except:
            tkMessageBox.showerror("Error", "Key not received")
            return
        try:
            send_license(client_id, license_path)
            os.remove(license_path)
            os.remove("tmp.PEM")
        except:
            tkMessageBox.showerror("Error", "Failed Sending to Server")
        tkMessageBox.showinfo("Done", "License Generated")
        self.ui.quit()
        return


def main():
    root = Tk()
    GenerateLicense(root)
    root.pack_slaves()
    root.mainloop()


if __name__ == "__main__":
    main()
