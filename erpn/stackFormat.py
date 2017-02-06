# ERPN, an RPN calculator
# Copyright (C) 2017 Bart de Waal
# This program is licenced under the GPLv3, see Licence file for details

from math import log10, floor, isclose


class ValueFormatter:
    """ Parent class
    A valueformatter is a class that allows you to display values on the stack
    as strings in a user-defined way """
    max_digits = 15  # the maximum amount of digits we want to display

    def __init__(self, digits_after_decimal=2, exponent_grouping=1):
        self.digits_after_decimal = digits_after_decimal
        # exponent grouping is only used for scientific notation
        # The exponents displayed should be a multiple of this.
        # For "engineering display" exponent_grouping should be 3.
        self.exponent_grouping = exponent_grouping

    def __call__(self, value):
        """ You can use a valueformatter like this:
        a = ValueFormatter()
        print(a(value)) """
        if isinstance(value, str):
            return value
        else:
            return self.display(value)

    def display_using_exponent(self, value):
        """ Display using an exponent, using self.exponent_grouping to
        determine valid values of the exponent """
        exponent = floor(log10(abs(value))/self.exponent_grouping) * self.exponent_grouping
        mantissa = value/(10**exponent)
        return "{:.{precision}f}e{exponent}".format(mantissa,
                                                    precision=self.digits_after_decimal,
                                                    exponent=exponent)

    def add_precision(self):
        self.digits_after_decimal += 1
        if self.digits_after_decimal > self.max_digits - 2:
            # I don't have a great reason to limit it to max_digits - 2, but it seems about right
            self.digits_after_decimal = self.max_digits - 2

    def remove_precision(self):
        self.digits_after_decimal -= 1
        if self.digits_after_decimal < 0:
            self.digits_after_decimal = 0


class NoExponent(ValueFormatter):
    """ Never show an exponent, so 0.001 could get displayed as 0.00 """
    def display(self, value):
        return "{:.{precision}f}".format(value, precision=self.digits_after_decimal)


class OptionalExponent(ValueFormatter):
    """ format  a number, only use an exponent if required """
    # the displayed number should be within precision of the
    # actual value. Otherwise use exponent display.
    precision = 0.1  # 10%

    def display(self, value):
        noExponentDisplay = "{:.{precision}f}".format(value, precision=self.digits_after_decimal)
        rounded_value = float(noExponentDisplay)
        if (value == 0.0 or
            (isclose(value, rounded_value, rel_tol=self.precision) and
             len(noExponentDisplay) < self.max_digits)):
                # The simple display is close enough to the real value, and the
                # number is short enough we can go with the simple display
                return noExponentDisplay
        else:
            return self.display_using_exponent(value)


class UseExponent(ValueFormatter):
    """ Format a number using an exponent to display """
    def display(self, value):
        return self.display_using_exponent(value)
