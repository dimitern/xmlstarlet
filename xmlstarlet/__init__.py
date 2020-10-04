#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CFFI bindings to enable using the XMLStarlet Toolkit Command-line utilities for XML
processing from Python.

All commands are supported:

  edit(*args)         - Edit/Update XML document(s)
  select(*args)       - Select data or query XML document(s) (XPATH, etc)
  transform(*args)    - Transform XML document(s) using XSLT
  validate(*args)     - Validate XML document(s) (well-formed/DTD/XSD/RelaxNG)
  format(*args)       - Format XML document(s)
  elements(*args)     - Display element structure of XML document
  canonicalize(*args) - XML canonicalization
  listdir(*args)      - List directory as XML
  escape(*args)       - Escape special XML characters
  unescape(*args)     - Unescape special XML characters
  pyx(*args)          - Convert XML into PYX format (based on ESIS - ISO 8879)
  depyx(*args)        - Convert PYX into XML

Each of these functions takes string arguments and returns the integer exit code
(0 = success, otherwise an error occured).
"""

import xmlstarlet._xmlstarlet

_ffi = xmlstarlet._xmlstarlet.ffi  # pylint: disable=protected-access
_lib = xmlstarlet._xmlstarlet.lib  # pylint: disable=protected-access

__author__ = """Mikhail Grushinskiy"""
__email__ = "mgrouch@users.sourceforge.net"
__version__ = "1.6.6"


def _call_main(*args, main_func, escape_flag=-1):
    args = ["xmlstarlet", "command"] + list(args)
    ffi_args = []
    for arg in args:
        barg = bytes(arg, encoding="utf-8")
        cdata = _ffi.new("char[]", barg)
        ffi_args += [cdata]

    ffi_argv = _ffi.new("char *[]", ffi_args)
    ffi_argc = len(args)
    if escape_flag != -1:
        result = main_func(ffi_argc, ffi_argv, escape_flag)
    else:
        result = main_func(ffi_argc, ffi_argv)

    return result


def edit(*args):
    """
    Edit/Update XML document(s).

    `*args` contain string commands and/or options in the following format:

    <global-options> {<action>} [ <xml-file-or-uri> ... ]

    where
      <global-options>  - global options for editing
      <xml-file-or-uri> - input XML document file name/uri (stdin otherwise)

    <global-options> are:
      -P, or -S           - preserve whitespace nodes.
         (or --pf, --ps)    Note that space between attributes is not preserved
      -O (or --omit-decl) - omit XML declaration (<?xml ...?>)
      -L (or --inplace)   - edit file inplace
      -N <name>=<value>   - predefine namespaces (name without 'xmlns:')
                            ex: xsql=urn:oracle-xsql
                            Multiple -N options are allowed.
                            -N options must be last global options.
      --net               - allow network access
      --help or -h        - display help

    where <action>
      -d or --delete <xpath>
      --var <name> <xpath>
      -i or --insert <xpath> -t (--type) elem|text|attr -n <name> [-v (--value) <value>]
      -a or --append <xpath> -t (--type) elem|text|attr -n <name> [-v (--value) <value>]
      -s or --subnode <xpath> -t (--type) elem|text|attr -n <name> [-v (--value) <value>]
      -m or --move <xpath1> <xpath2>
      -r or --rename <xpath1> -v <new-name>
      -u or --update <xpath> -v (--value) <value>
                             -x (--expr) <xpath>
    """
    return _call_main(*args, main_func=_lib.edMain)


def select(*args):
    """
    Select from XML document(s).

    `*args` contain string commands and/or options in the following format:

    <global-options> {<template>} [ <xml-file> ... ]

    where
      <global-options> - global options for selecting
      <xml-file> - input XML document file name/uri (stdin is used if missing)
      <template> - template for querying XML document with following syntax:

    <global-options> are:
      -Q or --quiet             - do not write anything to standard output.
      -C or --comp              - display generated XSLT
      -R or --root              - print root element <xsl-select>
      -T or --text              - output is text (default is XML)
      -I or --indent            - indent output
      -D or --xml-decl          - do not omit xml declaration line
      -B or --noblanks          - remove insignificant spaces from XML tree
      -E or --encode <encoding> - output in the given encoding (utf-8, unicode...)
      -N <name>=<value>         - predefine namespaces (name without 'xmlns:')
                                  ex: xsql=urn:oracle-xsql
                                  Multiple -N options are allowed.
      --net                     - allow fetch DTDs or entities over network
      --help                    - display help

    Syntax for templates: -t|--template <options>
    where <options>
      -c or --copy-of <xpath>   - print copy of XPATH expression
      -v or --value-of <xpath>  - print value of XPATH expression
      -o or --output <string>   - output string literal
      -n or --nl                - print new line
      -f or --inp-name          - print input file name (or URL)
      -m or --match <xpath>     - match XPATH expression
      --var <name> <value> --break or
      --var <name>=<value>      - declare a variable (referenced by $name)
      -i or --if <test-xpath>   - check condition <xsl:if test="test-xpath">
      --elif <test-xpath>       - check condition if previous conditions failed
      --else                    - check if previous conditions failed
      -e or --elem <name>       - print out element <xsl:element name="name">
      -a or --attr <name>       - add attribute <xsl:attribute name="name">
      -b or --break             - break nesting
      -s or --sort op xpath     - sort in order (used after -m) where
      op is X:Y:Z,
        X is A - for order="ascending"
        X is D - for order="descending"
        Y is N - for data-type="numeric"
        Y is T - for data-type="text"
        Z is U - for case-order="upper-first"
        Z is L - for case-order="lower-first"

    There can be multiple --match, --copy-of, --value-of, etc options
    in a single template. The effect of applying command line templates
    can be illustrated with the following XSLT analogue

    xmlstarlet.select(
      "-t", "-c", "xpath0", "-m", "xpath1", "-m", "xpath2", "-v", "xpath3",
      "-t", "-m", "xpath4", "-c", "xpath5", "input.xml")

    is equivalent to applying the following XSLT

    <?xml version="1.0"?>
    <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
      <xsl:template match="/">
        <xsl:call-template name="t1"/>
        <xsl:call-template name="t2"/>
      </xsl:template>
      <xsl:template name="t1">
        <xsl:copy-of select="xpath0"/>
          <xsl:for-each select="xpath1">
            <xsl:for-each select="xpath2">
              <xsl:value-of select="xpath3"/>
            </xsl:for-each>
          </xsl:for-each>
      </xsl:template>
      <xsl:template name="t2">
        <xsl:for-each select="xpath4">
          <xsl:copy-of select="xpath5"/>
        </xsl:for-each>
      </xsl:template>
    </xsl:stylesheet>
    """
    return _call_main(*args, main_func=_lib.selMain)


def transform(*args):
    """
    Transform XML document(s) using XSLT.

    `*args` contain string commands and/or options in the following format:

    [<options>] <xsl-file> {-p|-s <name>=<value>} [<xml-file>...]

    where
      <xsl-file>      - main XSLT stylesheet for transformation
      <xml-file>      - input XML document file/URL (stdin is used if missing)
      <name>=<value>  - name and value of the parameter passed to XSLT processor
      -p              - parameter is XPATH expression ("'string'" to quote string)
      -s              - parameter is a string literal

    <options> are:
      --help or -h    - display help message
      --omit-decl     - omit xml declaration <?xml version="1.0"?>
      --embed or -E   - allow applying embedded stylesheet
      --show-ext      - show list of extensions
      --val           - allow validate against DTDs or schemas
      --net           - allow fetch DTDs or entities over network
      --xinclude      - do XInclude processing on document input
      --maxdepth val  - increase the maximum depth
      --html          - input document(s) is(are) in HTML format
    """
    return _call_main(*args, main_func=_lib.trMain)


def validate(*args):
    """
    Validate XML document(s) (well-formed/DTD/XSD/RelaxNG).

    `*args` contain string commands and/or options in the following format:

    <options> [ <xml-file-or-uri> ... ]

    where <options>
      -w or --well-formed        - validate well-formedness only (default)
      -d or --dtd <dtd-file>     - validate against DTD
      --net                      - allow network access
      -s or --xsd <xsd-file>     - validate against XSD schema
      -E or --embed              - validate using embedded DTD
      -r or --relaxng <rng-file> - validate against Relax-NG schema
      -e or --err                - print verbose error messages on stderr
      -S or --stop               - stop on first error
      -b or --list-bad           - list only files which do not validate
      -g or --list-good          - list only files which validate
      -q or --quiet              - do not list files (return result code only)

    NOTE: XML Schemas are not fully supported yet due to its incomplete
          support in libxml2 (see http://xmlsoft.org)
    """
    return _call_main(*args, main_func=_lib.valMain)


def format(*args):  # pylint:disable=redefined-builtin
    """
    Format XML document(s).

    `*args` contain string commands and/or options in the following format:

    [<options>] <xml-file>

    where <options> are
      -n or --noindent            - do not indent
      -t or --indent-tab          - indent output with tabulation
      -s or --indent-spaces <num> - indent output with <num> spaces
      -o or --omit-decl           - omit xml declaration <?xml version="1.0"?>
      --net                       - allow network access
      -R or --recover             - try to recover what is parsable
      -D or --dropdtd             - remove the DOCTYPE of the input docs
      -C or --nocdata             - replace cdata section with text nodes
      -N or --nsclean             - remove redundant namespace declarations
      -e or --encode <encoding>   - output in the given encoding (utf-8, unicode...)
      -H or --html                - input is HTML
      -h or --help                - print help
    """
    return _call_main(*args, main_func=_lib.foMain)


def element(*args):
    """
    Display element structure of XML document.

    `*args` contain string commands and/or options in the following format:

    [<options>] <xml-file>

    where
      <xml-file> - input XML document file name (stdin is used if missing)
      <options> is one of:
      -a    - show attributes as well
      -v    - show attributes and their values
      -u    - print out sorted unique lines
      -d<n> - print out sorted unique lines up to depth <n>
    """
    return _call_main(*args, main_func=_lib.elMain)


def canonicalize(*args):
    """
    XML canonicalization.

    `*args` contain string commands and/or options in the following format:

    [--net] <mode> <xml-file> [<xpath-file>] [<inclusive-ns-list>]

    where
      <xml-file>   - input XML document file name (stdin is used if '-')
      <xpath-file> - XML file containing XPath expression for
                     c14n XML canonicalization
        Example:
        <?xml version="1.0"?>
        <XPath xmlns:n0="http://a.example.com" xmlns:n1="http://b.example">
          (//. | //@* | //namespace::*)[ancestor-or-self::n1:elem1]
        </XPath>

      <inclusive-ns-list> - the list of inclusive namespace prefixes
                            (only for exclusive canonicalization)
        Example: 'n1 n2'

      <mode> is one of following:
        --with-comments         XML file canonicalization w comments (default)
        --without-comments      XML file canonicalization w/o comments
        --exc-with-comments     Exclusive XML file canonicalization w comments
        --exc-without-comments  Exclusive XML file canonicalization w/o comments
    """
    return _call_main(*args, main_func=_lib.c14nMain)


def listdir(*args):
    """
    List directory as XML.

    `*args` contain string commands and/or options in the following format:

    [ <dir> | --help ]

    Lists current directory in XML format.
    Time is shown per ISO 8601 spec.
    """
    return _call_main(*args, main_func=_lib.lsMain)


def escape(*args):
    """
    Escape special XML characters.

    `*args` contain string commands and/or options in the following format:

    [<options>] [<string>]

    where <options> are
      --help      - print usage

    if <string> is missing stdin is used instead.
    """
    return _call_main(*args, main_func=_lib.escMain, escape_flag=1)


def unescape(*args):
    """
    Unescape special XML characters.

    `*args` contain string commands and/or options in the following format:

    [<options>] [<string>]

    where <options> are
      --help      - print usage

    if <string> is missing stdin is used instead.
    """
    return _call_main(*args, main_func=_lib.escMain, escape_flag=0)


def pyx(*args):
    """
    Convert XML into PYX format (based on ESIS - ISO 8879).

    `*args` contain string commands and/or options in the following format:

    {<xml-file>}

    where
      <xml-file> - input XML document file name (stdin is used if missing)

    The PYX format is a line-oriented representation of
    XML documents that is derived from the SGML ESIS format.
    (see ESIS - ISO 8879 Element Structure Information Set spec,
    ISO/IEC JTC1/SC18/WG8 N931 (ESIS))

    A non-validating, ESIS generating tool originally developed for
    pyxie project (see http://pyxie.sourceforge.net/)
    ESIS Generation by Sean Mc Grath http://www.digitome.com/sean.html
    """
    return _call_main(*args, main_func=_lib.pyxMain)


def depyx(*args):
    """
    Convert PYX into XML.

    `*args` contain string commands and/or options in the following format:

    [<pyx-file>]

    where
      <pyx-file> - input PYX document file name (stdin is used if missing)

    The PYX format is a line-oriented representation of
    XML documents that is derived from the SGML ESIS format.
    (see ESIS - ISO 8879 Element Structure Information Set spec,
    ISO/IEC JTC1/SC18/WG8 N931 (ESIS))
    """
    return _call_main(*args, main_func=_lib.depyxMain)
