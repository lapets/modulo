"""
Pure-Python library for working with modular arithmetic, congruence classes,
and finite fields.
"""
from __future__ import annotations
from typing import Union
from collections.abc import Iterable
import doctest
from egcd import egcd

class modulo:
    # pylint: disable=C0103,W1401 # Accommodate class name and backslash notation in docstring.
    """
    Class for representing both *individual congruence classes* (*e.g.*, finite
    field elements) and *sets of congruence classes* (*e.g.*, rings and finite
    fields such as **Z**/7\ **Z**). Common arithmetic and membership operations
    are supported for each, as appropriate.

    When two integer arguments are supplied, the created instance represents
    the individual congruence class corresponding to the remainder of the
    first argument modulo the second argument. The instance ``mod(3, 7)``
    in the example below represents the congruence class 3 in the set
    **Z**/7\ **Z**.

    >>> mod(3, 7)
    modulo(3, 7)

    Common modular arithmetic operations and the membership operator (via the
    method :obj:`__contains__`) are supported for congruence class instances.

    >>> mod(3, 7) + mod(2, 7)
    modulo(5, 7)
    >>> mod(0, 7) - mod(1, 7)
    modulo(6, 7)
    >>> mod(3, 7) * mod(2, 7)
    modulo(6, 7)
    >>> mod(3, 7) ** (-1)
    modulo(5, 7)
    >>> mod(3, 7) in mod(7)
    True
    >>> int(mod(3, 7))
    3
    >>> 3 in mod(3, 7)
    True
    >>> 10 in mod(3, 7)
    True
    >>> 4 in mod(3, 7)
    False

    Individual congruence classes can be compared with one another according to
    their least nonnegative residues (and, thus, can also be sorted).

    >>> mod(2, 7) < mod(3, 7)
    True
    >>> list(sorted([mod(2, 3), mod(1, 3), mod(0, 3)]))
    [modulo(0, 3), modulo(1, 3), modulo(2, 3)]

    When one integer argument is supplied, the created instance represents the
    set containing the congruence classes modulo that integer. The instance
    ``mod(7)`` in the example below represents the set **Z**/7\ **Z**.

    >>> len(mod(7))
    7

    The membership operation for individual congruence classes is supported.

    >>> mod(3, 7) in mod(7)
    True
    >>> mod(1, 2) in mod(7)
    False

    Congruence classes and sets of congruence classes are also hashable (making
    it possible to use them as dictionary keys and as set members) and iterable.

    >>> list(mod(4))
    [modulo(0, 4), modulo(1, 4), modulo(2, 4), modulo(3, 4)]
    >>> len({mod(0, 3), mod(1, 3), mod(2, 3)})
    3
    >>> from itertools import islice
    >>> list(islice(mod(3, 7), 5))
    [3, 10, 17, 24, 31]

    Constructor invocations involving arguments that have incorrect types raise
    exceptions.

    >>> mod()
    Traceback (most recent call last):
      ...
    TypeError: must provide either a modulus or an integer and a modulus
    >>> mod(-2)
    Traceback (most recent call last):
      ...
    ValueError: modulus must be a positive integer
    >>> mod(1.2, 7)
    Traceback (most recent call last):
      ...
    ValueError: element must be an integer
    """
    def __init__(self: modulo, *args):
        """
        Create an instance of a set of congruence classes (*e.g.*, a finite field)
        or an individual congruence class.
        """
        if len(args) not in [1, 2]:
            raise TypeError("must provide either a modulus or an integer and a modulus")

        self.mod = args[-1]
        if not isinstance(self.mod, int) or self.mod <= 0:
            raise ValueError("modulus must be a positive integer")

        self.val = None
        if len(args) == 2:
            self.val = args[0]
            if not isinstance(self.val, int):
                raise ValueError("element must be an integer")
            self.val = self.val % self.mod

    def _cc(self: modulo, arg: Union[modulo, int]) -> modulo:
        """
        Attempt to convert the supplied argument to a congruence class. Raise an
        appropriate exception if this is not possible.
        """
        if isinstance(arg, modulo):
            if arg.val is not None:
                if self.mod == arg.mod:
                    return arg
                raise TypeError("congruence classes do not have the same modulus")
            raise TypeError("expecting a congruence class or integer")

        if isinstance(arg, int):
            return modulo(arg, self.mod)

        raise TypeError("expecting a congruence class or integer")

    def __hash__(self: modulo) -> int:
        """
        Allow use of congruence classes and sets of congruence classes within
        contexts that require hashable objects (*e.g.*, as dictionary keys or
        as elements in sets).

        >>> len({mod(0, 3), mod(1, 3), mod(2, 3)})
        3
        >>> {mod(3)}
        {modulo(3)}
        """
        return hash((self.val, self.mod))

    def __add__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        Perform modular addition.

        >>> mod(1, 4) + mod(2, 4)
        modulo(3, 4)
        >>> mod(1, 4) + 2
        modulo(3, 4)

        Attempts to invoke the operator on arguments having incorrect types raise
        exceptions.

        >>> mod(1, 3) + mod(2, 4)
        Traceback (most recent call last):
          ...
        TypeError: congruence classes do not have the same modulus
        >>> mod(1, 3) + mod(4)
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or integer
        >>> mod(1, 3) + 'a'
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or integer
        >>> mod(4) + 2
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or integer
        """
        if self.val is None:
            raise TypeError("expecting a congruence class or integer")

        other = self._cc(other)
        return modulo((self.val + other.val) % self.mod, self.mod)

    def __radd__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        Perform modular addition.

        >>> mod(1, 4) + mod(2, 4)
        modulo(3, 4)
        >>> 2 + mod(1, 4)
        modulo(3, 4)
        >>> 2 + mod(4)
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or integer
        """
        if self.val is None:
            raise TypeError("expecting a congruence class or integer")

        other = self._cc(other)
        return modulo((self.val + other.val) % self.mod, self.mod)

    def __sub__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        Perform modular subtraction.

        >>> mod(1, 4) - mod(2, 4)
        modulo(3, 4)
        >>> mod(1, 4) - 3
        modulo(2, 4)

        Attempts to invoke the operator on arguments having incorrect types raise
        exceptions.

        >>> mod(4) - 3
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or integer
        """
        if self.val is None:
            raise TypeError("expecting a congruence class or integer")

        other = self._cc(other)
        return modulo((self.val - other.val) % self.mod, self.mod)

    def __rsub__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        Perform modular subtraction.

        >>> 3 - mod(1, 4)
        modulo(2, 4)

        Attempts to invoke the operator on arguments having incorrect types raise
        exceptions.

        >>> 3 - mod(4)
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or integer
        """
        if self.val is None:
            raise TypeError("expecting a congruence class or integer")

        other = self._cc(other)
        return modulo((other.val - self.val) % self.mod, self.mod)

    def __mul__(self, other: Union[modulo, int]) -> modulo:
        """
        Perform modular multiplication.

        >>> mod(1, 4) * mod(2, 4)
        modulo(2, 4)
        >>> mod(2, 7) * 3
        modulo(6, 7)

        Attempts to invoke the operator on arguments having incorrect types raise
        exceptions.

        >>> mod(7) * 3
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or integer
        """
        if self.val is None:
            raise TypeError("expecting a congruence class or integer")

        other = self._cc(other)
        return modulo((self.val * other.val) % self.mod, self.mod)

    def __rmul__(self, other: Union[modulo, int]) -> modulo:
        """
        Perform modular multiplication.

        >>> 3 * mod(2, 7)
        modulo(6, 7)

        Attempts to invoke the operator on arguments having incorrect types raise
        exceptions.

        >>> 3 * mod(7)
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or integer
        """
        if self.val is None:
            raise TypeError("expecting a congruence class or integer")

        other = self._cc(other)
        return modulo((self.val * other.val) % self.mod, self.mod)

    def __floordiv__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        Perform modular division (*i.e.*, multiplication by the inverse).

        >>> mod(4, 7) // mod(2, 7)
        modulo(2, 7)
        >>> mod(6, 17) // mod(3, 17)
        modulo(2, 17)

        Any attempt to divide by a congruence class that is not invertible -- or
        to invoke the operator on arguments that have incorrect types -- raises
        exceptions.

        >>> mod(17) // mod(3, 17)
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or integer
        >>> mod(4, 6) // mod(2, 6)
        Traceback (most recent call last):
          ...
        ValueError: congruence class has no inverse
        """
        if self.val is None:
            raise TypeError("expecting a congruence class or integer")

        other = self._cc(other)
        (gcd, inv, _) = egcd(other.val, self.mod)
        if gcd > 1:
            raise ValueError("congruence class has no inverse")

        return modulo((self.val * inv) % self.mod, self.mod)

    def __pos__(self: modulo) -> modulo:
        """
        Identity function on congruence classes.

        >>> +mod(4, 7)
        modulo(4, 7)

        Any attempt to invoke the operator on an argument having an incorrect
        type raises an exception.

        >>> +mod(4)
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class
        """
        if self.val is None:
            raise TypeError("expecting a congruence class")

        return modulo(self.val, self.mod)

    def __neg__(self: modulo) -> modulo:
        """
        Return the additive inverse of a congruence class.

        >>> -mod(4, 7)
        modulo(3, 7)

        Any attempt to invoke the operator on an argument having an incorrect
        type raises an exception.

        >>> -mod(4)
        Traceback (most recent call last):
          ...
        TypeError: can only negate a congruence class
        """
        if self.val is None:
            raise TypeError("can only negate a congruence class")

        return modulo((0 - self.val) % self.mod, self.mod)

    def __pow__(self: modulo, other: int, mod: int = None) -> modulo: # pylint: disable=W0621
        """
        Perform modular exponentiation.

        >>> mod(4, 7) ** 3
        modulo(1, 7)
        >>> mod(4, 7) ** (-1)
        modulo(2, 7)
        >>> mod(4, 7) ** (-2)
        modulo(4, 7)
        >>> pow(mod(4, 7), 3)
        modulo(1, 7)
        >>> pow(mod(4, 7), 3, 7)
        modulo(1, 7)

        Attempts to invoke the operator on arguments that lack required properties
        (*e.g.*, congruence classes that are not invertible) -- or that have incorrect
        types -- raise an exception.

        >>> pow(mod(7), 3)
        Traceback (most recent call last):
          ...
        TypeError: can only exponentiate a congruence class
        >>> pow(mod(3, 7), 'a')
        Traceback (most recent call last):
          ...
        TypeError: exponent must be an integer
        >>> pow(mod(4, 7), 3, 8)
        Traceback (most recent call last):
          ...
        ValueError: modulus does not match congruence class modulus
        >>> pow(mod(4, 6), -1, 6)
        Traceback (most recent call last):
          ...
        ValueError: congruence class has no inverse
        """
        if self.val is None:
            raise TypeError("can only exponentiate a congruence class")

        if not isinstance(other, int):
            raise TypeError("exponent must be an integer")

        if mod is not None and mod != self.mod:
            raise ValueError("modulus does not match congruence class modulus")

        if other < 0:
            (gcd, inv, _) = egcd(self.val, self.mod)
            if gcd > 1:
                raise ValueError("congruence class has no inverse")

            return modulo(pow(inv % self.mod, 0-other, self.mod), self.mod)

        return modulo(pow(self.val, other, self.mod), self.mod)

    def __eq__(self: modulo, other: modulo) -> bool:
        """
        Return a boolean value indicating whether this instance represents the
        same congruence class or set of congruence classes as the other instance.

        >>> mod(3, 7) == mod(3, 7)
        True
        >>> mod(2, 7) == mod(3, 7)
        False
        >>> mod(4) == mod(4)
        True
        >>> mod(5) == mod(7)
        False
        """
        return (
            self.mod == other.mod and \
            (self.val == other.val or (self.val is None and other.val is None))
        )

    def __ne__(self: modulo, other: modulo) -> bool:
        """
        Return a boolean value indicating whether this instance represents a
        different congruence class (or set of congruence classes) than the
        other instance.

        >>> mod(2, 7) != mod(3, 7)
        True
        >>> mod(3, 7) != mod(3, 7)
        False
        >>> mod(5) != mod(7)
        True
        >>> mod(4) != mod(4)
        False
        """
        return not self == other

    def __lt__(self: modulo, other: modulo) -> bool:
        """
        Allow comparison and sorting of congruence classes (according to their
        canonical nonnegative representative integers).

        >>> mod(2, 7) < mod(3, 7)
        True
        >>> mod(3, 7) < mod(3, 7)
        False
        >>> mod(5, 7) < mod(3, 7)
        False
        >>> mod(9, 7) < mod(3, 7)
        True
        >>> list(sorted([mod(2, 3), mod(1, 3), mod(0, 3)]))
        [modulo(0, 3), modulo(1, 3), modulo(2, 3)]

        Sets of congruence classes cannot be compared.

        >>> mod(3) < mod(5)
        Traceback (most recent call last):
          ...
        ValueError: sets of congruence classes cannot be compared
        """
        if self.val is None or other.val is None:
            raise ValueError("sets of congruence classes cannot be compared")

        return self.val < other.val

    def __le__(self: modulo, other: modulo) -> bool:
        """
        Allow comparison and sorting of congruence classes (according to their
        canonical nonnegative representative integers).

        >>> mod(2, 7) <= mod(3, 7)
        True
        >>> mod(3, 7) <= mod(3, 7)
        True
        >>> mod(5, 7) <= mod(3, 7)
        False
        >>> mod(9, 7) <= mod(3, 7)
        True
        >>> list(sorted([mod(2, 3), mod(1, 3), mod(0, 3)]))
        [modulo(0, 3), modulo(1, 3), modulo(2, 3)]

        Sets of congruence classes cannot be compared.

        >>> mod(3) <= mod(5)
        Traceback (most recent call last):
          ...
        ValueError: sets of congruence classes cannot be compared
        """
        if self.val is None or other.val is None:
            raise ValueError("sets of congruence classes cannot be compared")

        return self.val <= other.val

    def __gt__(self: modulo, other: modulo) -> bool:
        """
        Allow comparison and sorting of congruence classes (according to their
        canonical nonnegative representative integers).

        >>> mod(3, 7) > mod(2, 7)
        True
        >>> mod(3, 7) > mod(3, 7)
        False
        >>> mod(1, 7) > mod(3, 7)
        False
        >>> mod(3, 7) > mod(9, 7)
        True
        >>> list(sorted([mod(2, 3), mod(1, 3), mod(0, 3)]))
        [modulo(0, 3), modulo(1, 3), modulo(2, 3)]

        Sets of congruence classes cannot be compared.

        >>> mod(3) > mod(5)
        Traceback (most recent call last):
          ...
        ValueError: sets of congruence classes cannot be compared
        """
        if self.val is None or other.val is None:
            raise ValueError("sets of congruence classes cannot be compared")

        return self.val > other.val

    def __ge__(self: modulo, other: modulo) -> bool:
        """
        Allow comparison and sorting of congruence classes (according to their
        canonical nonnegative representative integers).

        >>> mod(3, 7) >= mod(2, 7)
        True
        >>> mod(3, 7) >= mod(3, 7)
        True
        >>> mod(1, 7) >= mod(3, 7)
        False
        >>> mod(3, 7) >= mod(9, 7)
        True
        >>> list(sorted([mod(2, 3), mod(1, 3), mod(0, 3)]))
        [modulo(0, 3), modulo(1, 3), modulo(2, 3)]

        Sets of congruence classes cannot be compared.

        >>> mod(3) >= mod(5)
        Traceback (most recent call last):
          ...
        ValueError: sets of congruence classes cannot be compared
        """
        if self.val is None or other.val is None:
            raise ValueError("sets of congruence classes cannot be compared")

        return self.val >= other.val

    def __contains__(self: modulo, other: Union[modulo, int]) -> bool:
        """
        Membership function for integers, congruence classes, and sets of congruence classes.

        >>> 3 in mod(4, 7)
        False
        >>> 4 in mod(4, 7)
        True
        >>> 11 in mod(4, 7)
        True
        >>> mod(4, 7) in mod(7)
        True
        >>> mod(4, 5) in mod(7)
        False

        Attempts to perform invalid membership checks raise exceptions.

        >>> 3 in mod(4)
        Traceback (most recent call last):
          ...
        TypeError: can only check if a congruence class is a member
        >>> mod(4) in mod(4)
        Traceback (most recent call last):
          ...
        TypeError: can only check if a congruence class is a member
        >>> 'a' in mod(7)
        Traceback (most recent call last):
          ...
        TypeError: can only check if a congruence class is a member
        >>> 'a' in mod(4, 7)
        Traceback (most recent call last):
          ...
        TypeError: can only check if an integer is a member of a congruence class
        """
        if self.val is None:
            if (not isinstance(other, modulo)) or (other.val is None):
                raise TypeError(
                    "can only check if a congruence class is a member"
                )

            return self.mod == other.mod

        if not isinstance(other, int):
            raise TypeError(
                "can only check if an integer is a member of a congruence class"
            )

        return (other % self.mod) == self.val

    def __iter__(self: modulo) -> Union[Iterable[int], Iterable[modulo]]:
        """
        Allow iteration over all nonnegative (infinitely many) members (if this
        instance is a congruence class), or all congruence classes (if this
        instance is a set of congruence classes).

        >>> [i for (_, i) in zip(range(5), mod(3, 7))]
        [3, 10, 17, 24, 31]
        >>> list(mod(4))
        [modulo(0, 4), modulo(1, 4), modulo(2, 4), modulo(3, 4)]
        """
        if self.val is not None:
            member = self.val
            while True:
                yield member
                member += self.mod

        for c in range(0, self.mod):
            yield modulo(c, self.mod)

    def __repr__(self: modulo) -> str:
        """
        Return the string representation of this congruence class or set of
        congruence classes.

        >>> mod(2, 4)
        modulo(2, 4)
        >>> mod(7)
        modulo(7)
        """
        return str(self)

    def __str__(self: modulo) -> str:
        """
        Return the string representation of this congruence class or set of
        congruence classes.

        >>> mod(2, 4)
        modulo(2, 4)
        >>> mod(7)
        modulo(7)
        """
        ss = ([] if self.val is None else [str(self.val)]) + [str(self.mod)]
        return "modulo(" + ", ".join(ss) + ")"

    def __int__(self: modulo) -> int:
        """
        Return the canonical integer representative of a congruence class.

        >>> int(mod(2, 4))
        2

        A set of congruence classes (*e.g.*, a finite field) cannot be represented
        as a single integer.

        >>> int(mod(4))
        Traceback (most recent call last):
          ...
        TypeError: can only convert a congruence class to an integer
        """
        if self.val is None:
            raise TypeError("can only convert a congruence class to an integer")

        return self.val

    def __len__(self: modulo) -> int:
        """
        Return the number of elements in a set of congruence classes
        (*e.g.*, a ring or finite field).

        >>> len(mod(36))
        36

        While a congruence class contains an infinite number of integers,
        attempting to determine its size raises an exception.

        >>> len(mod(2, 4))
        Traceback (most recent call last):
          ...
        TypeError: cannot determine size of a congruence class
        """
        if self.val is not None:
            raise TypeError("cannot determine size of a congruence class")

        return self.mod

mod = modulo # pylint: disable=C0103
"""
Alias for :obj:`modulo`.
"""

Z = modulo # pylint: disable=C0103
"""
Alias for :obj:`modulo`.
"""

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
