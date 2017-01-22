# ERPN, an RPN calculator
# Copyright (C) 2016 Bart de Waal
# This program is licenced under the GPL version three, see Licence file for details

from numbers import Real
from math import isfinite


class Domain:
    """ A class for domains, allowing you to check if a variable is in a domain.
    The default, non-subclassed version is all real numbers """
    def __init__(self):
        pass

    def __contains__(self, item):
        # Include all real numbers, but not floating point numbers like NaN
        return (isinstance(item, Real) and isfinite(item))

    def __add__(self, item):
        return Union(self, item)

    def __lt__(self, value):
        return self.comparison("__lt__", value)

    def __le__(self, value):
        return self.comparison("__le__", value)

    def __gt__(self, value):
        return self.comparison("__gt__", value)

    def __ge__(self, value):
        return self.comparison("__ge__", value)

    def comparison(self, operator, value):
        subDomain = Comparison(operator, value)
        if type(self) is Domain:
            return subDomain
        else:
            return Intersect(self, subDomain)

    def __sub__(self, other):
        if isinstance(other, set) or isinstance(other, frozenset):
            return Minus(self, SetDomain(other))
        return Minus(self, other)

    def __repr__(self):
        return "Domain()"


class DomainCombination(Domain):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__,
                                   repr(self.left),
                                   repr(self.right))


class Union(DomainCombination):
    def __contains__(self, item):
        return (item in self.left or item in self.right)


class Intersect(DomainCombination):
    def __contains__(self, item):
        return (item in self.left and item in self.right)


class Minus(DomainCombination):
    def __contains__(self, item):
        return ((item in self.left) and not (item in self.right))


class Comparison(Domain):
    def __init__(self, operator, value):
        """ operator should be a string like "__lt__" or "__gt__" """
        self.value = value
        self.operator = operator

    def __contains__(self, item):
        # Call the comparison operator on the item, and use it on value
        return (getattr(item, self.operator)(self.value))

    def __repr__(self):
        return "Comparison({}, {})".format(self.operator, self.value)


class SetDomain(Domain):
    def __init__(self, values):
        self.set = set(values)

    def __contains__(self, item):
        return item in self.set

    def __add__(self, other):
        if isinstance(other, SetDomain):
            return SetDomain(self.set.union(other.set))
        else:
            return super().__add__(other)

    def __str__(self):
        return self.set.__str__()

    def __repr__(self):
        return "SetDomain({})".format(self.set)


def SingleValue(value):
    return SetDomain([value])


class IntegersDomain(Domain):
    def __contains__(self, value):
        return (isinstance(value, int) or value.is_integer())

    def __repr__(self):
        return "IntegersDomain()"


Reals = Domain()
Integers = IntegersDomain()
