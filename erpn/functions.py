# ERPN, an RPN calculator
# Copyright (C) 2017 Bart de Waal
# This program is licenced under the GPL version three, see Licence file for details

import math

from .domain import Reals, Integers
from pyperclip import copy, paste


class StackToSmallError(Exception):
    """ The Stack is to small to preform the requested operation """
    pass


class DomainError(Exception):
    """ An argument is not defined on an argument """
    pass


class RPNfunction:
    def __init__(self, args, description, function,
                 functionDomain=[Reals, Reals],
                 undo=True, checkStackSize=True,
                 display=True):
        """an RPN function.
        rpn is the number of items it takes from the stack
        description is a short description of the function
        function should return a list to be added to the stack, and should take a list as input
        functionDomain is a list of domains, element 0 will check argument x etc.
        undo is for functions like "copy" that would be confusing for a user if they could be undone
        Some functions can use a default element, so they don't need to check the stack size
        Display indicates whether this function should be displayed in the help bar """
        self.function = function
        self.args = args
        self.description = description
        self.checkStackSize = checkStackSize
        self.functionDomain = functionDomain
        self.undo = undo
        self.display = display

    def run(self, stack, undostack, arrowLocation):
        """ Run the function on the stack """
        self.handleArrow(stack, undostack, arrowLocation)

        if self.checkStackSize and len(stack) < self.args:
            raise StackToSmallError()

        functionArguments = []
        if self.args > 0:
            functionArguments = stack[-self.args:]
        self.checkDomain(functionArguments)

        toAdd = self.function(functionArguments)

        if(self.undo):
            # Remember how many items we added and which ones we removed so we can undo
            undostack.append(UndoItem(len(toAdd), functionArguments, self))

        if self.args > 0:
            del stack[-self.args:]

        stack.extend(toAdd)

    def checkDomain(self, arguments):
        if self.checkStackSize:
            # functions that don't check the stack size will need to do their own domain checking
            for i in range(self.args):
                if arguments[-1-i] not in self.functionDomain[i]:
                    raise DomainError("'{}' is not defined at {}".format(self.description,
                                                                         arguments[-1-i]))

    def handleArrow(self, stack, undostack, arrowLocation):
        if arrowLocation != 0:
            value = stack[-arrowLocation-1]
            AddItem(value).run(stack, undostack, 0)

    def __str__(self):
        return "RPN function, {}, {} args".format(self.description, self.args)


class UndoItem:
    def __init__(self, remove, add, redo):
        """ An action to undo something
        remove: how many items this will remove
        add: the list of items it will add
        redo: the RPNclass instance to redo this action. It is always run with ArrowLocation=0"""
        self.remove = remove
        self.add = add
        self.redo = redo

    def apply(self, stack):
        """ Apply the remembered undo action to indicated stack """
        if self.remove > 0:
            del stack[-self.remove:]
        stack.extend(self.add)

    def __str__(self):
        return "Undo: Remove {}, add {}".format(self.remove, self.add)


def multiply_function(items):
    """ Multiply two items from the stack, if there are no two items use 1
    instead """
    items = items + [1, 1]
    return [items[0]*items[1]]


def check_exponent_domain(args):
    """ check the domain for y^x """
    x = args[-1]
    y = args[-2]
    if y < 0:
        if x not in Integers:
            raise DomainError("Cannot raise negative numbers to a non-integer power")
    if y == 0.0:
        if x < 0.0:
            raise DomainError("Cannot raise 0 to a negative power")


def check_tan_domain(args):
    """ Check the domain for tan(x)
    This cosists of the real numbers line, excluding pi/2 + k*pi"""
    x = args[-1]
    if math.isclose(math.pi/2,
                    math.fmod(x, math.pi)):
        raise DomainError("tan(x) is not defined at pi/2 radians")


def copy_function(args):
    """ Copy x to the clipboard without changing anything """
    x = args[-1]
    copy(str(x))
    return [x]


def paste_function(args):
    """ Take value from OS clipboard """
    try:
        return([float(paste())])
    except:
        raise DomainError("Unable to use clipboard value")


# Basic functions
switch2 = RPNfunction(2, "switch x, y", lambda x: [x[1], x[0]])

addition = RPNfunction(2, "x+y", lambda x: [sum(x)], checkStackSize=False)
subtract = RPNfunction(2, "y-x", lambda x: [x[0]-x[1]])
multiply = RPNfunction(2, "x*y", multiply_function, checkStackSize=False)
divide = RPNfunction(2, "y/x", lambda x: [x[0]/x[1]], [Reals - {0}, Reals])

exponent = RPNfunction(2, "y^x", lambda x: [x[0]**x[1]])
exponent.checkDomain = check_exponent_domain
square = RPNfunction(1, "x^2", lambda x: [x[0]*x[0]])
sqrt = RPNfunction(1, "sqrt x", lambda x: [math.sqrt(x[0])], [Reals >= 0])
power_e = RPNfunction(1, "e^x", lambda x: [math.exp(x[0])])
power_10 = RPNfunction(1, "10^x", lambda x: [10**x[0]])
log10 = RPNfunction(1, "log10", lambda x: [math.log10(x[0])], [Reals > 0])
ln = RPNfunction(1, "ln", lambda x: [math.log(x[0])], [Reals > 0])

mult_inverse = RPNfunction(1, "1/x", lambda x: [1/x[0]], [Reals - {0}])
add_inverse = RPNfunction(1, "-x", lambda x: [-x[0]])

modulo = RPNfunction(2, "y mod x", lambda x: [math.fmod(x[0], x[1])], [Reals - {0}, Reals])

sin = RPNfunction(1, "sin x (rad)", lambda x: [math.sin(x[0])])
cos = RPNfunction(1, "cos x (rad)", lambda x: [math.cos(x[0])])
tan = RPNfunction(1, "tan x (rad)", lambda x: [math.tan(x[0])])
tan.checkDomain = check_tan_domain

arcsin = RPNfunction(1, "arcsin x (rad)", lambda x: [math.asin(x[0])],
                     [(Reals <= 1) >= -1])
arccos = RPNfunction(1, "arccos x (rad)", lambda x: [math.acos(x[0])],
                     [(Reals <= 1) >= -1])
arctan = RPNfunction(1, "arctan x (rad)", lambda x: [math.atan(x[0])])

floor = RPNfunction(1, "floor", lambda x: [math.floor(x[0])])
ceil = RPNfunction(1, "ceil", lambda x: [math.ceil(x[0])])
factorial = RPNfunction(1, "factorial",
                        lambda x: [math.factorial(round(x[0]))],
                        [Integers >= 0])
gcd = RPNfunction(2, "GCD", lambda x: [math.gcd(round(x[0]), round(x[1]))],
                  [Integers > 0, Integers > 0])


def raise_(ex):
    """I like to use exceptions as flow control, and I like to define functions
    using lambda So this is a helper function to let me raise exceptions in
    lambda"""
    raise ex


def Pass(*args, **namedArgs):
    pass


class IsBack(Exception): pass  # noqa
class IsUndo(Exception): pass  # noqa
class IsRedo(Exception): pass  # noqa
class IsQuit(Exception): pass  # noqa
class IsCopyFromStack(Exception): pass  # noqa
class EnterDisplayMenu(Exception): pass  # noqa


class IsArrow(Exception):
    def __init__(self, direction, message="Arrow button pressed", *args):
        """ Direction should be "up" or "down" """
        self.message = message
        self.direction = direction
        super().__init__(message)


undo = RPNfunction(0, "undo", lambda x: raise_(IsUndo()))
redo = RPNfunction(0, "redo", lambda x: raise_(IsRedo()))
quit = RPNfunction(0, "quit", lambda x: raise_(IsQuit()))
back = RPNfunction(0, "go back", lambda x: raise_(IsBack()))
quit = RPNfunction(0, "quit", lambda x: raise_(IsQuit()))
copy_from_stack = RPNfunction(1, "Copy from Stack", lambda x: raise_(IsCopyFromStack()))
copy_to_OS = RPNfunction(1, "Copy", copy_function, undo=False)
paste_from_OS = RPNfunction(0, "Paste", paste_function)
menu_display = RPNfunction(0, "Change Display", lambda x: raise_(EnterDisplayMenu()))

arrow_up = RPNfunction(0, "Arrow up", lambda x: raise_(IsArrow("up")), display=False, undo=False)
arrow_up.handleArrow = Pass
arrow_down = RPNfunction(0, "Arrow down", lambda x: raise_(IsArrow("down")), display=False, undo=False)
arrow_down.handleArrow = Pass


class CopyCurrent(RPNfunction):
    def __init__(self, display=True):
        self.description = "Copy Current"
        self.display = display

    def run(self, stack, undostack, arrowLocation):
        if len(stack) < 1:
            raise StackToSmallError()

        toAdd = stack[-arrowLocation-1]

        # Undo should delete the item we just added, and add nothing
        undostack.append(UndoItem(1, [], AddItem(toAdd)))
        stack.extend([toAdd])


class UndoDelete(UndoItem):
    def __init__(self, position, value):
        """ Undo a deletion action
        When this undo is applied, value will be at position
        position should be a non-negative integer, just like ArrowLocation"""
        self.position = position
        self.value = value
        self.redo = Delete(deleteLocation=position)

    def apply(self, stack):
        """ Apply the remembered undo action to indicated stack """
        if self.position == 0:
            stack.append(self.value)
        else:
            stack.insert(-self.position, self.value)

    def __str__(self):
        return "Undo: delete {} at position {}".format(self.value, self.position)


class Delete(RPNfunction):
    def __init__(self, display=True, deleteLocation=None):
        self.description = "delete x"
        self.display = display
        self.deleteLocation = deleteLocation

    def run(self, stack, undostack, arrowLocation):
        if len(stack) < 1:
            raise StackToSmallError()

        if self.deleteLocation is not None:
            arrowLocation = self.deleteLocation

        undoVal = stack.pop(-arrowLocation-1)
        undostack.append(UndoDelete(arrowLocation, undoVal))

    def __str__(self):
        return "Delete single item from stack"


class AddItem(RPNfunction):
    """ RPN function to add an item to the stack.
    The __init__ function will check that the value is a float we can use """
    def __init__(self, value, display=True, description=None):
        value = float(value)
        if value not in Reals:
            raise ValueError
        self.valueToAdd = value
        if description is None:
            self.description = "push {}".format(value)
        else:
            self.description = description
        self.display = display

    def run(self, stack, undostack, arrowLocation):
        stack.append(self.valueToAdd)
        undostack.append(UndoItem(1, [], self))


class ChangeDisplayFormat(Exception):
    """ An exception to signal we want to change the display settings. It
    carries the display settings it wants with it """
    def __init__(self, adj_format, message="Change Display Format", *args):
        """ adj_format can be + or - to change the precision, or a ValueFormatter """
        self.adj_format = adj_format
        super().__init__(message)


class ChangeDisplayFunction(RPNfunction):
    """ Raise an ChangeDisplayFormat exception to set the correct display value """
    def __init__(self, adj_format, display=True, description=None):
        """ adj_format can be '+' or '-' to change the precision, or a ValueFormatter """
        self.adj_format = adj_format
        self.description = description
        self.display = display

    def run(self, *args, **kwargs):
        raise ChangeDisplayFormat(self.adj_format)
