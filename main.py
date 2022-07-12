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

# EDIT HERE
RESIZE_COOF = 4
# EDIT HERE

def click(event):
    x = event.x * RESIZE_COOF
    y = event.y * RESIZE_COOF
    os.system(_adb_path + " shell input tap " + str(x) + " " + str(y))

def screenUpdater():
    while True:
        os.system(_adb_path + " exec-out screencap -p > " + _rundir + "/screen.png")
        _screen = Image.open(_rundir + "/screen.png")
        _width, _height = _screen.size

        _new_width = _width // RESIZE_COOF
        _new_height = _height // RESIZE_COOF
        _screen = _screen.resize((_new_width, _new_height), Image.Resampling.LANCZOS)
        root.geometry(str(_new_width) + "x" + str(_new_height))

        _image = ImageTk.PhotoImage(_screen)
        label1 = tkinter.Label(image = _image)
        label1.image = _image
        label1.place(x = 0, y = 0)

def main():
    updaterThread = threading.Thread(target=screenUpdater)
    updaterThread.start()
    root.bind("<Button-1>", click)
    root.mainloop()

if __name__ == "__main__":
    main()
