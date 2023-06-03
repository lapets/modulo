"""
Pure-Python library for working with modular arithmetic, congruence classes,
and finite fields.
"""
from __future__ import annotations
from typing import Union, Sequence
from collections.abc import Iterable
import doctest
from math import gcd
from egcd import egcd

class _symbol(type): # pylint: disable=invalid-name # Private/internal class.
    """
    Metaclass to enable the use of a class as a mathematical symbol within
    expressions.
    """
    def __new__(mcs, clsname, bases, attrs):
        return super(_symbol, mcs).__new__(mcs, clsname, bases, attrs)

    def __rmul__(cls: _symbol, other: int) -> modulo:
        """
        Enable use of the :obj:`modulo` class and its synonyms as a
        mathematical symbol, enabling construction of congruence class
        instances via a concise and familiar notation.

        >>> 4*Z
        modulo(0, 4)
        >>> 1.23 * Z
        Traceback (most recent call last):
          ...
        TypeError: left-hand argument must be an integer
        >>> -2 * Z
        Traceback (most recent call last):
          ...
        ValueError: left-hand argument must be a positive integer
        """
        if not isinstance(other, int):
            raise TypeError('left-hand argument must be an integer')

        if other <= 0:
            raise ValueError('left-hand argument must be a positive integer')

        return modulo(0, other)

    def __truediv__(cls: _symbol, other: modulo) -> modulo:
        """
        Enable use of the :obj:`modulo` class and its synonyms as a
        mathematical symbol, enabling construction of sets of congruence
        classes via a concise and familiar notation.

        >>> Z/(4*Z)
        modulo(4)
        >>> Z/(1 + 4*Z)
        Traceback (most recent call last):
          ...
        ValueError: right-hand argument must be a congruence class represented by 0
        >>> Z/1.23
        Traceback (most recent call last):
          ...
        TypeError: right-hand argument must be a congruence class
        """
        if not isinstance(other, modulo):
            raise TypeError('right-hand argument must be a congruence class')

        if other.residue != 0:
            raise ValueError('right-hand argument must be a congruence class represented by 0')

        return modulo(other.modulus)

class modulo(metaclass=_symbol):
    # pylint: disable=anomalous-backslash-in-string # Allow backslashes in docstring.
    """
    Class for representing both *individual congruence classes* (*e.g.*, finite
    field elements) and *sets of congruence classes* (*e.g.*, rings and finite
    fields such as **Z**/7\ **Z**). Common arithmetic and membership operations
    are supported for each, as appropriate.

    When two integer arguments are supplied, the created instance represents
    the individual congruence class corresponding to the remainder of the
    first argument modulo the second argument. The instance ``modulo(3, 7)``
    in the example below represents the congruence class 3 in the set
    **Z**/7\ **Z**. Note that **the synonym** :obj:`mod` **is made available to
    support more concise notation and is used throughout this documentation.**

    >>> mod(3, 7)
    modulo(3, 7)

    Common modular arithmetic operations and the membership operator (via the
    special method :obj:`modulo.__contains__`) are supported for congruence
    class instances.

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

    Use of the membership operation is also supported for individual congruence
    classes that are themselves members of a set of congruence classes.

    >>> mod(3, 7) in mod(7)
    True
    >>> mod(1, 2) in mod(7)
    False

    The built-in :obj:`int` function can be used to retrieve the least nonnegative
    residue of an instance (see :obj:`modulo.__int__`) and the built-in :obj:`len`
    function can be used to retrieve the modulus of an instance (see
    :obj:`modulo.__len__`).

    >>> c = modulo(3, 7)
    >>> int(c)
    3
    >>> len(c)
    7

    Congruence classes and sets of congruence classes are also hashable (making
    it possible to use them as dictionary keys and as set members) and iterable.

    >>> list(mod(4))
    [modulo(0, 4), modulo(1, 4), modulo(2, 4), modulo(3, 4)]
    >>> len({mod(0, 3), mod(1, 3), mod(2, 3)})
    3
    >>> from itertools import islice
    >>> list(islice(mod(3, 7), 5))
    [3, 10, 17, 24, 31]

    The `Chinese remainder theorem <https://en.wikipedia.org/wiki/Chinese_remainder_theorem>`__
    can be applied to construct the intersection of two congruence classes as a
    congruence class (when it is possible to do so).

    >>> mod(23, 100) & mod(31, 49)
    modulo(423, 4900)
    >>> mod(2, 10) & mod(4, 20) is None
    True

    Special methods such as :obj:`modulo.__getitem__` and synonyms such as
    :obj:`Z` make it possible to use a number of different forms of notation
    for creating congruence classes and sets thereof.

    >>> Z/(23*Z)
    modulo(23)
    >>> 23*Z
    modulo(0, 23)
    >>> 17 + 23*Z
    modulo(17, 23)
    >>> 17 % mod(23)
    modulo(17, 23)
    >>> cs = mod(23)
    >>> cs[17]
    modulo(17, 23)

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
    ValueError: residue must be an integer
    """
    def __init__(self: modulo, *args: Union[int, Sequence[int]]):
        """
        Create an instance of a set of congruence classes (*e.g.*, a finite field)
        or an individual congruence class.
        """
        if len(args) not in [1, 2]:
            raise TypeError('must provide either a modulus or an integer and a modulus')

        self.modulus = args[-1]
        if not isinstance(self.modulus, int) or self.modulus <= 0:
            raise ValueError('modulus must be a positive integer')

        self.residue = None
        if len(args) == 2:
            self.residue = args[0]
            if not isinstance(self.residue, int):
                raise ValueError('residue must be an integer')
            self.residue = self.residue % self.modulus

    def _cc(self: modulo, arg: Union[modulo, int]) -> modulo:
        """
        Attempt to convert the supplied argument to a congruence class. Raise an
        appropriate exception if this is not possible.
        """
        if isinstance(arg, modulo):
            if arg.residue is not None:
                if self.modulus == arg.modulus:
                    return arg
                raise ValueError('congruence classes do not have the same modulus')
            raise TypeError('expecting a congruence class or integer')

        if isinstance(arg, int):
            return modulo(arg, self.modulus)

        raise TypeError('expecting a congruence class or integer')

    def _comparable(self: modulo, other: modulo):
        """
        Confirm that the two inputs are comparable; raise an exception if they are not.
        """
        if not isinstance(other, modulo):
            raise TypeError('expecting a congruence class')

        if self.residue is None or other.residue is None:
            raise ValueError('sets of congruence classes cannot be compared')

        if self.modulus != other.modulus:
            raise ValueError('congruence classes do not have the same modulus')

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
        return hash((self.residue, self.modulus))

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
        ValueError: congruence classes do not have the same modulus
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
        if self.residue is None:
            raise TypeError('expecting a congruence class or integer')

        other = self._cc(other)
        return modulo((self.residue + other.residue) % self.modulus, self.modulus)

    def __radd__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        If this instance is a congruence class, perform modular addition of
        congruence classes (even if the left-hand argument is an integer
        and/or representative of a congruence class).

        >>> mod(1, 4) + mod(2, 4)
        modulo(3, 4)
        >>> 2 + mod(1, 4)
        modulo(3, 4)

        If this instance is a set of congruence classes, support use of
        familiar mathematical notation to construct congruence classes.

        >>> 2 + mod(4)
        modulo(2, 4)
        >>> 2 + 4*Z
        modulo(2, 4)
        """
        if self.residue is None:
            return modulo(other, self.modulus)

        other = self._cc(other)
        return modulo((self.residue + other.residue) % self.modulus, self.modulus)

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
        if self.residue is None:
            raise TypeError('expecting a congruence class or integer')

        other = self._cc(other)
        return modulo((self.residue - other.residue) % self.modulus, self.modulus)

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
        if self.residue is None:
            raise TypeError('expecting a congruence class or integer')

        other = self._cc(other)
        return modulo((other.residue - self.residue) % self.modulus, self.modulus)

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
        if self.residue is None:
            raise TypeError('expecting a congruence class')

        return modulo(self.residue, self.modulus)

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
        if self.residue is None:
            raise TypeError('can only negate a congruence class')

        return modulo((0 - self.residue) % self.modulus, self.modulus)

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
        if self.residue is None:
            raise TypeError('expecting a congruence class or integer')

        other = self._cc(other)
        return modulo((self.residue * other.residue) % self.modulus, self.modulus)

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
        if self.residue is None:
            raise TypeError('expecting a congruence class or integer')

        other = self._cc(other)
        return modulo((self.residue * other.residue) % self.modulus, self.modulus)

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
        if self.residue is None:
            raise TypeError('expecting a congruence class or integer')

        other = self._cc(other)
        (gcd_, inv, _) = egcd(other.residue, self.modulus)
        if gcd_ > 1:
            raise ValueError('congruence class has no inverse')

        return modulo((self.residue * inv) % self.modulus, self.modulus)

    def __pow__(
            self: modulo,
            other: Union[int, modulo],
            modulo: int = None # pylint: disable=redefined-outer-name # Parameter from Python docs.
        ) -> modulo:
        """
        Perform modular exponentiation (including inversion, if the supplied
        exponent is negative).

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

        The exponent can be an integer or an instance of :obj:`modulo`. The
        latter option can enable concise notation when exponent values are
        treated as elements within their own group (such as when leveraging
        `Euler's theorem <https://en.wikipedia.org/wiki/Euler%27s_theorem>`__).

        >>> pow(mod(4, 7), mod(2, 6)) * pow(mod(4, 7), mod(4, 6))
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
        TypeError: exponent must be an integer or congruence class
        >>> pow(mod(4, 7), 3, 8)
        Traceback (most recent call last):
          ...
        ValueError: modulus does not match congruence class modulus
        >>> pow(mod(4, 6), -1, 6)
        Traceback (most recent call last):
          ...
        ValueError: congruence class has no inverse
        """
        # Support the parameter ``modulo`` as it appears in the Python documentation,
        # but restore the module-specific naming convention within the remainder of
        # the body of this method.
        modulus = modulo
        modulo = mod

        if self.residue is None:
            raise TypeError('can only exponentiate a congruence class')

        if not isinstance(other, (int, modulo)):
            raise TypeError('exponent must be an integer or congruence class')

        if modulus is not None and modulus != self.modulus:
            raise ValueError('modulus does not match congruence class modulus')

        base = self.residue

        if isinstance(other, int) and other < 0:
            (gcd_, inv, _) = egcd(self.residue, self.modulus)
            if gcd_ > 1:
                raise ValueError('congruence class has no inverse')

            base = inv % self.modulus
            other = 0 - other

        if isinstance(other, modulo):
            other = int(other)

        return modulo(pow(base, other, self.modulus), self.modulus)

    def __invert__(self: modulo) -> modulo:
        """
        Return the multiplicative inverse of a congruence class.

        >>> ~mod(4, 7)
        modulo(2, 7)

        Any attempt to invoke the operator on an instance that lacks the required
        properties (*e.g.*, a congruence class that is not invertible) raises an
        exception.

        >>> ~mod(4, 6)
        Traceback (most recent call last):
          ...
        ValueError: congruence class has no inverse
        """
        return self ** (-1)

    def __mod__(self: modulo, other: int) -> modulo:
        """
        If this instance is a congruence class, return a congruence class with
        a modified modulus attribute.

        >>> mod(3, 10) % 7
        modulo(3, 7)
        >>> mod(11, 23) % 2
        modulo(1, 2)

        This operation is only defined for congruence classes and the second
        argument must be an integer.

        >>> mod(10) % 2
        Traceback (most recent call last):
          ...
        ValueError: modulus cannot be modified for a set of congruence classes
        >>> mod(3, 10) % 1.23
        Traceback (most recent call last):
          ...
        TypeError: right-hand argument must be an integer
        """
        if self.residue is None:
            raise ValueError('modulus cannot be modified for a set of congruence classes')

        if not isinstance(other, int):
            raise TypeError('right-hand argument must be an integer')

        return modulo(self.residue, other)

    def __rmod__(self: modulo, other: int) -> modulo:
        """
        If this instance is a set of congruence classes, construct a congruence class
        corresponding to the supplied integer.

        >>> 7 % mod(11)
        modulo(7, 11)

        This operation is only defined for a set of congruence classes.

        >>> 7 % mod(3, 11)
        Traceback (most recent call last):
          ...
        ValueError: expecting a set of congruence classes as the second argument
        >>> 1.23 % mod(11)
        Traceback (most recent call last):
          ...
        TypeError: left-hand argument must be an integer
        """
        if self.residue is not None:
            raise ValueError('expecting a set of congruence classes as the second argument')

        if not isinstance(other, int):
            raise TypeError('left-hand argument must be an integer')

        return modulo(other, self.modulus)

    def __truediv__(self: modulo, other: int) -> modulo:
        """
        Transform a congruence class into a related congruence class that is
        obtained by dividing both the residue and the modulus by the same positive
        integer.

        >>> mod(2, 10) / 2
        modulo(1, 5)

        Only a congruence class can be transformed, and both the residue and modulus
        must be divisible by the supplied integer.

        >>> mod(4) / 2
        Traceback (most recent call last):
          ...
        ValueError: can only transform a congruence class
        >>> mod(3, 4) / 2
        Traceback (most recent call last):
          ...
        ValueError: residue and modulus must both be divisible by the supplied integer
        >>> mod(3, 9) / 3.0
        Traceback (most recent call last):
          ...
        TypeError: second argument must be an integer

        This method is made available primarily for use in applying the Chinese
        remainder theorem (*e.g.*, as is done in :obj:`modulo.__and__`) and
        similar processes.
        """
        if self.residue is None:
            raise ValueError('can only transform a congruence class')

        if not isinstance(other, int):
            raise TypeError('second argument must be an integer')

        if gcd(self.residue, other) != other or gcd(self.modulus, other) != other:
            raise ValueError('residue and modulus must both be divisible by the supplied integer')

        return modulo(self.residue // other, self.modulus // other)

    def __and__(self: modulo, other: modulo) -> Union[modulo, set, None]:
        """
        Return the intersection of two congruence classes, represented as a
        congruence class. The result is constructed via an application of the
        `Chinese remainder theorem <https://en.wikipedia.org/wiki/Chinese_remainder_theorem>`__).

        >>> mod(2, 3) & mod(4, 5)
        modulo(14, 15)
        >>> mod(1, 10) & mod(1, 14)
        modulo(1, 70)
        >>> mod(2, 10) & mod(2, 14)
        modulo(2, 70)
        >>> mod(23, 100) & mod(31, 49)
        modulo(423, 4900)
        >>> mod(2, 10) & mod(4, 20) is None
        True

        The example below compares the outputs from this method (across a range of
        inputs) with the results of an exhaustive search. Note the use of congruence
        class instances as iterables (via :obj:`modulo.__iter__`).

        >>> from itertools import islice
        >>> all(
        ...     int(modulo(a, m) & modulo(b, n)) in (
        ...         set(islice(modulo(a, m), 20)) & set(islice(modulo(b, n), 20))
        ...     )
        ...     for m in range(1, 20) for a in range(m)
        ...     for n in range(1, 20) for b in range(n)
        ...     if (a % gcd(m, n) == b % gcd(m, n))
        ... )
        True
        >>> all(
        ...     (modulo(a, m) & modulo(b, n) is None) and (
        ...         set(islice(modulo(a, m), 20)) & set(islice(modulo(b, n), 20)) == set()
        ...     )
        ...     for m in range(1, 20) for a in range(m)
        ...     for n in range(1, 20) for b in range(n)
        ...     if (a % gcd(m, n) != b % gcd(m, n))
        ... )
        True

        Both arguments must be congruence classes.

        >>> mod(2, 3) & mod(7)
        Traceback (most recent call last):
          ...
        ValueError: intersection operation is only defined for two congruence classes
        >>> mod(2, 3) & 1.23
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class
        """
        if not isinstance(other, modulo):
            raise TypeError('expecting a congruence class')

        if self.residue is None or other.residue is None:
            raise ValueError(
                'intersection operation is only defined for two congruence classes'
            )

        g = gcd(self.modulus, other.modulus)
        modulus = (self.modulus * other.modulus) // g
        r = self.residue % g

        if other.residue % g != r:
            return None

        other_mod = modulo(other.modulus, self.modulus) / g
        self_mod = modulo(self.modulus, other.modulus) / g
        return modulo(
            r + (g * (
                (((self.residue - r) // g) * (other.modulus // g) * int(~other_mod)) + \
                (((other.residue - r) // g) * (self.modulus // g) * int(~self_mod))
            )),
            modulus
        )

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

        Both arguments must be congruence classes or sets thereof.

        >>> modulo(2, 3) == 2
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or set of congruence classes
        """
        if not isinstance(other, modulo):
            raise TypeError('expecting a congruence class or set of congruence classes')

        return (
            self.modulus == other.modulus and \
            (self.residue == other.residue or (self.residue is None and other.residue is None))
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

        Both arguments must be congruence classes or sets thereof.

        >>> modulo(2, 3) != 2
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class or set of congruence classes
        """
        return not self == other

    def __lt__(self: modulo, other: modulo) -> bool:
        """
        Allow comparison and sorting of congruence classes (according to their
        least nonnegative residues).

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

        Congruence classes with different moduli, sets of congruence classes,
        and other incompatible objects cannot be compared.

        >>> mod(2, 3) < mod(1, 4)
        Traceback (most recent call last):
          ...
        ValueError: congruence classes do not have the same modulus
        >>> mod(3) < mod(5)
        Traceback (most recent call last):
          ...
        ValueError: sets of congruence classes cannot be compared
        >>> mod(3) < 5
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class
        """
        self._comparable(other)
        return self.residue < other.residue

    def __le__(self: modulo, other: modulo) -> bool:
        """
        Allow comparison and sorting of congruence classes (according to their
        least nonnegative residues).

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
        """
        self._comparable(other)
        return self.residue <= other.residue

    def __gt__(self: modulo, other: modulo) -> bool:
        """
        Allow comparison and sorting of congruence classes (according to their
        least nonnegative residues).

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
        """
        self._comparable(other)
        return self.residue > other.residue

    def __ge__(self: modulo, other: modulo) -> bool:
        """
        Allow comparison and sorting of congruence classes (according to their
        least nonnegative residues).

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
        """
        self._comparable(other)
        return self.residue >= other.residue

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
        TypeError: can only check if a congruence class is a member of a set of congruence classes
        >>> mod(4) in mod(4)
        Traceback (most recent call last):
          ...
        TypeError: can only check if a congruence class is a member
        >>> 'a' in mod(7)
        Traceback (most recent call last):
          ...
        TypeError: can only check if a congruence class is a member of a set of congruence classes
        >>> 'a' in mod(4, 7)
        Traceback (most recent call last):
          ...
        TypeError: can only check if an integer is a member of a congruence class
        """
        if self.residue is None:
            if not isinstance(other, modulo):
                raise TypeError(
                    'can only check if a congruence class is a member of a set of ' + \
                    'congruence classes'
                )

            if other.residue is None:
                raise TypeError('can only check if a congruence class is a member')

            return self.modulus == other.modulus

        if not isinstance(other, int):
            raise TypeError(
                'can only check if an integer is a member of a congruence class'
            )

        return (other % self.modulus) == self.residue

    def issubset(self: modulo, other: modulo) -> bool:
        """
        Return a boolean value indicating whether a congruence class of integers
        is a subset of another congruence class of integers.

        >>> mod(2, 8).issubset(mod(2, 4))
        True
        >>> mod(6, 8).issubset(mod(2, 4))
        True
        >>> mod(3, 4).issubset(mod(0, 2))
        False

        Only pairs of congruence classes can be compared using this method.

        >>> mod(6).issubset(mod(2, 4))
        Traceback (most recent call last):
          ...
        ValueError: subset relationship is only defined between congruence classes
        >>> mod(2, 8).issubset(mod(4))
        Traceback (most recent call last):
          ...
        ValueError: subset relationship is only defined between congruence classes
        >>> mod(2, 8).issubset(4)
        Traceback (most recent call last):
          ...
        TypeError: expecting a congruence class
        """
        if not isinstance(other, modulo):
            raise TypeError('expecting a congruence class')

        if self.residue is None or other.residue is None:
            raise ValueError(
                'subset relationship is only defined between congruence classes'
            )

        return (self.residue % other.modulus) == other.residue

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
        if self.residue is not None:
            member = self.residue
            while True:
                yield member
                member += self.modulus

        for c in range(0, self.modulus):
            yield modulo(c, self.modulus)

    def __getitem__(self: modulo, index: int) -> Union[modulo, int]:
        """
        Allow efficient retrieval of individual members of a congruence class
        or set of congruence classes.

        >>> cs = modulo(7)
        >>> cs[2]
        modulo(2, 7)
        >>> cs[-2]
        modulo(5, 7)
        >>> c = modulo(2, 7)
        >>> c[0]
        2
        >>> c[-1]
        -5
        >>> c[2]
        16

        The supplied index must be an integer.

        >>> c['a']
        Traceback (most recent call last):
          ...
        TypeError: index must be an integer
        """
        if not isinstance(index, int):
            raise TypeError('index must be an integer')

        return (
            modulo(index, self.modulus)
            if self.residue is None else
            self.residue + index * self.modulus
        )

    def __len__(self: modulo) -> int:
        """
        Return the number of elements in a set of congruence classes
        (*e.g.*, a ring or finite field) or the modulus for a congruence
        class.

        >>> len(mod(36))
        36
        >>> len(mod(2, 4))
        4

        Use of the built-in :obj:`len` function is the recommended approach
        for retrieving the ``modulus`` attribute of a :obj:`modulo` instance.
        """
        return self.modulus

    def __int__(self: modulo) -> int:
        """
        Return the least nonnegative residue (*i.e.*, the canonical integer
        representative) of an instance that represents a congruence class.

        >>> int(mod(2, 4))
        2

        A set of congruence classes (*e.g.*, a finite field) cannot be represented
        as a single integer.

        >>> int(mod(4))
        Traceback (most recent call last):
          ...
        TypeError: can only convert a congruence class to an integer

        Use of the built-in :obj:`int` function is the recommended approach
        for retrieving the ``residue`` attribute of a :obj:`modulo` instance.
        """
        if self.residue is None:
            raise TypeError('can only convert a congruence class to an integer')

        return self.residue

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
        ss = ([] if self.residue is None else [str(self.residue)]) + [str(self.modulus)]
        return 'modulo(' + ', '.join(ss) + ')'

mod: type = modulo
"""
Alias for :obj:`modulo`.
"""

Z: type = modulo
"""
Alias for :obj:`modulo`.
"""

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
