=======
History
=======

1.6.8 (2022-04-30)
------------------

* Added Python 3.10 support.
* Fixed issue #199 (pending confirmation) - upgraded libxml2 and libxslt versions to fix CVEs
* Upgraded development and build-time dependencies.
* Now using latest `cibuildwheel` 2.5.0, which supports more architectures and builds.
* Started to improve the documentation - added better usage examples.
* Formatting and linting fixes

1.6.7 (2020-12-24)
------------------

* Fixed MacOS binary wheel builds

1.6.6 (2020-10-04)
------------------

* Simplified and automated building source and binary wheels for Linux, MacOS, and Windows via GitHub actions + `cibuildwheel`.
* Improved documentation and local development workflow.
* Fixes issue #51 (previously closed as "hard to fix", but now reopened).
* Completely rewritten native Windows build process, based on libxslt.
* Windows port does not support `ls` (and conversely `listdir()`).

1.6.5 (2020-09-29)
------------------

* No changes from previous release except up-to-date dependencies and some build fixes.
* Fixes issue #118 (awaiting confirmation).

1.6.3 (2019-10-29)
------------------

* First working release on PyPI, based on xmlstarlet-1.6.1 source tarball.

1.6.2 (2019-10-28)
------------------

* Second (failed) release on PyPI, based on XMLStarlet master branch.

1.6.1 (2019-10-23)
------------------

* First (incomplete) release on PyPI, based on XMLStarlet master branch.
