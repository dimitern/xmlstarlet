"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
# pylint: disable=invalid-name

import platform
import shutil
import webbrowser

from invoke import task

try:
    from pathlib import Path

    Path().expanduser()
except (ImportError, AttributeError):
    from pathlib2 import Path


ROOT_DIR = Path(__file__).parent
SETUP_FILE = ROOT_DIR.joinpath("setup.py")
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("xmlstarlet")
TOX_DIR = ROOT_DIR.joinpath(".tox")
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [SOURCE_DIR, TEST_DIR]]


def _delete_file(file):
    try:
        file.unlink(missing_ok=True)
    except TypeError:
        # missing_ok argument added in 3.8
        try:
            file.unlink()
        except FileNotFoundError:
            pass


@task(
    help={
        "wheel": "Build a binary wheel in addition to source package",
    }
)
def dist(c, wheel=False):
    """
    Build source and (optionally) a binary wheel packages, optionally installing it.
    """
    commands = "sdist" if not wheel else "sdist bdist_wheel"
    c.run(f"python {SETUP_FILE} {commands}")


@task(
    name="format",
    pre=[dist],
    help={"check": "Checks if source is formatted without applying changes"},
)
def format_sources(c, check=False):
    """
    Format code
    """
    python_dirs_string = " ".join(PYTHON_DIRS)
    # Run black
    black_options = "--check" if check else ""
    c.run(f"black {black_options} . {python_dirs_string}")
    # Run isort
    isort_options = "--check-only" if check else ""
    c.run(f"isort {isort_options} {python_dirs_string}")


@task(pre=[dist])
def lint(c):
    """
    Lint code
    """
    c.run("flake8 *.py")
    c.run("pylint --rcfile=setup.cfg *.py")


@task(pre=[dist])
def test(c):
    """
    Run tests
    """
    pty = platform.system() == "Linux"
    c.run(f"python {SETUP_FILE} test", pty=pty)


@task(
    help={
        "publish": "Publish the result via coveralls (not working)",
        "browser": "Open the local HTML coverage report in the default browser",
    }
)
def coverage(c, publish=False, browser=False):
    """
    Create coverage report
    """
    c.run(f"coverage run --source {SOURCE_DIR} -m pytest")
    c.run("coverage report")
    if publish:
        # Publish the results via coveralls
        c.run("coveralls")

    # Build a local report
    c.run("coverage html")
    if browser:
        webbrowser.open(COVERAGE_REPORT.as_uri())


@task(help={"browser": "Open the built documentation in the default browser"})
def docs(c, browser=False):
    """
    Generate documentation
    """
    c.run(f"sphinx-build -b html {DOCS_DIR} {DOCS_BUILD_DIR}")
    if browser:
        webbrowser.open(DOCS_INDEX.as_uri())


@task
def clean_docs(c):
    """
    Clean up files from documentation builds
    """
    c.run(f"rm -fr {DOCS_BUILD_DIR}")


@task
def clean_build(c):
    """
    Clean up files from package building
    """
    c.run("rm -fr build/")
    c.run("rm -fr dist/")
    c.run("rm -fr xmlstarlet/config.h " "xmlstarlet/Makefile " "xmlstarlet/config.status")
    c.run("rm -fr .eggs/")
    c.run("find . -name '*.egg-info' -exec rm -fr {} +")
    c.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(c):
    """
    Clean up Python file artifacts
    """
    c.run("find . -name '*.pyc' -exec rm -f {} +")
    c.run("find . -name '*.pyo' -exec rm -f {} +")
    c.run("find . -name '*~' -exec rm -f {} +")
    c.run("find . -name '__pycache__' -exec rm -fr {} +")


@task(help={"tox": "Clean tox directory {!r} as well"})
def clean_tests(c, tox=False):  # pylint: disable=unused-argument
    """
    Clean up files from testing
    """
    _delete_file(COVERAGE_FILE)
    if tox:
        shutil.rmtree(TOX_DIR, ignore_errors=True)
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)


@task(
    pre=[clean_build, clean_python, clean_tests, clean_docs],
    help={"uninstall": "Also uninstall the package (if installed)"},
)
def clean(c, uninstall=False):
    """
    Runs all clean sub-tasks
    """
    if uninstall:
        c.run("pip uninstall -y xmlstarlet")


@task(
    pre=[clean],
    help={"dry-run": "Only display what will change, do NOT commit/tag/push"},
)
def release(c, dry_run=False):
    """
    Run all tox tests, and if successful, bump the patch
    version of the package, commit and tag it, then push
    to GitHub. If `dry_run` is True, no commit or push is
    done. Working directory must be clean (no uncommited
    changes).
    """
    tox_args = "--skip-pkg-install -e py37" if not dry_run else ""
    c.run(f"tox {tox_args}")
    dry = "--dry-run" if dry_run else ""
    c.run(f"bump2version {dry} --verbose patch")

    if not dry_run:
        c.run("git push --tags")
