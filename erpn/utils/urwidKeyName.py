#!/usr/bin/env python3
# Util to find out what urwid's name for a key (pressed on the keyboard) is.
# Adapted from example in the tutorial

import urwid


def show_or_exit(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    txt.set_text(repr(key))


palette = [('quoteColor', 'light red', 'default'), ]
txt = urwid.Text("Press key to display name, q to quit")
fill = urwid.Filler(txt, 'top')
loop = urwid.MainLoop(fill, unhandled_input=show_or_exit)
loop.run()
