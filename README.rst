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
The package is available on `PyPI <https://pypi.org/project/modulo/>`_::

    python -m pip install modulo

The library can be imported in the usual way::

    from modulo import modulo

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
