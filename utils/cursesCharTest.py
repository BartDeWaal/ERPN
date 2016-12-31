# Small program to find out how to map a function to a key

import curses
from curseshelper import getKeyAlt


def main(stdscr):
    # Clear screen
    stdscr.clear()

    key = getKeyAlt(stdscr)

    while True:
        stdscr.addstr(1, 3, "Use Ctrl-C to quit")
        stdscr.addstr(2, 3, key)
        stdscr.refresh()
        for i in range(6):
            # put them below each other, to make it easer to compare stuff
            key = getKeyAlt(stdscr)
            stdscr.addstr(3 + i, 3, key)
            stdscr.refresh()
        stdscr.clear()


curses.wrapper(main)
