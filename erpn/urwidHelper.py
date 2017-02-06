# ERPN, an RPN calculator
# Copyright (C) 2017 Bart de Waal
# This program is licenced under the GPL version 3, see Licence file for details

import urwid


class FillerWithMemory(urwid.Filler):
    """ Like a urwid filler, but remember the last heigth and width you had.
    This allows you to adjust for the height and width """
    lastWidth = None
    lastHeight = None

    def render(self, size, focus=False):
        (self.lastWidth, self.lastHeight) = size
        return super().render(size, focus)
