# ERPN, an RPN calculator
# Copyright (C) 2017 Bart de Waal
# This program is licenced under the GPLv3, see Licence file for details

from . import functions

def loadMappings(interface):
    """ Load all the mappings """
    # See utils folder for script that helps figure out what each key does
    interface.add('x', functions.Delete())
    interface.add('z', functions.switch2)
    interface.add('+', functions.addition)
    interface.add('a', functions.addition)
    interface.add('s', functions.subtract)
    interface.add('-', functions.subtract)
    interface.add('m', functions.multiply)
    interface.add('*', functions.multiply)
    interface.add('d', functions.divide)
    interface.add('/', functions.divide)
    interface.add('p', functions.exponent)
    interface.add('q', functions.square)
    interface.add('S', functions.sqrt)
    interface.add('E', functions.power_e)
    interface.add('e', functions.power_10)  # Should be bound to e for compatability with "1e3" notation
    interface.add('L', functions.log10)
    interface.add('l', functions.ln)
    interface.add('I', functions.mult_inverse)
    interface.add('i', functions.add_inverse)
    interface.add('M', functions.modulo)
    interface.add('%', functions.modulo)
    interface.add('#', functions.gcd)
    interface.add('!', functions.factorial)
    interface.add('`', functions.floor)
    interface.add('~', functions.ceil)
    interface.add('meta e', functions.e)
    interface.add('meta p', functions.pi)

    interface.add('meta t', functions.tan)
    interface.add('meta s', functions.sin)
    interface.add('meta c', functions.cos)
    interface.add('meta T', functions.arctan)
    interface.add('meta S', functions.arcsin)
    interface.add('meta C', functions.arccos)

    interface.add(' ', functions.CopyCurrent(display=False))
    interface.add('enter', functions.CopyCurrent())
    interface.add('u', functions.undo)
    interface.add('Q', functions.quit)
    interface.add('c', functions.copy_to_OS)
    interface.add('v', functions.paste_from_OS)

    interface.add('up', functions.arrow_up)
    interface.add('k', functions.arrow_up)
    interface.add('down', functions.arrow_down)
    interface.add('j', functions.arrow_down)
