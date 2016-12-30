# CRPN, a Curses based RPN calculator
# Copyright (C) 2016 Bart de Waal
# This program is licenced under the GPL version three, see Licence file for details
import curses


class EchoOn:
    """ helper class, so you can say "with EchoOn:" """
    def __enter__(self):
        curses.echo()

    def __exit__(self, type, value, traceback):
        curses.noecho()


def getEntry(window, key):
    """ Enter an entry, using the window to display the entry
        It handles key (a string) as the start of the entry
        Returns a tuple: (string entered, key pressed to abort entry) """
    window.refresh()

    # '_' means '-' in this context, to allow users to enter negative numbers
    if key[0] == '_':
        key = '-' + key[1:]

    # display the first character(s) the user already entered
    window.addstr(0, 0, key)
    window.refresh()

    c = chr(window.getch())
    while c in "1234567890.e":
        key = key + c
        window.clear()
        window.addstr(0, 0, key)
        window.refresh()
        c = chr(window.getch())

    window.clear()
    window.refresh()

    return key, c
