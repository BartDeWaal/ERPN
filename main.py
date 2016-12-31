#!/usr/bin/env python3
# CRPN, a Curses based RPN calculator
# Copyright (C) 2016 Bart de Waal
# This program is licenced under the GPL version three, see Licence file for details

import curses
from collections import defaultdict

import functions
import utils.curseshelper as curseshelper

stack = []  # The stack as displayed to the unit
undostack = []  # The stack of undo actions


class Interface:
    functions = {}
    entryBox = None      # Replace with a curses box for text entry
    stackWindow = None
    helpWindow = None
    mainScreen = None

    def add(self, key, function):
        """ Add a entry to link a keyboard shortcut to a function """
        if key in self.functions:
            # You probably don't want to overwrite everything
            raise Exception("Already defined key {}".format(key))
        self.functions[key] = function

    def run(self, key):
        """ React to a pressed key """

        if key in '1234567890 ._':
            # if this is a number or starts with a space we want to
            # let the user enter the whole line
            self.entry(key)

        if key in self.functions:
            try:
                # This function uses exceptions to communicate if something is
                # not a simple function on the stack
                self.functions[key].run(stack, undostack)

            except functions.StackToSmallError:
                displayError(self.stackWindow, "Stack too small")
                return  # do not re-display

            except functions.DomainError as e:
                displayError(self.stackWindow, str(e))
                return  # do not re-display

            except OverflowError:
                displayError(self.stackWindow, "Value too large")
                return  # do not re-display

            except functions.IsUndo:
                # Take the top action from the undostack and apply it to the
                # stack
                if len(undostack) > 0:
                    undostack.pop().apply(stack)
                else:
                    displayError(self.stackWindow, "Nothing to undo")

            except functions.IsCopyFromStack:
                c = self.getKey()
                try:
                    addToStack(stack[lineLabelLookup(c)])
                except:
                    displayError(self.stackWindow, "Could not lookup value")
                    return  # keep showing error

            except functions.IsQuit:
                exit()

        displayStack(self.stackWindow)

    def entry(self, key):
        """ Let the user enter a line, mainly for entering new numbers """
        val, nextkey = curseshelper.getEntry(self.entryBox, key)
        try:
            val = float(val)
            addToStack(val)
            displayStack(self.stackWindow)
            self.run(nextkey)
        except ValueError:
            displayError(self.stackWindow, "Could not decode value")

    def helptext(self):
        """ Generate the string for the help text in the sidebar.
        The information in generated from the configuration """

        # All items in the dicts are [] by default, so we can append to them
        # without checking if they exist
        items = defaultdict(lambda: [])
        # The keys in this dict will be the functions they are linked to.

        for item in self.functions:
            items[self.functions[item]].append(item)

        returnstrings = []
        for item in items:
            returnstrings.append(
                    "{}: {}".format(', '.join(sorted(items[item])),
                                    item.description))
        returnstrings.sort()
        return "\n".join(returnstrings)

    def getKey(self):
        """ Allow the interface to define how keys are recieved """
        return curseshelper.getKeyAlt(self.mainScreen)


interface = Interface()
# See utils folder for script that helps figure out what each key does
interface.add('x', functions.delete)
interface.add('z', functions.switch2)
interface.add('+', functions.addition)
interface.add('a', functions.addition)
interface.add('s', functions.subtract)
interface.add('-', functions.subtract)
interface.add('m', functions.multiply)
interface.add('*', functions.multiply)
interface.add('d', functions.divide)
interface.add('/', functions.divide)
interface.add('p', functions.exponent)
interface.add('q', functions.square)
interface.add('S', functions.sqrt)
interface.add('E', functions.power_e)
interface.add('e', functions.power_10)  # Should be bound to e for compatability with "1e3" notation
interface.add('L', functions.log10)
interface.add('l', functions.ln)
interface.add('I', functions.mult_inverse)
interface.add('i', functions.add_inverse)
interface.add('M', functions.modulo)
interface.add('!e', functions.e)
interface.add('!p', functions.pi)
interface.add('t', functions.copy_from_stack)
interface.add('u', functions.undo)
interface.add('Q', functions.quit)


def main(screen):
    """ Main entrypoint, sets up screens etc. """
    screen.clear()
    helpWindowWidth = 21
    interface.helpWindow = curses.newwin(curses.LINES-2, helpWindowWidth,
                                         0, curses.COLS-helpWindowWidth-1)
    interface.stackWindow = curses.newwin(curses.LINES-2, curses.COLS-helpWindowWidth-1, 0, 0)
    interface.entryBox = curses.newwin(1, curses.COLS-1, curses.LINES-1, 0)
    interface.mainScreen = screen

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Used for warnings
    screen.refresh()
    displayStack(interface.stackWindow)
    displayHelp(interface.helpWindow)

    while True:
        c = interface.getKey()
        interface.run(c)


def lineLabel(n):
    """ return how item n (numbered 1-indexed from the top of the stack) should
    be labeled """
    if n == 1:
        return 'x'
    if n == 2:
        return 'y'
    if n == 3:
        return 'z'
    return "{}".format(n-3)


def lineLabelLookup(key):
    """ Return the line from the stack (as negative index) to get to the stack
    item. """
    if key == 'x':
        return -1
    if key == 'y':
        return -2
    if key == 'z':
        return -3
    num = int(key)
    if num < 1:
        raise ValueError("number too low")
    return -3-num


def addToStack(item):
    stack.append(item)
    undostack.append(functions.UndoItem(1, []))


def displayStack(window):
    """ Display the stack in window """
    window.clear()
    # Add the labeled items including numbers
    for line, num in zip(stack, range(len(stack), 0, -1)):
        window.addstr("{}: {}\n".format(lineLabel(num), line))
    window.refresh()


def displayHelp(window):
    """ Display the help messages in the sidebar """
    window.clear()
    window.addstr(0, 0, interface.helptext())
    window.refresh()


def displayError(window, error):
    """ Display the stack, with an error message """
    displayStack(window)
    window.addstr("\n")
    window.addstr(error, curses.color_pair(2))
    window.refresh()


curses.wrapper(main)
