#!/usr/bin/env python3

from tkinter import Tk
from twisted.internet import reactor, tksupport

import gui

if __name__ == '__main__':
    root = Tk()
    tksupport.install(root)
    gui.App(root)

    reactor.run()
