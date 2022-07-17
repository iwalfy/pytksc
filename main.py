#!/usr/bin/env python3
import os
import sys
import platform
import threading
import tkinter
from tkinter import *
from tkinter import simpledialog
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

use_alt_method = False
if len(sys.argv) >= 2 and sys.argv[1] == "--alternative":
    use_alt_method = True

def click(event):
    x = event.x * resize_coof
    y = event.y * resize_coof
    os.system(_adb_path + " shell input tap " + str(x) + " " + str(y))

def sendButton(key):
    os.system(_adb_path + " shell input keyevent " + key)

def customButton():
    key = simpledialog.askstring(title="pytksc", prompt="Enter eventkey id:")
    os.system(_adb_path + " shell input keyevent " + key)

def sendText():
    text = simpledialog.askstring(title="pytksc", prompt="Enter text to send:")
    os.system(_adb_path + " shell input text " + text)

def resize(i):
    listOfGlobals = globals()
    listOfGlobals['resize_coof'] = i

def swipe(i):
    _screen = Image.open(_rundir + "/screen.png")
    _width, _height = _screen.size

    _new_width = (_width // resize_coof) * resize_coof
    _new_height = (_height // resize_coof) * resize_coof

    _center_y = _new_height // 2
    _center_x = _new_width // 2

    _width4 = _new_width // 4
    _height3 = _new_height // 3

    if i == 1:
        _x1 = 0 + _width4
        _x2 = _new_width - _width4
        _y1 = _center_y
        _y2 = _center_y
    
    if i == 2:
        _x1 = _new_width - _width4
        _x2 = _width4
        _y1 = _center_y
        _y2 = _center_y
    
    if i == 3:
        _x1 = _center_x
        _x2 = _center_x
        _y1 = _new_height - _height3
        _y2 = _height3
    
    if i == 4:
        _x1 = _center_x
        _x2 = _center_x
        _y1 = _height3
        _y2 = _new_height - _height3

    if i == 5:
        _x1 = 10
        _x2 = 10
        _y1 = 0
        _y2 = _center_y
    
    if i == 6:
        _x1 = _new_width - 10
        _x2 = _new_width - 10
        _y1 = 0
        _y2 = _center_y
    
    os.system(_adb_path + " shell input swipe " + str(_x1) + " " + str(_y1) + " " + str(_x2) + " " + str(_y2) + " 500")

def screenUpdater():
    while True:
        if use_alt_method:
            os.system(_adb_path + " shell screencap -p /sdcard/screen.png")
            os.system(_adb_path + " pull /sdcard/screen.png " + _rundir + "/screen.png")
        else:
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
    os.system(_adb_path + " kill-server")
    os.system(_adb_path + " devices")

    input("Check your device then press Enter...")

    updaterThread = threading.Thread(target=screenUpdater)
    updaterThread.start()

    menubar = Menu(root)
    buttonmenu = Menu(menubar, tearoff=0)
    buttonmenu.add_command(label = "Back", command= lambda: sendButton("4"))
    buttonmenu.add_command(label = "Home", command= lambda: sendButton("3"))
    buttonmenu.add_command(label = "Menu", command= lambda: sendButton("1"))
    buttonmenu.add_command(label = "Recent", command= lambda: sendButton("187"))
    buttonmenu.add_separator()
    buttonmenu.add_command(label = "Unlock", command= lambda: sendButton("82"))
    buttonmenu.add_command(label = "Custom", command= lambda: customButton())
    buttonmenu.add_separator()
    buttonmenu.add_command(label = "String input", command= lambda: sendText())
    menubar.add_cascade(label="Button", menu=buttonmenu)

    swipemenu = Menu(menubar, tearoff=0)
    swipemenu.add_command(label = "Center Left -> Center Right", command= lambda: swipe(1))
    swipemenu.add_command(label = "Center Right -> Center Left", command= lambda: swipe(2))
    swipemenu.add_command(label = "Center Down -> Center Up", command= lambda: swipe(3))
    swipemenu.add_command(label = "Center Up -> Center Down", command= lambda: swipe(4))
    swipemenu.add_command(label = "Left Up -> Left Center (Notifications)", command= lambda: swipe(5))
    swipemenu.add_command(label = "Right Up -> Right Center (Notifications)", command= lambda: swipe(6))
    menubar.add_cascade(label="Swipe", menu=swipemenu)

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
