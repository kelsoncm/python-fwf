"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


import json, io, sys
from unittest import TestCase
from pybatchfile.readers import Reader
import json, io
from unittest import TestCase
from pybatchfile.columns import CharColumn, RightCharColumn, PositiveIntegerColumn, PositiveDecimalColumn, \
    DateTimeColumn, DateColumn, TimeColumn
from pybatchfile.descriptors import RowDescriptor, HeaderRowDescriptor, \
    FooterRowDescriptor, DetailRowDescriptor, FileDescriptor


class TestReader(TestCase):

    def setUp(self):
        self.file_descriptor = FileDescriptor(
            [
                DetailRowDescriptor([
                    CharColumn('row_type', 1),
                    CharColumn('name', 60),
                    RightCharColumn('right_name', 60),
                    PositiveIntegerColumn('positive_interger', 9),
                    PositiveDecimalColumn('positive_decimal', 9),
                    DateTimeColumn('datetime'),
                    DateColumn('date'),
                    TimeColumn('time'),
                ])
            ],
            HeaderRowDescriptor([
                CharColumn('row_type', 1),
                CharColumn('filetype', 5),
                CharColumn('fill', 157),
            ]),
            FooterRowDescriptor([
                CharColumn('row_type', 1),
                PositiveIntegerColumn('detail_count', 4),
                PositiveIntegerColumn('row_count', 4),
                CharColumn('fill', 154),
            ]),
        )
        with open('assets/example01.json') as f:
            self.example01_json = f.read()
        with open('assets/example01.md') as f:
            self.example01_markdown = f.read()
        with open('assets/example01_wrong_line_size.batch') as f:
            self.example01_wrong_line_size = f.read()
        with open('assets/example01_are_right.batch') as f:
            self.example01_are_right = f.read()
        with open('assets/example01_are_right_win.batch') as f:
            self.example01_are_right_win = f.read()

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 2', Reader)

    def test_constructor_wrong_arguments(self):
        self.assertRaisesRegex(AssertionError, 'Iterator', Reader, 1, 2)
        self.assertRaisesRegex(AssertionError, 'Iterator', Reader, False, True)
        self.assertRaisesRegex(AssertionError, 'FileDescriptor', Reader, [], True)
        self.assertRaisesRegex(AssertionError, 'FileDescriptor', Reader, [], 1)
        self.assertRaisesRegex(AssertionError, 'FileDescriptor', Reader, [], 1)
        self.assertRaisesRegex(AssertionError, 'lines_count', Reader, [], self.file_descriptor, "")
        self.assertRaisesRegex(AssertionError, 'lines_count', Reader, [], self.file_descriptor, False)

    def test_constructor_args_ok(self):
        self.assertIsInstance(Reader([], self.file_descriptor), Reader)
        with open('assets/example01_are_right.batch') as f:
            self.assertIsInstance(Reader(f, self.file_descriptor), Reader)
        with io.StringIO() as f:
            self.assertIsInstance(Reader(f, self.file_descriptor), Reader)

    def test_validate_file_structure__wrong_line_size(self):
        reader = Reader(io.StringIO(self.example01_wrong_line_size), self.file_descriptor)
        self.assertRaisesRegex(AssertionError, 'instead of 163 we have 6', reader.validate_file_structure)

    def test_validate_file_structure__are_right(self):
        reader = Reader(io.StringIO(self.example01_are_right), self.file_descriptor)
        reader.lines_count = reader.validate_file_structure()
        self.assertEqual(4, reader.lines_count)

    def test_constructor(self):
        with open('assets/example01_are_right.batch') as f:
            reader = Reader(io.StringIO(self.example01_are_right), self.file_descriptor)
            reader.lines_count = reader.validate_file_structure()
            for row in reader:
                print(row)
        with open('assets/example01_are_right_win.batch') as f:
            reader = Reader(io.StringIO(self.example01_are_right), self.file_descriptor)
            reader.lines_count = reader.validate_file_structure()
            for row in reader:
                print(row)
