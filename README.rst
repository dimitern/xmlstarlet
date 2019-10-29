===============
XMLStarlet CFFI
===============


.. image:: https://img.shields.io/pypi/v/xmlstarlet.svg
        :target: https://pypi.python.org/pypi/xmlstarlet

.. image:: https://img.shields.io/travis/dimitern/xmlstarlet.svg
        :target: https://travis-ci.org/dimitern/xmlstarlet

.. image:: https://readthedocs.org/projects/xmlstarlet/badge/?version=latest
        :target: https://xmlstarlet.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/dimitern/xmlstarlet/shield.svg
     :target: https://pyup.io/repos/github/dimitern/xmlstarlet/
     :alt: Updates



XMLStarlet Toolkit: Python CFFI bindings


* Free software: MIT license
* Documentation (this package): https://xmlstarlet.readthedocs.io.
* Original XMLStarlet Documentation: http://xmlstar.sourceforge.net/doc/UG/

Features
--------

Supports all XMLStarlet commands from Python, just `import xmlstarlet`:

* `edit(*args)`: Edit/Update XML document(s)
* `select(*args)`: Select data or query XML document(s) (XPATH, etc)
* `transform(*args)`: Transform XML document(s) using XSLT
* `validate(*args)`: Validate XML document(s) (well-formed/DTD/XSD/RelaxNG)
* `format(*args)`: Format XML document(s)
* `elements(*args)`: Display element structure of XML document
* `canonicalize(*args)`: XML canonicalization
* `listdir(*args)`: List directory as XML
* `escape(*args)`: Escape special XML characters
* `unescape(*args)`: Unescape special XML characters
* `pyx(*args)`: Convert XML into PYX format (based on ESIS - ISO 8879)
* `depyx(*args)`: Convert PYX into XML

For some examples, have a look at `tests/test_xmlstarlet.py`.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
