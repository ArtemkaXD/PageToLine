from tkinter import *
from tkinter import filedialog
import shifter as sh
import configparser
from icon import *
import base64
import os


INI = 'maps.ini'

config = configparser.ConfigParser()
if not(config.read(INI)):
    with open(INI,'w') as f:
        f.write('[DEFAULT]\ndef_root = C:/\n\n[NewMCU]')
    config.read(INI)


root = Tk()

with open("temp.ico","wb+") as tmp:
    tmp.write(base64.b64decode(img))
root.iconbitmap("temp.ico")
os.remove("temp.ico")

root.geometry('320x240')
root.resizable(0, 0)
root.title('PageToLine')


def filesel(conf, mcu, ftype, frame):
    frame.filename = filedialog.askopenfilename(initialdir=conf['DEFAULT']['def_root'],
                                                title="Select file",
                                                filetypes=(("SREC", ".s2 .s19"),
                                                           ("Binary", ".bin"),
                                                           ("All", "*.*")))
    if not frame.filename:
        return -1

    droot = frame.filename

    if droot.partition('.')[2][:1] == 'b':
        f = sh.bin_open(droot)
    elif droot.partition('.')[2][:1] == 's':
        f = sh.srec_open(droot)

    f = sh.rerange(mcu, f, conf)
    sh.bin_save(droot, ftype, f)

    droot = droot[::-1].partition('/')[2][::-1]
    conf['DEFAULT']['def_root'] = droot
    with open(INI, 'w') as configfile:
        conf.write(configfile)

    return 0


f_left = Frame(root)
f_right = Frame(root)
f_list = Frame(f_right)
f_out = LabelFrame(f_left, text='Output file type')


outtype = StringVar(root, ".s19")

mcuLabel = Label(f_right, text='Select MCU from list ',
                 font="Arial 10", width=16)

selBut = Button(f_left, text="Select file", width=9, height=1,
                font="Arial 11",
                command=lambda: filesel(config, mcuBox.get(mcuBox.curselection()),
                                        outtype.get(), root))

Radiobutton(f_out, text='S19', variable=outtype,
            value='.s19').pack(side=TOP)
Radiobutton(f_out, text='BIN', variable=outtype,
            value='.bin').pack(side=TOP, ipady=5)


mculist = config.sections()
mcuBox = Listbox(f_list, selectmode=SINGLE, height=11, bd=3,
                 activestyle='none')
for i in mculist:
    mcuBox.insert(END, i)
mcuBox.select_set(0)

scrollBar = Scrollbar(f_list, command=mcuBox.yview)
mcuBox.configure(yscrollcommand=scrollBar.set)

f_right.pack(side=RIGHT, padx=16)
f_left.pack(side=RIGHT, padx=16, pady=36)

selBut.pack(pady=16)
f_out.pack(pady=16)

mcuLabel.pack()
f_list.pack()
scrollBar.pack(side=RIGHT, fill=Y)
mcuBox.pack(side=RIGHT)

root.mainloop()
