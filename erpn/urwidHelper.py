# ERPN, an RPN calculator
# Copyright (C) 2017 Bart de Waal
# This program is licenced under the GPL version 3, see Licence file for details

import urwid

class FillerWithMemory(urwid.Filler):
    lastWidth = None
    lastHeight = None
    def render(self, size, focus=False):
        (self.lastWidth, self.lastHeight) = size
        return super().render(size, focus)

