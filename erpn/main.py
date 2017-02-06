#!/usr/bin/env python3
# ERPN, an RPN calculator
# Copyright (C) 2017 Bart de Waal
# This program is licenced under the GPL version 3, see Licence file for details

import urwid
from collections import defaultdict

from . import functions
from .buttonMappings import loadMappings
from . import urwidHelper
from . import stackFormat

stack = []  # The stack as displayed to the unit
undostack = []  # The stack of undo actions
redostack = []


class Interface:
    """ Container for all the interface (keybindings, display etc.) for the calulator """
    # functions holds all the keybindings.  We support having multiple
    # different menus with different items, so they all need to be stored
    # seperataly. 'main' is the one loaded at startup.
    functions = {'main': {}, 'display': {}}

    # To make it easy to keep track of the current menu, we keep the latest set
    # of button mappings in functions_stack[-1]. If we go back, we can just pop
    # the top part.
    functions_stack = [functions['main']]

    arrowLocation = 0  # The location of the arrow selector
    numberEntry = ""  # If we are currently entering a number, this will contain the entry up to now
    error = None  # The currently displayed error

    displayFormat = stackFormat.OptionalExponent(3)  # default display mode

    def add(self, key, function, category='main'):
        """ Add a entry to link a keyboard shortcut to a function """
        if key in self.functions[category]:
            # You probably don't want to overwrite everything
            raise Exception("Already defined key {} for category {}".format(key, category))
        self.functions[category][key] = function

    def enterNumber(self, key):
        """ Enter an entry
            It handles key (a string) as the start of the entry
            Returns None if the number entry isn't done, or a key if it is """
        global redostack

        # find out all the keys it's allowed to have
        allowedKeys = "1234567890"

        # '_' means '-' in this context if it is the first character, to allow
        # users to enter negative numbers
        if self.numberEntry == "" and key == '_':
            allowedKeys += '-'  # we need to allow the first character
            key = '-'

        # We also allow a - after an e
        if len(self.numberEntry) > 0 and self.numberEntry[-1] == 'e':
            allowedKeys += '-'
            # For consistency the user should be able to enter _ after an e too
            if key == '_':
                key = '-'

        # allow decimalpoints if we don't have one yet, and it's not after the
        # e in an engineering number
        if 'e' not in self.numberEntry and '.' not in self.numberEntry:
            allowedKeys += '.'

        # allow e, unless:
        # - there is already an e, don't allow 1e5e2
        # - there is no digit yet, so don't allow -e4 or .e5
        if 'e' not in self.numberEntry and any(c.isdigit() for c in self.numberEntry):
            allowedKeys += 'e'

        if key in allowedKeys:
            self.numberEntry += key
            return None
        else:
            try:
                functions.AddItem(self.numberEntry).run(stack, undostack,
                                                        self.arrowLocation)
                self.clearError()
                redostack = []
            except ValueError:
                self.setError("Could not decode value")
            self.numberEntry = ""
            return key

    def takeKey(self, key):
        """ React to a pressed key """
        global redostack

        if len(self.numberEntry) > 0 or key in '1234567890._':
            key = self.enterNumber(key)
            self.displayStack()
            # if the entry is done enterNumber will return the next key, which
            # we need to apply to the stack
            # The only exception we make is for the "copy numbers" buttons,
            # sometimes I just press enter to finish entering a number
            if (key is not None and
                (key not in self.functions_stack[-1] or
                 not isinstance(self.functions_stack[-1][key], functions.CopyCurrent))):
                        self.takeKey(key)
            return

        if key in self.functions_stack[-1]:
            try:
                # This function uses exceptions to communicate if something is
                # not a simple function on the stack
                self.checkArrowLocation()
                self.functions_stack[-1][key].run(stack, undostack, self.arrowLocation)
                self.arrowLocation = 0

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
                    undo = undostack.pop()
                    undo.apply(stack)
                    redostack.append(undo.redo)
                    self.clearError()
                else:
                    self.setError("Nothing to undo")

            except functions.IsRedo:
                if len(redostack) > 0:
                    redo = redostack.pop()
                    redo.run(stack, undostack, 0)
                else:
                    self.setError("Nothing to Redo")

            except functions.IsArrow as e:
                if e.direction == "up":
                    self.arrowLocation += 1
                else:
                    self.arrowLocation -= 1
                self.checkArrowLocation()

            except functions.IsQuit:
                raise urwid.ExitMainLoop()

            except functions.EnterDisplayMenu:
                self.functions_stack.append(self.functions['display'])
                self.displayHelp()

            except functions.IsBack:
                if len(self.functions_stack) > 0:
                    self.functions_stack.pop()
                    self.displayHelp()
                else:
                    self.setError("No menu to go back to")

            except functions.ChangeDisplayFormat as e:
                if e.adj_format == '+':
                    self.displayFormat.add_precision()
                elif e.adj_format == '-':
                    self.displayFormat.remove_precision()
                elif isinstance(e.adj_format, stackFormat.ValueFormatter):
                    # We want to use the format given by the exception, but we
                    # want to keep the precision the user has already set.
                    digits_after_decimal = self.displayFormat.digits_after_decimal
                    self.displayFormat = e.adj_format
                    self.displayFormat.digits_after_decimal = digits_after_decimal
                else:
                    self.setError("Unparsable format")

            else:
                # If the function applied and no new errors appeared we can clear the error
                self.clearError()
                redostack = []

        self.displayStack()

    def setError(self, error_text):
        """ Display an error """
        self.error = error_text

    def clearError(self):
        """ Clear the error display """
        self.error = None

    def setupWindows(self):
        """ Setup the different parts of the screen layout """
        self.helpBox = urwid.Text('')
        self.displayHelp()
        helpfill = urwid.Filler(self.helpBox, 'top')

        self.stackBox = self.getStackBox()
        self.stackfill = urwidHelper.FillerWithMemory(self.stackBox, 'bottom')
        self.displayStack()

        self.root = urwid.Columns([self.stackfill, (23, helpfill)])

    def getStackBox(self):
        """ Display the stack in window. Supply the stack to display """
        return urwid.Text("")

    def displayStack(self):
        lines = [""]

        # Display the current entry at the bottom of the stack.
        displayStack = stack
        if self.numberEntry != "":
            displayStack = displayStack + [self.numberEntry]

        # If possible, limit the lines shown so you only see the bottom of the stack.
        if self.stackfill.lastHeight is not None:
            displayStack = displayStack[-self.stackfill.lastHeight+1:]

        for i in range(len(displayStack)):
            n = len(displayStack) - i - 1
            arrow = "   "
            if(n != 0 and n == self.arrowLocation):
                arrow = ('arrow', " ->")
            label = ('lineLabel', "{:>3}: ".format(lineLabel(n)))
            number = self.displayFormat(displayStack[i])
            lines.extend([arrow, label, number, "\n"])

        if self.error is not None:
            lines.append(('error', self.error))

        self.stackBox.set_text(lines)

    def displayHelp(self):
        """ Update the text in the self.helpBox """
        # First generate the strings

        # All items in the dicts are [] by default, so we can append to them
        # without checking if they exist
        items = defaultdict(lambda: [])
        # The keys in this dict will be the functions they are linked to.

        for item in self.functions_stack[-1]:
            items[self.functions_stack[-1][item]].append(item)

        helpStrings = []
        for item in items:
            if item.display:
                newitem = "{}: {}".format(', '.join(sorted(items[item])),
                                          item.description)
                helpStrings.append(newitem)

        helpStrings.sort()  # this will do until I figure out a better way to sort the displayed strings
        self.helpBox.set_text('\n'.join(helpStrings))

    def checkArrowLocation(self):
        """ Ensure that the arrow is actually pointing at the stack """
        if self.arrowLocation < 0 or self.arrowLocation >= len(stack):
            self.arrowLocation = 0


interface = Interface()
loadMappings(interface)


def lineLabel(n):
    """ return how item n (numbered with 0 the top of the stack) should be
    labeled """
    if n == 0:
        return 'x'
    if n == 1:
        return 'y'
    if n == 2:
        return 'z'
    return "{}".format(n-2)


def addToStack(item):
    stack.append(item)
    undostack.append(functions.UndoItem(1, []))


def main():
    interface.setupWindows()
    palette = [('arrow', 'yellow', 'default'),
               ('lineLabel', 'dark cyan', 'default'),
               ('error', 'light red', 'default')]
    loop = urwid.MainLoop(interface.root, palette,
                          unhandled_input=interface.takeKey,
                          handle_mouse=False)
    loop.run()
