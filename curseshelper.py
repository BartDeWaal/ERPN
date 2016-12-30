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
