#!/usr/bin/env python3

import curses
from collections import defaultdict

import functions
import curseshelper

stack = []
undostack = []


class Interface:
    functions = {}
    entryBox = None  # Replace with a curses box for text entry

    def add(self, key, function):
        self.functions[key] = function

    def run(self, key):
        if type(key) is int:
            key = chr(key)
        if key in '1234567890 .':
            self.entry(key)
        if key in self.functions:
            try:
                self.functions[key].run(stack, undostack)
            except functions.StackToSmallError:
                pass
            except functions.IsUndo:
                undostack.pop().apply(stack)
            except functions.IsQuit:
                exit()

    def entry(self, key):
        self.entryBox.refresh()
        self.entryBox.addstr(0, 0, key)
        self.entryBox.refresh()

        with curseshelper.EchoOn():
            string = key + self.entryBox.getstr(0, 1).decode('utf-8')

        try:
            val = float(string)
            stack.append(val)
            undostack.append(functions.UndoItem(1, []))
        except ValueError:
            pass

        self.entryBox.clear()
        self.entryBox.refresh()

    def helptext(self):
        items = defaultdict(lambda: [])
        for item in self.functions:
            items[self.functions[item]].append(item)

        returnstring = ""
        for item in items:
            returnstring += "{}: {}\n".format(
                    ', '.join(sorted(items[item])),
                    item.description)
        returnstring += "q: quit\n"
        return returnstring


interface = Interface()
interface.add('+', functions.addition)
interface.add('a', functions.addition)
interface.add('x', functions.delete)
interface.add('m', functions.multiply)
interface.add('*', functions.multiply)
interface.add('s', functions.subtract)
interface.add('-', functions.subtract)
interface.add('d', functions.divide)
interface.add('/', functions.divide)
interface.add('u', functions.undo)


def main(screen):
    screen.clear()
    helpWindow = curses.newwin(curses.LINES-3, 20, 0, curses.COLS-21)
    stackWindow = curses.newwin(curses.LINES-3, curses.COLS-21, 0, 0)
    interface.entryBox = curses.newwin(1, curses.COLS-1, curses.LINES-2, 0)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    screen.refresh()
    displayStack(stackWindow)
    displayHelp(helpWindow)
    c = screen.getch()
    while c != ord('q'):
        interface.run(c)
        displayStack(stackWindow)
        c = screen.getch()


def displayStack(window):
    window.clear()
    for line, num in zip(stack, range(len(stack), 0, -1)):
        window.addstr("{}: {}\n".format(num, line))
    window.refresh()


def displayHelp(window):
    window.clear()
    window.addstr(0, 0, interface.helptext())
    window.refresh()


curses.wrapper(main)
