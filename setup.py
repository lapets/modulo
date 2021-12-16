from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="modulo",
    version="0.2.0",
    packages=["modulo",],
    install_requires=["egcd~=0.2",],
    license="MIT",
    url="https://github.com/lapets/modulo",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Pure Python library for working with modular arithmetic, " +\
                "congruence classes, and finite fields.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
