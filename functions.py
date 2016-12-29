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
        self.checkStackSize = checkStackSize

    def run(self, stack):
        """ Run the function on the stack """
        if self.checkStackSize and len(stack) < self.args:
            raise StackToSmallError()
        toAdd = self.function(stack[-self.args:])
        del stack[-self.args:]
        stack.extend(toAdd)


addition = RPNfunction(2, "add 2", lambda x: [sum(x)], checkStackSize=False)


def multiply_function(items):
    items = items + [1, 1]
    return [items[0]*items[1]]


multiply = RPNfunction(2, "multiply 2", multiply_function, checkStackSize=False)

subtract = RPNfunction(2, "y-x", lambda x: [x[-2]-x[-1]])

divide = RPNfunction(2, "y/x", lambda x: [x[-2]/x[-1]])

delete = RPNfunction(1, "delete 1", lambda x: [])
