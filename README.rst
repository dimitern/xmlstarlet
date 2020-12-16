===============
XMLStarlet CFFI
===============


.. image:: https://img.shields.io/pypi/v/xmlstarlet.svg
     :target: https://pypi.python.org/pypi/xmlstarlet

.. image:: https://github.com/dimitern/xmlstarlet/workflows/cibuildwheel/badge.svg?branch=master&event=push
     :target: https://github.com/dimitern/xmlstarlet/actions?query=event%3Apush+branch%3Amaster+workflow%3Acibuildwheel
     :alt: cibuildwheel

.. image:: https://readthedocs.org/projects/xmlstarlet/badge/?version=latest
     :target: https://xmlstarlet.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status


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
* `listdir(*args)`: List directory as XML (**NOT** supported on Windows)
* `escape(*args)`: Escape special XML characters
* `unescape(*args)`: Unescape special XML characters
* `pyx(*args)`: Convert XML into PYX format (based on ESIS - ISO 8879)
* `depyx(*args)`: Convert PYX into XML

For some examples, have a look at `tests/test_xmlstarlet.py`.

Credits
-------

Kudos to XMLStarlet and its maintainers and users (original sources on SourceForge_)!

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

Binary wheels built via GitHub Actions by cibuildwheel_

.. _SourceForge: https://sourceforge.net/projects/xmlstar/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _cibuildwheel: https://github.com/joerick/cibuildwheel

