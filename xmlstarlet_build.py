#!/usr/bin/env python
"""XMLStarlet CFFI Python bindings build script."""
import os
import subprocess
import sys
from glob import glob

from cffi import FFI

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
SOURCE_DIR = os.path.join(ROOT_DIR, "xmlstarlet")
C_SOURCE_DIR = os.path.join(SOURCE_DIR, "src")

# Ensure the git source directory is not dirty (e.g. when developing locally)
print(subprocess.getoutput("git checkout -- ./xmlstarlet/ || true"))

if os.name != "nt":
    HAVE_CONFIG = os.path.exists(os.path.join(SOURCE_DIR, "config.h"))
    HAVE_CONFIGURE = os.path.exists(os.path.join(SOURCE_DIR, "configure"))
    HAVE_MAKEFILE = os.path.exists(os.path.join(SOURCE_DIR, "Makefile"))

    if not HAVE_CONFIGURE:
        print("Generating `configure` with `autoreconf`...")
        exit_code, output = subprocess.getstatusoutput(
            "cd ./xmlstarlet/ && autoreconf -sif && cd  .."
        )

        print(output)
        if exit_code != 0:
            sys.exit(exit_code)

        HAVE_CONFIGURE = os.path.exists(os.path.join(SOURCE_DIR, "configure"))

    LIBRARY_DIRS = ["/usr/lib"]
    LIBRARIES = ["xml2", "xslt", "exslt"]
    SOURCES = [
        os.path.relpath(s, ROOT_DIR)
        for s in glob(os.path.join(SOURCE_DIR, "**"), recursive=True)
        if s.endswith(".c") and "_xmlstarlet" not in s and "win32" not in s
    ]

    EXTRA_CFLAGS = (
        subprocess.getoutput("xml2-config --cflags").split()
        + subprocess.getoutput("xslt-config --cflags").split()
    )

    EXTRA_LDFLAGS = (
        subprocess.getoutput("xml2-config --libs").split()
        + subprocess.getoutput("xslt-config --libs").split()
    )

    LIBRARY_DIRS += [
        ld.replace("-L", "") for ld in EXTRA_LDFLAGS if ld.startswith("-L")
    ]
    LIBRARIES += [lb.replace("-l", "") for lb in EXTRA_LDFLAGS if lb.startswith("-l")]

    INCLUDE_DIRS = [SOURCE_DIR, C_SOURCE_DIR] + [
        d.replace("-I", "") for d in EXTRA_CFLAGS if d.startswith("-I")
    ]
    LIBRARIES += [lb.replace("-l", "") for lb in EXTRA_CFLAGS if lb.startswith("-l")]

    os.environ.update(
        CONFIG_PREFIX=os.environ.get("CONFIG_PREFIX", "/usr"),
        INCLUDE_PATH=os.environ.get("INCLUDE_PATH", "/usr/include"),
        CFLAGS=os.environ.get("CFLAGS", " ".join(EXTRA_CFLAGS)),
    )

    if not (HAVE_CONFIG or HAVE_MAKEFILE) and HAVE_CONFIGURE:
        print("Running `./configure` to create a Makefile...")
        exit_code, output = subprocess.getstatusoutput(
            "cd ./xmlstarlet/ && ./configure --prefix={0} --includedir={1} && cd  ..".format(
                os.environ["CONFIG_PREFIX"],
                os.environ["INCLUDE_PATH"],
            )
        )

        print(output)
        if exit_code != 0:
            sys.exit(exit_code)

        HAVE_CONFIG = os.path.exists(os.path.join(SOURCE_DIR, "config.h"))
        HAVE_MAKEFILE = os.path.exists(os.path.join(SOURCE_DIR, "Makefile"))

    if HAVE_MAKEFILE:
        print("Compiling xmlstarlet C sources...")
        exit_code, output = subprocess.getstatusoutput(
            "cd ./xmlstarlet/ && make -j && make check && cd  .."
        )

        print(output)
        if exit_code != 0:
            sys.exit(exit_code)

else:
    os.environ["PREFIX"] = "C:\\opt"  # configured by build_msvc.bat.
    SOURCES = [
        os.path.relpath(s, ROOT_DIR)
        for s in glob(os.path.join(C_SOURCE_DIR, "**"), recursive=True)
        if s.endswith(".c")
        and "_xmlstarlet" not in s
        and ("win32_xml_ls.c" in s or "xml_ls.c" not in s)
    ]
    INCLUDE_DIRS = [
        SOURCE_DIR,
        C_SOURCE_DIR,
        os.path.join(os.environ["PREFIX"], "include"),
        os.path.join(os.environ["PREFIX"], "include", "libxml2"),
    ]
    LIBRARY_DIRS = [os.path.join(os.environ["PREFIX"], "lib")]
    LIBRARIES = [
        "libxml2_a",
        "libxslt_a",
        "libexslt_a",
        "wsock32",
        "ws2_32",
        "shell32",
    ]

sources = sorted(set(SOURCES))
include_dirs = sorted(set(INCLUDE_DIRS))
libraries = sorted(set(LIBRARIES))
library_dirs = sorted(set(LIBRARY_DIRS))

print("Build settings:")
print("-" * 40)
print("sources:\n\t{}".format("\n\t".join(sources)))
print("include_dirs:\n\t{}".format("\n\t".join(include_dirs)))
print("libraries:\n\t{}".format("\n\t".join(libraries)))
print("library_dirs:\n\t{}".format("\n\t".join(library_dirs)))
print("-" * 40)


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
    sources=sources,
    include_dirs=include_dirs,
    libraries=libraries,
    library_dirs=library_dirs,
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
