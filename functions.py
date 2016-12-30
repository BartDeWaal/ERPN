import math


class StackToSmallError(Exception):
    pass


class RPNfunction:
    def __init__(self, args, description, function, checkStackSize=True):
        """an RPN function.
        rpn is the number of items it takes from the stack
        description is a SHORT description of the function
        function should return a list to be added to the stack, and should take a list as input"""
        self.function = function
        self.args = args
        self.description = description
        self.checkStackSize = checkStackSize

    def run(self, stack, undostack):
        """ Run the function on the stack """
        if self.checkStackSize and len(stack) < self.args:
            raise StackToSmallError()
        toAdd = self.function(stack[-self.args:])
        undostack.append(UndoItem(len(toAdd), stack[-self.args:]))
        if self.args > 0:
            del stack[-self.args:]
        stack.extend(toAdd)


class UndoItem:
    def __init__(self, remove, add):
        """ An action to undo something
        remove: how many items this will remove
        add: the list of items it will add """
        self.remove = remove
        self.add = add

    def apply(self, stack):
        if self.remove > 0:
            del stack[-self.remove:]
        stack.extend(self.add)


def multiply_function(items):
    items = items + [1, 1]
    return [items[0]*items[1]]


# Basic functions
delete = RPNfunction(1, "delete x", lambda x: [])
switch2 = RPNfunction(2, "switch x, y", lambda x: [x[1], x[0]])

addition = RPNfunction(2, "x+y", lambda x: [sum(x)], checkStackSize=False)
subtract = RPNfunction(2, "y-x", lambda x: [x[0]-x[1]])
multiply = RPNfunction(2, "x*y", multiply_function, checkStackSize=False)
divide = RPNfunction(2, "y/x", lambda x: [x[0]/x[1]])

exponent = RPNfunction(2, "y^x", lambda x: [x[0]**x[1]])
square = RPNfunction(1, "x^2", lambda x: [x[0]*x[0]])
sqrt = RPNfunction(1, "sqrt x", lambda x: [math.sqrt(x[0])])
e_power = RPNfunction(1, "e^x", lambda x: [math.exp(x[0])])
log10 = RPNfunction(1, "log10", lambda x: [math.log10(x[0])])
ln = RPNfunction(1, "ln", lambda x: [math.log(x[0])])

mult_inverse = RPNfunction(1, "1/x", lambda x: [1/x[0]])
add_inverse = RPNfunction(1, "-x", lambda x: [-x[0]])

modulo = RPNfunction(2, "y mod x", lambda x: [math.fmod(x[0], x[1])])

# constants
e = RPNfunction(0, "e=2.71...", lambda x: [math.e])
pi = RPNfunction(0, "pi=3.14...", lambda x: [math.pi])


# I like to use exceptions as flow control, and I like to define functions using lambda
# So this is a helper function to let me raise exceptions in lambda:
def raise_(ex):
    raise ex


class IsUndo(Exception):
    pass


class IsQuit(Exception):
    pass


undo = RPNfunction(0, "undo", lambda x: raise_(IsUndo()))
quit = RPNfunction(0, "quit", lambda x: raise_(IsQuit()))
