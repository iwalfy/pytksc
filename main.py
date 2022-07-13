#!/usr/bin/env python3
import os
import platform
import threading
import tkinter
from tkinter import *
from PIL import Image, ImageTk

_rundir = os.path.dirname(os.path.realpath(__file__))

_platform = platform.system()
if _platform == "Linux":
    _adb_path = _rundir + "/adb/adb"
elif _platform == "Windows":
    _adb_path = _rundir + "/adb/adb.exe"
elif _platform == "Darwin":
    _adb_path = _rundir + "/adb/adb-darwin"

root = Tk()
root.title("pytksc")

resize_coof = 2

def click(event):
    x = event.x * resize_coof
    y = event.y * resize_coof
    os.system(_adb_path + " shell input tap " + str(x) + " " + str(y))

def sendButton(key):
    os.system(_adb_path + " shell input keyevent " + key)

def resize(i):
    listOfGlobals = globals()
    listOfGlobals['resize_coof'] = i

def screenUpdater():
    while True:
        os.system(_adb_path + " exec-out screencap -p > " + _rundir + "/screen.png")
        _screen = Image.open(_rundir + "/screen.png")
        _width, _height = _screen.size

        _new_width = _width // resize_coof
        _new_height = _height // resize_coof
        _screen = _screen.resize((_new_width, _new_height), Image.Resampling.LANCZOS)
        root.geometry(str(_new_width) + "x" + str(_new_height))

        _image = ImageTk.PhotoImage(_screen)
        label1 = tkinter.Label(image = _image)
        label1.image = _image
        label1.place(x = 0, y = 0)

def main():
    updaterThread = threading.Thread(target=screenUpdater)
    updaterThread.start()

    menubar = Menu(root)
    buttonmenu = Menu(menubar, tearoff=0)
    buttonmenu.add_command(label = "Back", command= lambda: sendButton("4"))
    buttonmenu.add_command(label = "Home", command= lambda: sendButton("3"))
    buttonmenu.add_command(label = "Menu", command= lambda: sendButton("1"))
    buttonmenu.add_command(label = "Recent", command= lambda: sendButton("187"))
    menubar.add_cascade(label="Button", menu=buttonmenu)

    resizemenu = Menu(menubar, tearoff=0)
    resizemenu.add_command(label = "1x", command= lambda: resize(1))
    resizemenu.add_command(label = "2x", command= lambda: resize(2))
    resizemenu.add_command(label = "3x", command= lambda: resize(3))
    resizemenu.add_command(label = "4x", command= lambda: resize(4))
    menubar.add_cascade(label="Resize", menu=resizemenu)

    root.config(menu=menubar)
    root.bind("<Button-1>", click)
    root.mainloop()

if __name__ == "__main__":
    main()
