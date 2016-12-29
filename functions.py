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


addition = RPNfunction(2, "add 2", lambda x: [sum(x)], checkStackSize=False)


def multiply_function(items):
    items = items + [1, 1]
    return [items[0]*items[1]]


multiply = RPNfunction(2, "multiply 2", multiply_function, checkStackSize=False)

subtract = RPNfunction(2, "y-x", lambda x: [x[-2]-x[-1]])

divide = RPNfunction(2, "y/x", lambda x: [x[-2]/x[-1]])

delete = RPNfunction(1, "delete 1", lambda x: [])

# I like to use exceptions as flow control, and I like to define functions using lambda
# So this is a helper function to let me raise exceptions in lambda:


def raise_(ex):
    raise ex


class IsUndo(Exception):
    pass


undo = RPNfunction(0, "undo", lambda x: raise_(IsUndo()))
