======
modulo
======

Pure Python library for working with modular arithmetic and congruence classes.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/modulo.svg
   :target: https://badge.fury.io/py/modulo
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/modulo/badge/?version=latest
   :target: https://modulo.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/lapets/modulo/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/lapets/modulo/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/lapets/modulo/badge.svg?branch=master
   :target: https://coveralls.io/github/lapets/modulo?branch=master
   :alt: Coveralls test coverage summary.

Purpose
-------
The library allows users to work with congruence classes (including finite field elements) as objects, with support for many common operations.

Package Installation and Usage
------------------------------
The package is available on `PyPI <https://pypi.org/project/modulo/>`_::

    python -m pip install modulo

The library can be imported in the usual way::

    from modulo import modulo

Examples
^^^^^^^^
This library makes it possible to work with congruence classes (and sets of congruence classes such as finite fields) as objects. A congruence class is defined using a representative integer and a modulus::

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

A set of congruence classes such as a finite field can also be defined. The built-in length function and the membership operator are supported::

    >>> len(modulo(7))
    7
    >>> modulo(3, 7) in modulo(7)
    True

Documentation
-------------
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configuration details)::

    python -m pip install nose coverage
    nosetests --cover-erase

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python modulo/modulo.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    python -m pip install pylint
    pylint modulo

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/lapets/modulo>`_ for this library.

Versioning
----------
Beginning with version 0.2.0, the version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
