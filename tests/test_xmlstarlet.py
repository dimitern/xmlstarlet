#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `xmlstarlet` package."""

import os

import pytest

import xmlstarlet


@pytest.fixture(scope="session", autouse=True)
def testsdir():
    original = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    yield
    os.chdir(original)


def test_edit():
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


def test_element():
    assert xmlstarlet.element("./test.xml") == 0


def test_escape():
    assert xmlstarlet.escape("./test.xml") == 0


def test_unescape():
    assert xmlstarlet.unescape("./test2.xml") == 0


def test_canonicalize():
    assert xmlstarlet.canonicalize("test.xml") == 0


def test_pyx():
    assert xmlstarlet.pyx("test.xml") == 0


def test_depyx():
    assert xmlstarlet.depyx("test.xml") == 0


def test_select():
    assert xmlstarlet.select("-t", "-f", "-n", "-b", "test.xml") == 0


def test_format():
    assert xmlstarlet.format("test2.xml") == 0


def test_listdir():
    # ls is not supported on Windows.
    expected = 0
    if os.name == "nt":
        expected = 1
    assert xmlstarlet.listdir() == expected


def test_transform():
    assert xmlstarlet.transform("test.xslt", "test.xml") == 0


def test_validate():
    assert xmlstarlet.validate("-r", "test.rng", "-e", "test.xml") == 0
