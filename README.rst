======
modulo
======

Pure Python library for working with modular arithmetic, congruence classes, and finite fields.

.. image:: https://badge.fury.io/py/modulo.svg
   :target: https://badge.fury.io/py/modulo
   :alt: PyPI version and link.

Purpose
-------
The library allows users to work with congruence classes (or, equivalently, finite field elements) as objects, with support for many common operations.

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install modulo

The library can be imported in the usual way::

    from modulo import modulo

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
