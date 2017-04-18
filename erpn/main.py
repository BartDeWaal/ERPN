#!/usr/bin/env python3
# ERPN, an RPN calculator
# Copyright (C) 2017 Bart de Waal
# This program is licenced under the GPL version 3, see Licence file for details

import urwid
from argparse import ArgumentParser

from .buttonMappings import loadMappings
from .urwidInterface import Interface

version = '1.0'
website = 'https://github.com/BartDeWaal/ERPN'

interface = Interface()
loadMappings(interface)


def main():
    parser = ArgumentParser(
        prog="erpn",
        description='An RPN calculator',
        epilog='See website for full instructions: {}'.format(website))
    parser.add_argument('--version', dest='version',
                        action='store_const', const=True,
                        help='show the version number and exit')
    args = parser.parse_args()
    if args.version is True:
        print("erpn {}\n{}".format(version, website))
        return

    palette = [('arrow', 'yellow', 'default'),
               ('lineLabel', 'dark cyan', 'default'),
               ('error', 'light red', 'default')]
    loop = urwid.MainLoop(interface.root, palette,
                          unhandled_input=interface.takeKey,
                          handle_mouse=False)
    loop.run()
