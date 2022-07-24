======
modulo
======

Pure-Python library for working with modular arithmetic, congruence classes, and finite fields.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/modulo.svg
   :target: https://badge.fury.io/py/modulo
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/modulo-lib/badge/?version=latest
   :target: https://modulo-lib.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/lapets/modulo/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/lapets/modulo/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/lapets/modulo/badge.svg?branch=main
   :target: https://coveralls.io/github/lapets/modulo?branch=main
   :alt: Coveralls test coverage summary.

Purpose
-------
The library allows users to work with congruence classes (including finite field elements) as objects, with support for many common operations.

Installation and Usage
----------------------
This library is available as a `package on PyPI <https://pypi.org/project/modulo>`__::

    python -m pip install modulo

The library can be imported in the usual way::

    from modulo import modulo

Examples
^^^^^^^^
This library makes it possible to work with `congruence classes <https://en.wikipedia.org/wiki/Congruence_relation>`__ (and sets of congruence classes such as finite fields) as objects. A congruence class is defined using a representative integer and a modulus::

    >>> from modulo import modulo
    >>> modulo(3, 7)
    modulo(3, 7)

Built-in operators can be used to perform modular addition, modular subtraction, and modular negation of congruence classes::

    >>> modulo(3, 7) + modulo(5, 7)
    modulo(1, 7)
    >>> modulo(1, 7) - modulo(4, 7)
    modulo(4, 7)
    >>> -modulo(5, 7)
    modulo(2, 7)

Modular multiplication, division, inversion, and exponentiation are also supported (when they are defined)::

    >>> modulo(3, 7) * modulo(5, 7)
    modulo(1, 7)
    >>> modulo(1, 7) // modulo(3, 7)
    modulo(5, 7)
    >>> modulo(5, 7) ** 2
    modulo(4, 7)
    >>> modulo(5, 7) ** (-1)
    modulo(3, 7)

Individual congruence classes can be compared with one another according to their least nonnegative residues (and, thus, can also be sorted)::

    >>> mod(2, 7) < mod(3, 7)
    True
    >>> list(sorted([mod(2, 3), mod(1, 3), mod(0, 3)]))
    [modulo(0, 3), modulo(1, 3), modulo(2, 3)]

The membership operation is supported between integers and congruence classes::

    >>> 3 in mod(3, 7)
    True
    >>> 10 in mod(3, 7)
    True
    >>> 4 in mod(3, 7)
    False

.. |len| replace:: ``len``
.. _len: https://docs.python.org/3/library/functions.html#len

A set of congruence classes such as a finite field can also be defined. The built-in length function |len|_ and the membership operator are supported::

    >>> len(modulo(7))
    7
    >>> modulo(3, 7) in modulo(7)
    True

.. |int| replace:: ``int``
.. _int: https://docs.python.org/3/library/functions.html#int

The built-in |int|_ function can be used to retrieve the least nonnegative residue of a congruence class and the built-in |len|_ function can be used to retrieve the modulus of a congruence class or set of congruence classes (this is the recommended approach)::

    >>> c = modulo(3, 7)
    >>> int(c)
    3
    >>> len(c)
    7

Congruence classes and sets of congruence classes are also hashable (making it possible to use them as dictionary keys and as set members) and iterable::

    >>> len({mod(0, 3), mod(1, 3), mod(2, 3)})
    3
    >>> list(mod(4))
    [modulo(0, 4), modulo(1, 4), modulo(2, 4), modulo(3, 4)]
    >>> from itertools import islice
    >>> list(islice(mod(3, 7), 5))
    [3, 10, 17, 24, 31]

The `Chinese remainder theorem <https://en.wikipedia.org/wiki/Chinese_remainder_theorem>`__ can be applied to construct the intersection of two congruence classes as a congruence class (when it is possible to do so)::

    >>> mod(23, 100) & mod(31, 49)
    modulo(423, 4900)
    >>> mod(2, 10) & mod(4, 20) is None
    True

Some familiar forms of notation for referring to congruence classes (and sets thereof) are also supported::

    >>> Z/(23*Z)
    modulo(23)
    >>> 23*Z
    modulo(0, 23)
    >>> 17 + 23*Z
    modulo(17, 23)

Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The ``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__::

    python -m pip install .[docs,lint]

Documentation
^^^^^^^^^^^^^
The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__::

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see the ``pyproject.toml`` file for configuration details)::

    python -m pip install .[test]
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__::

    python src/modulo/modulo.py -v

Style conventions are enforced using `Pylint <https://pylint.pycqa.org>`__::

    python -m pip install .[lint]
    python -m pylint src/modulo

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/lapets/modulo>`__ for this library.

Versioning
^^^^^^^^^^
Beginning with version 0.2.0, the version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/modulo>`__ by a package maintainer. First, install the dependencies required for packaging and publishing::

    python -m pip install .[publish]

Ensure that the correct version number appears in ``pyproject.toml``, and that any links in this README document to the Read the Docs documentation of this package (or its dependencies) have appropriate version numbers. Also ensure that the Read the Docs project for this library has an `automation rule <https://docs.readthedocs.io/en/stable/automation-rules.html>`__ that activates and sets as the default all tagged versions. Create and push a tag for this version (replacing ``?.?.?`` with the version number)::

    git tag ?.?.?
    git push origin ?.?.?

Remove any old build/distribution files. Then, package the source into a distribution archive::

    rm -rf build dist src/*.egg-info
    python -m build --sdist --wheel .

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__::

    python -m twine upload dist/*
