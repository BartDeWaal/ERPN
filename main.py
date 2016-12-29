#!/usr/bin/env python3

import curses
import functions
import curseshelper

stack = []

class Interface:
    functions = {}
    entryBox = None # replace with a curses box for text entry

    def add(self, key, function):
        self.functions[key] = function

    def run(self, key):
        if type(key) is int:
            key = chr(key)
        if key in '1234567890 .':
            self.entry(key)
        if key in self.functions:
            try:
                self.functions[key].run(stack)
            except functions.StackToSmallError:
                pass

    def entry(self, key):
        self.entryBox.refresh()
        self.entryBox.addstr(0,0,key)
        self.entryBox.refresh()
        with curseshelper.EchoOn():
            string = key + self.entryBox.getstr(0,1).decode('utf-8')
        try:
            val = float(string)
            stack.append(val)
        except ValueError:
            pass
        self.entryBox.clear()
        self.entryBox.refresh()


interface = Interface()
interface.add('+', functions.addition)
interface.add('a', functions.addition)
interface.add('x', functions.delete)
interface.add('m', functions.multiply)
interface.add('s', functions.subtract)

def main(screen):
    screen.clear()
    helpWindow = curses.newwin(curses.LINES-3, 20, 0, curses.COLS-21)
    stackWindow = curses.newwin(curses.LINES-3, curses.COLS-21, 0, 0)
    interface.entryBox = curses.newwin(1, curses.COLS-1, curses.LINES-2, 0)

    curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
    screen.refresh()
    displayStack(stackWindow)
    c = screen.getch()
    while c != ord('q'):
        interface.run(c)
        displayStack(stackWindow)
        c = screen.getch()


def displayStack(window):
    window.clear()
    for line, num in zip(stack, range(len(stack),0,-1)):
        window.addstr("{}: {}\n".format(num, line))
    window.refresh()


curses.wrapper(main)
