#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `xmlstarlet` package."""

import os

import py
import pytest

import xmlstarlet


@pytest.fixture(scope="function")
def captured_fd():
    c = py.io.StdCaptureFD(out=True, err=True, in_=False)
    return c


@pytest.fixture(scope="session", autouse=True)
def testsdir():
    original = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    yield
    os.chdir(original)


def test_edit(captured_fd):
    assert (
        xmlstarlet.edit(
            "-S",
            "-N",
            "_=urn:local:html",
            "--var",
            "foo",
            "translate(//_:a[1]/text(), ' \n', '')",
            "-s",
            "/_:html",
            "-t",
            "attr",
            "-n",
            "text",
            "-v",
            "X",
            "-u",
            "$prev",
            "-x",
            "$foo",
            "./test.xml",
            "./test2.xml",
        )
        == 0
    )

    expected = """<?xml version="1.0"?>
<h:html xmlns:h="urn:local:html" text="Link">
        <h:body>
                <h:p>
                        <h:a h:href="#">
                                Link
                        </h:a>
                </h:p>
        </h:body>
</h:html>
<?xml version="1.0"?>
<h:html xmlns:h="urn:local:html" text="Link" text="Link">
        <h:body>
                <h:p>
                        <h:a h:href="#">
                                Link
                        </h:a>
                </h:p>
        </h:body>
</h:html>
"""

    out, err = captured_fd.reset()
    assert err == ""
    assert out == expected


def test_element(captured_fd):
    assert xmlstarlet.element("./test.xml") == 0

    expected = """h:html
h:html/h:body
h:html/h:body/h:p
h:html/h:body/h:p/h:a
"""

    out, err = captured_fd.reset()
    assert err == ""
    assert out == expected


def test_escape(captured_fd):
    exit_code = xmlstarlet.escape("<xml/>")
    assert exit_code == 0

    out, err = captured_fd.reset()
    assert err == ""
    assert out == "&lt;xml/&gt;\n"


def test_unescape(captured_fd):
    ec = xmlstarlet.unescape("&lt;xml/&gt;")
    assert ec == 0

    out, err = captured_fd.reset()
    assert err == ""
    assert out == "<xml/>"


def test_canonicalize(captured_fd):
    assert xmlstarlet.canonicalize("test.xml") == 0

    expected = """<h:html xmlns:h="urn:local:html">
        <h:body>
                <h:p>
                        <h:a h:href="#">
                                Link
                        </h:a>
                </h:p>
        </h:body>
</h:html>"""

    out, err = captured_fd.reset()
    assert err == ""
    assert out == expected


def test_pyx(captured_fd):
    assert xmlstarlet.pyx("test.xml") == 0

    out, err = captured_fd.reset()
    expected = open("./test.pyx", "r").read()
    assert err == ""
    assert out == expected


def test_depyx(captured_fd):
    assert xmlstarlet.depyx("test.pyx") == 0

    out, err = captured_fd.reset()
    expected = """<h:html xmlns:h="urn:local:html">
        <h:body>
                <h:p>
                        <h:a h:href="#">
                                Link
                        </h:a>
                </h:p>
        </h:body>
</h:html>
"""
    assert err == ""
    assert out == expected


def test_select(captured_fd):
    assert xmlstarlet.select("-t", "-f", "-n", "-b", "test.xml") == 0

    out, err = captured_fd.reset()
    assert err == ""
    assert out.strip() == "test.xml"


def test_format(captured_fd):
    assert xmlstarlet.format("test2.xml") == 0

    expected = """<?xml version="1.0"?>
<h:html xmlns:h="urn:local:html" text="Link">
  <h:body>
    <h:p>
      <h:a h:href="#">
                                Link
                        </h:a>
    </h:p>
  </h:body>
</h:html>
"""

    out, err = captured_fd.reset()
    assert err == ""
    assert out == expected


def test_listdir(captured_fd):
    # ls is not supported on Windows.
    expected = 0
    out_contains = "</dir>"
    if os.name == "nt":
        expected = 1
        out_contains = "ls is not supported"
    assert xmlstarlet.listdir() == expected

    out, err = captured_fd.reset()
    assert err == ""
    assert out_contains in out


def test_transform(captured_fd):
    assert xmlstarlet.transform("test.xslt", "test.xml") == 0

    expected = """<?xml version="1.0" encoding="utf-8"?>
<h:html xmlns:h="urn:local:html">
        <h:body>
                <h:p>
                        <h:a h:href="#">
                                Link
                        </h:a>
                </h:p>
        </h:body>
</h:html>"""

    out, err = captured_fd.reset()
    assert err == ""
    assert out.strip() == expected.strip()


def test_validate(captured_fd):
    assert xmlstarlet.validate("-r", "test.rng", "-e", "test.xml") == 0

    out, err = captured_fd.reset()
    assert err == ""
    assert out == "test.xml - valid\n"
