#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import sys

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["cffi>=1.0.0"]

setup_requirements = ["pytest-runner", "setuptools", "wheel", "cffi>=1.0.0"]

if sys.version_info[:2] in ((3, 7), (3, 6)):
    setup_requirements += ["pickle5"]

test_requirements = ["pytest"]

setup(
    author="Mikhail Grushinskiy",
    author_email="mgrouch@users.sourceforge.net",
    maintainer="Dimiter Naydenov",
    maintainer_email="dimitern@users.noreply.github.com",
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="XMLStarlet Toolkit: Python CFFI bindings",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    include_package_data=False,
    keywords="xmlstarlet cffi",
    name="xmlstarlet",
    packages=find_packages(include=["xmlstarlet"]),
    setup_requires=setup_requirements,
    cffi_modules=["xmlstarlet/xmlstarlet_build.py:FFIBUILDER"],
    python_requires=">=3.6.*",
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/dimitern/xmlstarlet",
    version="1.6.3",
    zip_safe=False,
)
