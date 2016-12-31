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
    labelColumn = None

    def add(self, key, function):
        """ Add a entry to link a keyboard shortcut to a function """
        if key in self.functions:
            # You probably don't want to overwrite everything
            raise Exception("Already defined key {}".format(key))
        self.functions[key] = function

    def run(self, key):
        """ React to a pressed key """

        if key in '1234567890._':
            # if this is a number or starts with a space we want to
            # let the user enter the whole line
            self.clearError()
            self.displayLineLabels(len(stack), True)
            self.entry(key)
            self.displayLineLabels(len(stack), False)

        if key in self.functions:
            try:
                # This function uses exceptions to communicate if something is
                # not a simple function on the stack
                self.functions[key].run(stack, undostack)

            except functions.StackToSmallError:
                self.setError("Stack too small")

            except functions.DomainError as e:
                self.setError(str(e))

            except OverflowError:
                self.setError("Value too large")

            except functions.IsUndo:
                # Take the top action from the undostack and apply it to the
                # stack
                if len(undostack) > 0:
                    undostack.pop().apply(stack)
                    self.clearError()
                else:
                    self.setError("Nothing to undo")

            except functions.IsCopyFromStack:
                c = self.getKey()
                try:
                    addToStack(stack[lineLabelLookup(c)])
                except:
                    self.setError("Could not lookup value")

            except functions.IsQuit:
                exit()

            else:
                # If the function applied and no new errors appeared we can clear the error
                self.clearError()

        self.displayStack(stack)
        self.displayLineLabels(len(stack))

    def entry(self, key):
        """ Let the user enter a line, mainly for entering new numbers """
        val, nextkey = curseshelper.getEntry(self.entryBox, key)
        try:
            val = float(val)
            addToStack(val)
            self.displayStack(stack)
            self.run(nextkey)
        except ValueError:
            self.setError("Could not decode value")

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

    def setError(self, error_text):
        """ Display an error """
        self.errorWindow.clear()
        self.errorWindow.addstr(error_text, curses.color_pair(2))
        self.errorWindow.refresh()

    def clearError(self):
        """ Clear the error display """
        self.setError("")

    def setupWindows(self, screen):
        """ Setup the screen layout """
        width = curses.COLS
        height = curses.LINES

        self.mainScreen = screen
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Used for warnings/Errors
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Used for line labels

        # We use four colums. From left to right:
        # A left column. This includes the label numbers. Some day this may be used to display an arrow
        # The stack column, with the main display
        # A small spacer column
        # And the hel column on th right
        helpColumn = 21
        leftColumn = 8
        spacerColumn = 1
        stackColumn = width - helpColumn - leftColumn - spacerColumn

        self.labelColumn = curses.newwin(height, leftColumn, 0, 0)

        x = leftColumn
        self.stackWindow = curses.newwin(height-2, stackColumn, 0, x)
        self.entryBox = curses.newwin(1, stackColumn, height-2, x)
        self.errorWindow = curses.newwin(1, stackColumn, height-1, x)

        x += stackColumn + spacerColumn
        self.helpWindow = curses.newwin(height-2, helpColumn, 0, x)

    def displayLineLabels(self, stacksize, enteringValue=False):
        """ Display the labels to the left of the stack.
        stacksize is the number of items on the stack.
        While a value is being entered it should go down one to label the new
        value as it is entered.  """
        addAtEnd = ["", ""]  # Fill the last few spaces with this
        if enteringValue:
            stacksize += 1
            addAtEnd = [""]

        labels = ["   {:>3}:".format(lineLabel(i)) for i in range(stacksize)]

        curseshelper.displayFromBottom(self.labelColumn, addAtEnd + labels, curses.color_pair(3))

    def displayStack(self, stackObject):
        """ Display the stack in window. Supply the stack to display """
        lines = ["{}".format(x) for x in reversed(stackObject[-100:])]  # 100 is the maximum amount of lines I expect
        curseshelper.displayFromBottom(self.stackWindow, lines)


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
interface.add('c', functions.copy_to_OS)


def main(screen):
    """ Main entrypoint, sets up screens etc. """
    screen.clear()
    screen.refresh()
    interface.setupWindows(screen)
    interface.displayStack(stack)
    displayHelp(interface.helpWindow)
    interface.displayLineLabels(len(stack))

    while True:
        c = interface.getKey()
        interface.run(c)


def lineLabel(n):
    """ return how item n (numbered 0-indexed from the top of the stack) should
    be labeled """
    if n == 0:
        return 'x'
    if n == 1:
        return 'y'
    if n == 2:
        return 'z'
    return "{}".format(n-2)


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


def displayHelp(window):
    """ Display the help messages in the sidebar """
    window.clear()
    window.addstr(0, 0, interface.helptext())
    window.refresh()


curses.wrapper(main)
