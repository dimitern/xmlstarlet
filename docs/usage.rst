=====
Usage
=====

Let's see some usage examples and description of each command.

------------
xml CLI Help
------------

.. highlight:: none

The original ``xml`` CLI command has the following help description::

  XMLStarlet Toolkit: Command line utilities for XML
  Usage: ./xml [<options>] <command> [<cmd-options>]
  where <command> is one of:
    ed    (or edit)      - Edit/Update XML document(s)
    sel   (or select)    - Select data or query XML document(s) (XPATH, etc)
    tr    (or transform) - Transform XML document(s) using XSLT
    val   (or validate)  - Validate XML document(s) (well-formed/DTD/XSD/RelaxNG)
    fo    (or format)    - Format XML document(s)
    el    (or elements)  - Display element structure of XML document
    c14n  (or canonic)   - XML canonicalization
    ls    (or list)      - List directory as XML
    esc   (or escape)    - Escape special XML characters
    unesc (or unescape)  - Unescape special XML characters
    pyx   (or xmln)      - Convert XML into PYX format (based on ESIS - ISO 8879)
    p2x   (or depyx)     - Convert PYX into XML
  <options> are:
    -q or --quiet        - no error output
    --doc-namespace      - extract namespace bindings from input doc (default)
    --no-doc-namespace   - don't extract namespace bindings from input doc
    --version            - show version
    --help               - show help
  Wherever file name mentioned in command help it is assumed
  that URL can be used instead as well.

  Type: .xml <command> --help <ENTER> for command help

  XMLStarlet is a command line toolkit to query/edit/check/transform
  XML documents (for more information see http://xmlstar.sourceforge.net/)

^^^^^^^^^^^
From Python
^^^^^^^^^^^

.. highlight:: python

To use XMLStarlet CFFI in a project::

    import xmlstarlet

Each command takes the same string arguments as the C version of ``xmlstarlet``, and returns an
integer exit code (0 means success).

Some examples for supported commands can be seen below.

-----------------
xmlstarlet.edit()
-----------------

.. highlight:: none

Original ``xml`` CLI help text for ``edit``::

    XMLStarlet Toolkit: Edit XML document(s)
    Usage: ./xml ed <global-options> {<action>} [ <xml-file-or-uri> ... ]
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

    XMLStarlet is a command line toolkit to query/edit/check/transform
    XML documents (for more information see http://xmlstar.sourceforge.net/)

.. highlight:: xml

Let's assume you have this ``test.xml`` file you want to modify::

    <h:html xmlns:h="urn:local:html">
            <h:body>
                    <h:p>
                            <h:a h:href="#">
                                    Link
                            </h:a>
                    </h:p>
            </h:body>
    </h:html>

The modification is to find the first hyperlink, extract its text content, and add it as the
value of a new attribute ``text=`` on the root (``html``) element, like so::

    <?xml version="1.0"?>
    <h:html xmlns:h="urn:local:html" text="Link">
            <h:body>
                    <h:p>
                            <h:a h:href="#">
                                    Link
                            </h:a>
                    </h:p>
            </h:body>
    </h:html>


.. highlight:: python

Here's how you can use the `edit` command to achieve this::

   result = xmlstarlet.edit(
        "-S",
        "-N", "_=urn:local:html",
        "--var", "foo", "translate(//_:a[1]/text(), ' \n', '')",
        "-s", "/_:html", "-t", "attr", "-n", "text", "-v", "X",
        "-u", "$prev", "-x", "$foo",
        "./test.xml",
        "./test2.xml",
   )
   if result != 0:
      print("Cannot update the XML")

This demonstrates a number of options and techniques:

``-S``
  preserve whitespaces in the input (do not trim).

``-N _=urn:local:html``
  define namespaces present in the input (usable in expressions), here we define ``_`` as
  the namespace prefix for ``urn:local:html``.

``--var foo translate(//_:a[1]/text(), ' \n', '')``
  assign the result of an XPath expression (in this case, a function call removing spaces
  and new-lines from the text content of the first ``a`` element), to a named variable ``foo``.

``-s /_:html -t attr -n text -v X``
  create a subnode (in this case, attribute), named ``text``, with value ``X`` (temporarily),
  as a child of the root ``h:html`` element.

``-u $prev -x $foo``
  update the node at the given XPath with the result of another XPath expression. In this case,
  the special variable ``$prev`` contains the last matched XPath (``/_:html``), and the variable
  ``$foo`` contains ``"Link"``.

``./test.xml``
  the input XML file to operate on.

``./test2.xml``
  the output XML file (will be **overwritten**).

.. tip:: More examples can be found in the original ``xmlstarlet`` edit_ documentation.

.. _edit: http://xmlstar.sourceforge.net/doc/UG/ch04s03.html
