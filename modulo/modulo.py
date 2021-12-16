"""modulo
https://github.com/lapets/modulo

Pure Python library for working with modular arithmetic,
congruence classes, and finite fields.

"""

from egcd import egcd
import doctest


class modulo():
    """
    Class for representing both finite fields and congruence classes
    (depending on the initialization arguments).

    """
    def __init__(self, *args):
        if len(args) not in [1,2]:
            raise TypeError("Must provide either a modulus or an integer and a modulus.")

        self.mod = args[-1]
        if type(self.mod) is not int or self.mod <= 0:
            raise ValueError("Modulus must be a positive integer.")

        self.val = None
        if len(args) == 2:
            self.val = args[0]
            if type(self.val) is not int:
                raise ValueError("Element must be an integer.")
            self.val = self.val % self.mod

    def _cc(self, arg):
        """
        Attempt to convert argument to a congruence class. Raise an appropriate
        error if this is not possible.
        """
        if type(arg) is modulo:
            if arg.val is not None:
                if self.mod == arg.mod:
                    return arg
                else:
                    raise TypeError("Congruence classes do not have the same modulus.")
            else:
                raise TypeError("Expecting a congruence class or integer.")
        elif type(arg) is int:
            return modulo(arg, self.mod)
        else:
            raise TypeError("Expecting a congruence class or integer.")

    def __add__(self, other):
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

    def __radd__(self, other):
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

    def __sub__(self, other):
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

    def __rsub__(self, other):
        """
        Modular subtraction.

        >>> 3 - mod(1, 4)
        modulo(2, 4)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class or integer.")
        other = self._cc(other)
        return modulo((other.val - self.val) % self.mod, self.mod)

    def __mul__(self, other):
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

    def __rmul__(self, other):
        """
        Modular multiplication.

        >>> 3 * mod(2, 7)
        modulo(6, 7)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class or integer.")
        other = self._cc(other)
        return modulo((self.val * other.val) % self.mod, self.mod)

    def __floordiv__(self, other):
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
        else:
            return modulo((self.val * inv) % self.mod, self.mod)

    def __pos__(self):
        """
        Identify function on congruence classes.

        >>> +mod(4, 7)
        modulo(4, 7)
        """
        if self.val is None:
            raise TypeError("Expecting a congruence class.")
        return modulo(self.val, self.mod)

    def __neg__(self):
        """
        Identify function on congruence classes.

        >>> -mod(4, 7)
        modulo(3, 7)
        """
        if self.val is None:
            raise TypeError("Can only negate a congruence class.")
        return modulo((0 - self.val) % self.mod, self.mod)

    def __pow__(self, other, mod = None):
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
        if type(other) is not int:
            raise TypeError("Exponent must be an integer.")
        if mod is not None and mod != self.mod:
            raise ValueError("Modulus does not match congruence class modulus.")

        if other < 0:
            (gcd, inv, _) = egcd(self.val, self.mod)
            if gcd > 1:
                raise ValueError("Congruence class has no inverse.")
            else:
                return modulo(pow(inv % self.mod, 0-other, self.mod), self.mod)
        else:
            return modulo(pow(self.val, other, self.mod), self.mod)

    def __contains__(self, other):
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
            if type(other) is not modulo:
                raise TypeError("Can only check a congruence class for membership in a finite field.")
            else:
                if other.val is None:
                    raise TypeError("Cannot check if finite field is in another finite field.")
                else:
                    return self.mod == other.mod
        else:
            if type(other) is not int:
                raise TypeError("Can only check if an integer is in a congruence class.")
            else:
                return (other % self.mod) == self.val

    def __repr__(self):
        return str(self)

    def __str__(self):
        """
        String representation.
        
        >>> mod(2, 4)
        modulo(2, 4)
        """
        ss = ([] if self.val is None else [str(self.val)]) + [str(self.mod)]
        return "modulo(" + ", ".join(ss) + ")"

    def __int__(self):
        """
        Conversion to the canonical integer representative of a congruence class.
        
        >>> int(mod(2, 4))
        2
        """
        if self.val is None:
            raise TypeError("Can only convert a congruence class to an integer.")
        return self.val

    def __len__(self):
        """
        Number of elements in a set of congruence classes (i.e., a finite field).
        
        >>> len(mod(36))
        36
        """
        if self.val is not None:
            raise TypeError("Cannot compute size of a congruence class.")
        return self.mod


mod = modulo # Synonym.
Z = modulo # Synonym.


if __name__ == "__main__": 
    doctest.testmod()
