"""
Pure Python library for working with modular arithmetic,
congruence classes, and finite fields.
"""
from __future__ import annotations
from typing import Union
import doctest
from egcd import egcd

class modulo: # pylint: disable=C0103
    """
    Class for representing both finite fields and congruence classes
    (depending on the initialization arguments).
    """
    def __init__(self: modulo, *args):
        if len(args) not in [1, 2]:
            raise TypeError("Must provide either a modulus or an integer and a modulus.")

        self.mod = args[-1]
        if not isinstance(self.mod, int) or self.mod <= 0:
            raise ValueError("Modulus must be a positive integer.")

        self.val = None
        if len(args) == 2:
            self.val = args[0]
            if not isinstance(self.val, int):
                raise ValueError("Element must be an integer.")
            self.val = self.val % self.mod

    def _cc(self: modulo, arg: Union[modulo, int]) -> modulo:
        """
        Attempt to convert argument to a congruence class. Raise an appropriate
        error if this is not possible.
        """
        if isinstance(arg, modulo):
            if arg.val is not None:
                if self.mod == arg.mod:
                    return arg
                raise TypeError("Congruence classes do not have the same modulus.")
            raise TypeError("Expecting a congruence class or integer.")

        if isinstance(arg, int):
            return modulo(arg, self.mod)

        raise TypeError("Expecting a congruence class or integer.")

    def __add__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        Modular addition.

        >>> mod(1, 4) + mod(2, 4)
        modulo(3, 4)
        >>> mod(1, 4) + 2
        modulo(3, 4)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class or integer.")

        other = self._cc(other)
        return modulo((self.val + other.val) % self.mod, self.mod)

    def __radd__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        Modular addition.

        >>> mod(1, 4) + mod(2, 4)
        modulo(3, 4)
        >>> 2 + mod(1, 4)
        modulo(3, 4)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class or integer.")

        other = self._cc(other)
        return modulo((self.val + other.val) % self.mod, self.mod)

    def __sub__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        Modular subtraction.

        >>> mod(1, 4) - mod(2, 4)
        modulo(3, 4)
        >>> mod(1, 4) - 3
        modulo(2, 4)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class or integer.")

        other = self._cc(other)
        return modulo((self.val - other.val) % self.mod, self.mod)

    def __rsub__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        Modular subtraction.

        >>> 3 - mod(1, 4)
        modulo(2, 4)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class or integer.")

        other = self._cc(other)
        return modulo((other.val - self.val) % self.mod, self.mod)

    def __mul__(self, other: Union[modulo, int]) -> modulo:
        """
        Modular multiplication.

        >>> mod(1, 4) * mod(2, 4)
        modulo(2, 4)
        >>> mod(2, 7) * 3
        modulo(6, 7)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class or integer.")

        other = self._cc(other)
        return modulo((self.val * other.val) % self.mod, self.mod)

    def __rmul__(self, other: Union[modulo, int]) -> modulo:
        """
        Modular multiplication.

        >>> 3 * mod(2, 7)
        modulo(6, 7)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class or integer.")

        other = self._cc(other)
        return modulo((self.val * other.val) % self.mod, self.mod)

    def __floordiv__(self: modulo, other: Union[modulo, int]) -> modulo:
        """
        Modular division.

        >>> mod(4, 7) // mod(2, 7)
        modulo(2, 7)
        >>> mod(6, 17) // mod(3, 17)
        modulo(2, 17)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class or integer.")

        other = self._cc(other)
        (gcd, inv, _) = egcd(other.val, self.mod)
        if gcd > 1:
            raise ValueError("Congruence class has no inverse.")

        return modulo((self.val * inv) % self.mod, self.mod)

    def __pos__(self: modulo) -> modulo:
        """
        Identify function on congruence classes.

        >>> +mod(4, 7)
        modulo(4, 7)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class.")

        return modulo(self.val, self.mod)

    def __neg__(self: modulo) -> modulo:
        """
        Identify function on congruence classes.

        >>> -mod(4, 7)
        modulo(3, 7)
        """
        if self.val is None:
            raise TypeError("Can only negate a congruence class.")

        return modulo((0 - self.val) % self.mod, self.mod)

    def __pow__(self: modulo, other: int, mod: int = None) -> modulo: # pylint: disable=W0621
        """
        Modular exponentiation.

        >>> mod(4, 7) ** 3
        modulo(1, 7)
        >>> pow(mod(4, 7), 3)
        modulo(1, 7)
        >>> pow(mod(4, 7), 3, 7)
        modulo(1, 7)
        """
        if self.val is None:
            raise TypeError("Can only exponentiate a congruence class.")

        if not isinstance(other, int):
            raise TypeError("Exponent must be an integer.")

        if mod is not None and mod != self.mod:
            raise ValueError("Modulus does not match congruence class modulus.")

        if other < 0:
            (gcd, inv, _) = egcd(self.val, self.mod)
            if gcd > 1:
                raise ValueError("Congruence class has no inverse.")

            return modulo(pow(inv % self.mod, 0-other, self.mod), self.mod)

        return modulo(pow(self.val, other, self.mod), self.mod)

    def __contains__(self: modulo, other: Union[modulo, int]) -> bool:
        """
        Membership function for integers, congruence classes, and finite fields.

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
        """
        if self.val is None:
            if not isinstance(other, modulo):
                raise TypeError(
                    "Can only check a congruence class for membership in a finite field."
                )

            if other.val is None:
                raise TypeError("Cannot check if finite field is in another finite field.")

            return self.mod == other.mod

        if not isinstance(other, int):
            raise TypeError("Can only check if an integer is in a congruence class.")

        return (other % self.mod) == self.val

    def __repr__(self: modulo) -> str:
        return str(self)

    def __str__(self: modulo) -> str:
        """
        String representation.

        >>> mod(2, 4)
        modulo(2, 4)
        """
        ss = ([] if self.val is None else [str(self.val)]) + [str(self.mod)]
        return "modulo(" + ", ".join(ss) + ")"

    def __int__(self: modulo) -> int:
        """
        Conversion to the canonical integer representative of a congruence class.

        >>> int(mod(2, 4))
        2
        """
        if self.val is None:
            raise TypeError("Can only convert a congruence class to an integer.")

        return self.val

    def __len__(self: modulo) -> int:
        """
        Number of elements in a set of congruence classes (i.e., a finite field).

        >>> len(mod(36))
        36
        """
        if self.val is not None:
            raise TypeError("Cannot compute size of a congruence class.")

        return self.mod

mod = modulo # Synonym. # pylint: disable=C0103
Z = modulo # Synonym. # pylint: disable=C0103

if __name__ == "__main__":
    doctest.testmod()
