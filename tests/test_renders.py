"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.
"""

__author__ = "Kelson da Costa Medeiros <kelsoncm@gmail.com>"

import io
import os
from unittest import TestCase

from pyfwf.columns import (
    CharColumn,
    DateColumn,
    DateTimeColumn,
    PositiveDecimalColumn,
    PositiveIntegerColumn,
    RightCharColumn,
    TimeColumn,
)
from pyfwf.descriptors import (
    DetailRowDescriptor,
    FileDescriptor,
    FooterRowDescriptor,
    HeaderRowDescriptor,
)
from pyfwf.renders import render_as_html, render_as_markdown, render_as_rst


class TestRenders(TestCase):
    def setUp(self):
        self.file_descriptor = FileDescriptor(
            [
                DetailRowDescriptor(
                    [
                        CharColumn("row_type", 1),
                        CharColumn("name", 60),
                        RightCharColumn("right_name", 60),
                        PositiveIntegerColumn("positive_interger", 9),
                        PositiveDecimalColumn("positive_decimal", 9),
                        DateTimeColumn("datetime"),
                        DateColumn("date"),
                        TimeColumn("time"),
                    ]
                )
            ],
            HeaderRowDescriptor(
                [
                    CharColumn("row_type", 1),
                    CharColumn("filetype", 5),
                    CharColumn("fill", 157),
                ]
            ),
            FooterRowDescriptor(
                [
                    CharColumn("row_type", 1),
                    PositiveIntegerColumn("detail_count", 4),
                    PositiveIntegerColumn("row_count", 4),
                    CharColumn("fill", 154),
                ]
            ),
        )

        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        with open(os.path.join(assets_dir, "example01.json")) as f:
            self.example01_json = f.read()
        with open(os.path.join(assets_dir, "example01.md")) as f:
            self.example01_markdown = f.read()
        with open(os.path.join(assets_dir, "example01.rst")) as f:
            self.example01_rst = f.read()
        with open(os.path.join(assets_dir, "example01.html")) as f:
            self.example01_html = f.read()

        self.maxDiff = None

    def test_render_as_rst(self):
        with io.StringIO() as buf:
            render_as_rst(self.file_descriptor, buf)
            print(buf.getvalue())  # Veja a saída usando `pytest -s tests/test_renders.py`
            self.assertEqual(self.example01_rst, buf.getvalue())

    def test_render_as_html(self):
        with io.StringIO() as buf:
            render_as_html(self.file_descriptor, buf)
            # print(buf.getvalue()) # Veja a saída usando `pytest -s tests/test_renders.py`
            self.assertEqual(self.example01_html, buf.getvalue())

    def test_render_as_markdown(self):
        with io.StringIO() as buf:
            render_as_markdown(self.file_descriptor, buf)
            # print(buf.getvalue()) # Veja a saída usando `pytest -s tests/test_renders.py`
            self.assertEqual(self.example01_markdown, buf.getvalue())
