.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/dimitern/xmlstarlet/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

XMLStarlet CFFI could always use more documentation, whether as part of the
official XMLStarlet CFFI docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/dimitern/xmlstarlet/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `xmlstarlet` for local development.

1. Fork the `xmlstarlet` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/xmlstarlet.git

3. Install your local copy into a virtualenv. Assuming you have Python 3 installed,
   this is how you set up your fork for local development::

    $ cd xmlstarlet/
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt

The following one-liner command goes through all steps: cleans all
build artifacts (if any), uninstalls the package (if installed), runs
the linters (asserting scores haven't gone down and no new issues are
found), the formatter (checking formatting won't change any of the files),
builds a source distribution, then a binary wheel, running all tests,
producing a coverage HTML report, and finally building the sphinx HTML,
displayed in a browser on completion::

    $ invoke clean --uninstall lint format --check dist --wheel test coverage docs --browser

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ invoke format lint test  # optional; tox runs those as well
    $ tox

Both `invoke` and `tox` are already installed from `requirements.txt`.
To re-create all the `tox` environments and run all matrix combinations::

   $ tox -r -e ALL  # equivalent to `invoke clean-tests --tox`

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push -u origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.6 and later (currently, up to 3.9).
   Check https://github.com/dimitern/xmlstarlet/pulls and make sure all checks
   pass OK. Binary wheels are built automatically for each PR, or `git push` to
   a branch.

Tips
----

To run a subset of tests::

  $ pytest tests.test_xmlstarlet

(`python setup.py test` will also work as alias of `pytest`).

Deploying
---------

A reminder for the maintainers on how to deploy.

Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

  $ invoke release --dry-run

This runs `tox`, and then displays how the new version will look like,
without pushing anything.

If it goes OK, make the actual release with::

  $ invoke release
