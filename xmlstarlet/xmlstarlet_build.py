#!/usr/bin/env python
"""XMLStarlet CFFI Python bindings build script."""
import os
import subprocess
from glob import glob

from cffi import FFI

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, "xmlstarlet")
C_SOURCE_DIR = os.path.join(SOURCE_DIR, "src")

print(
    subprocess.getoutput(
        "set -xe && cd xmlstarlet/ && test -f config.h && make -j && set +xe && cd .. "
    )
)

LIBRARIES = ["xml2", "xslt", "exslt"]
SOURCES = [
    os.path.relpath(s, ROOT_DIR)
    for s in glob(os.path.join(SOURCE_DIR, "**"), recursive=True)
    if s.endswith(".c")
]
INCLUDE_DIRS = ["/usr/include", "/usr/include/libxml2", SOURCE_DIR, C_SOURCE_DIR]

FFIBUILDER = FFI()

# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.  This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
FFIBUILDER.set_source(
    "xmlstarlet._xmlstarlet",
    """
#include <libxml/xmlversion.h>
#include <xmlstar.h>
#include <config.h>
#include <libexslt/exslt.h>
""",
    sources=SOURCES,
    include_dirs=INCLUDE_DIRS,
    libraries=LIBRARIES,
)

# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
FFIBUILDER.cdef(
    """
int c14nMain(int argc, char **argv);
int depyxMain(int argc, char **argv);
int edMain(int argc, char **argv);
int elMain(int argc, char **argv);
int escMain(int argc, char **argv, int escape);
int foMain(int argc, char **argv);
int lsMain(int argc, char **argv);
int pyxMain(int argc, char **argv);
int selMain(int argc, char **argv);
int trMain(int argc, char **argv);
int valMain(int argc, char **argv);
"""
)


if __name__ == "__main__":
    FFIBUILDER.compile(verbose=True)
