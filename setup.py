from setuptools import setup

setup(
    name             = 'modulo',
    version          = '0.1.0.0',
    packages         = ['modulo',],
    install_requires = ['egcd',],
    license          = 'MIT',
    url              = 'https://github.com/lapets/modulo',
    author           = 'Andrei Lapets',
    author_email     = 'a@lapets.io',
    description      = 'Pure Python library for working with modular arithmetic, congruence classes, and finite fields.',
    long_description = open('README.rst').read(),
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
)
