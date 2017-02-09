#!/usr/bin/env python3
# ERPN, an RPN calculator
# Copyright (C) 2017 Bart de Waal
# This program is licenced under the GPL version 3, see Licence file for details

import urwid

from .buttonMappings import loadMappings
from .urwidInterface import Interface

interface = Interface()
loadMappings(interface)


def main():
    palette = [('arrow', 'yellow', 'default'),
               ('lineLabel', 'dark cyan', 'default'),
               ('error', 'light red', 'default')]
    loop = urwid.MainLoop(interface.root, palette,
                          unhandled_input=interface.takeKey,
                          handle_mouse=False)
    loop.run()
