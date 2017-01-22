# ERPN, an RPN calculator
# Copyright (C) 2016 Bart de Waal
# This program is licenced under the GPL version three, see Licence file for details
import curses


class EchoOn:
    """ helper class, so you can say "with EchoOn:" """
    def __enter__(self):
        curses.echo()

    def __exit__(self, type, value, traceback):
        curses.noecho()


class NoDelay:
    """ Alows you to do a getch() that times out as soon as possible """
    # Todo: find out why this is so slow
    def __init__(self, window):
        self.window = window

    def __enter__(self):
        self.window.nodelay(True)
        self.window.timeout(1)

    def __exit__(self, type, value, traceback):
        self.window.nodelay(False)
        self.window.timeout(-1)


def getKeyAlt(window):
    """ getKey, but adding ! in front of keys pressed with alt """
    key = window.getch()
    # If alt+ something is pressed, getch returns 27 and will return the next
    # character on the next round
    if key == 27:
        with NoDelay(window):
            key = window.getch()
        # If the second character doesn't come (getch times out with -1) this
        # is an escape
        if key == -1:
            return '^['
        else:
            return '!' + curses.unctrl(key).decode('ascii')
    return curses.unctrl(key).decode('ascii')


def getEntry(window, key):
    """ Enter an entry, using the window to display the entry
        It handles key (a string) as the start of the entry
        Returns a tuple: (string entered, key pressed to abort entry) """
    window.refresh()
    (y, x) = window.getmaxyx()

    # '_' means '-' in this context, to allow users to enter negative numbers
    if key[0] == '_':
        key = '-' + key[1:]

    # display the first character(s) the user already entered
    window.addstr(0, 0, key)
    window.refresh()

    engineeringkey = "e"  # Allow things like "1e3"
    decimalpoint = "."
    if key == '.':
        decimalpoint = ""  # We shouldn't allow two decimal points

    c = window.getkey()
    while c in "1234567890" + engineeringkey + decimalpoint:
        if engineeringkey == '-':
            engineeringkey = ""  # stop allowing after the first
            # the user only has one chance to enter the negative sign
        if c == 'e':
            engineeringkey = '-'  # allow for 1e-3
            decimalpoint = ""  # don't allow decimal point after e
        if c == ".":
            decimalpoint = ""  # only one decimal point

        key = key + c

        displaykey = key[:x-1]  # Don't display more than the width of the screen
        if len(key) != len(displaykey):
            displaykey = displaykey[:-3] + "..."

        window.clear()
        window.addstr(0, 0, displaykey)
        window.refresh()
        c = window.getkey()

    window.clear()
    window.refresh()

    return key, c


def displayFromBottom(window, lines, displayProperties=None):
    """ Display things from the bottom of a window. Overflow will be ignored.
    window is the window to put things in
    lines is a list of the lines to add
    The strings should not contain enters"""
    (y, x) = window.getmaxyx()

    display = min(len(lines), y)  # how many items to display.
    # This can be limited y the size of the list or by the window

    start = min(y - display, y-1)  # we want at least one or the curser goes to low

    window.clear()
    window.move(start, 0)

    lines = [line[:x-1] for line in reversed(lines[:display])]  # trunctuate and sort the lines

    if displayProperties is None:
        window.addstr("\n".join(lines))
    else:
        window.addstr("\n".join(lines), displayProperties)
    window.refresh()
