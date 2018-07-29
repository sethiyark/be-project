#!/usr/bin/python

import shutil

import tkMessageBox
from EncryptionKey import generate_checksum
from EncryptionKey import generate_key
from Tkinter import *


class LicenseInstall:
    def __init__(self, master):
        self.linux_cnc_path = "/usr"
        self.ui = master
        client_id_var = StringVar()
        client_id_var.set("Client ID: ")
        client_id_label = Label(master, textvariable=client_id_var)
        client_id_label.grid(row=0, column=0)
        self.client_id_entry = Entry(master, bd=3)
        self.client_id_entry.grid(row=0, column=1)
        self.client_id_entry.focus()

        install_button = Button(master, text="Install", command=lambda: self.install_call())
        install_button.grid(columnspan=2, row=2, column=0, sticky=EW)

    def install_call(self):
        if self.linux_cnc_path != "":
            try:
                if self.client_id_entry.get() == "":
                    tkMessageBox.showerror("Alert", "Enter Client ID...")
                    return
            except:
                tkMessageBox.showwarning("Something Wrong...")
                self.client_id_entry.delete(0, 'end')
                return
            self.linux_cnc_path = self.linux_cnc_path.rstrip("/")
            try:
                shutil.copyfile("patch/1", self.linux_cnc_path + "/bin/axis")
                shutil.copyfile("patch/2", self.linux_cnc_path + "/share/axis/tcl/axis.tcl")
            except:
                tkMessageBox.showerror("Error", "Run as superuser!!!")
                return
        response = generate_key(self.client_id_entry.get())
        if not response:
            tkMessageBox.showerror("Error", "Can't reach server")
            return
        generate_checksum(self.linux_cnc_path)
        tkMessageBox.showinfo("Done", "Installation Complete")
        self.ui.quit()
        return


def main():
    root = Tk()
    LicenseInstall(root)
    root.pack_slaves()
    root.mainloop()


if __name__ == "__main__":
    main()
