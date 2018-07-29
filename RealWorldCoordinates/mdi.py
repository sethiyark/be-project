import telnetlib
import time


class MDI:
    def __init__(self):
        self.tn = None

    def initialize(self, host):
        self.tn = telnetlib.Telnet(host, "5007")


# user = raw_input("Enter your remote account: ")
# password = getpass.getpass()

'''
# tn.read_until("login: ")
tn.write(user + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")
'''


def telnet_connect(tnet):
    tnet.initialize("127.0.0.1")
    tnet.tn.write("hello EMC user-typing-at-telnet 1.0\n")
    tnet.tn.write("set enable EMCTOO\n")
    tnet.tn.write("set estop off\n")
    tnet.tn.write("set machine on\n")
    # Home according to available joints

    tnet.tn.write("set home 0\n")
    tnet.tn.write("set home 1\n")
    tnet.tn.write("set home 2\n")
    tnet.tn.write("set home 3\n")
    tnet.tn.write("set home 4\n")
    tnet.tn.write("set home 5\n")
    time.sleep(10)
    tnet.tn.write("set mode mdi\n")


def go(tnet, x=0, y=0, z=0):
    # comm7="set mdi g0x"+str(entry2.get())
    # Move by G code
    x_var = " x" + str(int(x))
    y_var = " y" + str(int(y))
    z_var = " z" + str(int(z))
    tnet.tn.write("set mdi g0" + x_var + y_var + z_var + "\n")
    time.sleep(1)


'''
def reset_values():
    entry2.setvar("e2", "")
    entry3.setvar("e3", "")
    entry4.setvar("e4", "")

root = Tk()
# Setting screen size as full-screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry('%dx%d' % (screen_width, screen_height))

# All labels in GUI
label1 = Label(root, text="IP address", width=30, height=5, font=("Ariel", 15))
label2 = Label(root, text="X co-ordinate", width=30, height=5, font=("Ariel", 15))
label3 = Label(root, text="Y co-ordinate", width=30, height=5, font=("Ariel", 15))
label4 = Label(root, text="Z co-ordinate", width=30, height=5, font=("Ariel", 15))

# All text-entry fields in GUI
entry1 = Entry(root)
entry2 = Entry(root)
entry3 = Entry(root)
entry4 = Entry(root)

# All buttons in GUI
button1 = Button(root, text='Connect', width=25, command=lambda: telnet_connect(tnet), font=("Ariel", 15))
button2 = Button(root, text='Go!', width=25, command=lambda: go(tnet), font=("Ariel", 15))
button3 = Button(root, text='Reset Values', width=25, command=reset_values, font=("Ariel", 15))
# button3 = Button(root, text='Exit', width=25, command=root.destroy, font=("Ariel", 15))

# Setting positions of all elements
label1.grid(row=0)
label2.grid(row=1)
label3.grid(row=2)
label4.grid(row=3)

entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)
entry3.grid(row=2, column=1)
entry4.grid(row=3, column=1)

button1.grid(row=0, column=3)
button2.grid(row=4, column=1)
button3.grid(row=5, column=1)

entry1.setvar("e1", "127.0.0.1")

# root.geometry("1000x500")
root.mainloop()
'''
