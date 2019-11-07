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


import io
import datetime
from typing import Iterable, Iterator
from unittest import TestCase
from pyfwf.readers import Reader
from pyfwf.columns import CharColumn, RightCharColumn, PositiveIntegerColumn, PositiveDecimalColumn, \
    DateTimeColumn, DateColumn, TimeColumn
from pyfwf.descriptors import HeaderRowDescriptor, \
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
                CharColumn('filetype', 3),
                CharColumn('fill', 159),
            ]),
            FooterRowDescriptor([
                CharColumn('row_type', 1),
                PositiveIntegerColumn('detail_count', 4),
                PositiveIntegerColumn('row_count', 4),
                CharColumn('fill', 154),
            ]),
        )
        with open('/src/tests/assets/example01.json') as f:
            self.example01_json = f.read()
        with open('/src/tests/assets/example01.md') as f:
            self.example01_markdown = f.read()
        with open('/src/tests/assets/example01_wrong_line_size.fwf') as f:
            self.example01_wrong_line_size = f.read()
        with open('/src/tests/assets/example01_are_right.fwf') as f:
            self.example01_are_right = f.read()
        with open('/src/tests/assets/example01_are_right_win.fwf') as f:
            self.example01_are_right_win = f.read()
        self.example01_are_right_lst = [
            "1FWF                                                                              "
            "                                                                                 \n",
            "2KELSON DA COSTA MEDEIROS                                                         "
            "               KELSON DA COSTA MEDEIROS123456789123456789200102282359200102282359\n",
            "2KELSON DA COSTA MEDEIROS                                                         "
            "               KELSON DA COSTA MEDEIROS000000000000000000000000000000000000000000\n",
            "900020003                                                                         "
            "                                                                                 \n"
        ]
        self.example01_are_right_expected = [
            {'row_type': '1', 'filetype': 'FWF', 'fill': ''},
            {'row_type': '2', 'name': 'KELSON DA COSTA MEDEIROS', 'right_name': 'KELSON DA COSTA MEDEIROS',
             'positive_interger': 123456789, 'positive_decimal': 1234567.89,
             'datetime': datetime.datetime(228, 1, 20, 23, 59), 'date': datetime.date(228, 1, 20),
             'time': datetime.time(23, 59)},
            {'row_type': '2', 'name': 'KELSON DA COSTA MEDEIROS', 'right_name': 'KELSON DA COSTA MEDEIROS',
             'positive_interger': 0, 'positive_decimal': 0.0, 'datetime': None, 'date': None, 'time': None},
            {'row_type': '9', 'detail_count': 2, 'row_count': 3, 'fill': ''}
        ]

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 2', Reader)

    def test_constructor_wrong_arguments(self):
        self.assertRaisesRegex(AssertionError, 'Iterator', Reader, 1, 2)
        self.assertRaisesRegex(AssertionError, 'Iterator', Reader, False, True)
        self.assertRaisesRegex(AssertionError, 'FileDescriptor', Reader, [], True)
        self.assertRaisesRegex(AssertionError, 'FileDescriptor', Reader, [], 1)
        self.assertRaisesRegex(AssertionError, 'FileDescriptor', Reader, [], 1)
        self.assertRaisesRegex(AssertionError, 'newline', Reader, [], self.file_descriptor, "")
        self.assertRaisesRegex(AssertionError, 'newline', Reader, [], self.file_descriptor, False)

    def test_validate_file_structure__wrong_line_size(self):
        self.assertRaisesRegex(AssertionError, 'correto.*163.*adequada',
                               Reader, io.StringIO(self.example01_wrong_line_size), self.file_descriptor, "\n")

    def test_validate_file_structure__wrong_iterable(self):
        class WrongIterator(Iterable):
            def __iter__(self):
                pass
        WrongIterator().__iter__()
        self.assertRaisesRegex(TypeError, 'Unsupported Iterable',
                               Reader, WrongIterator(), self.file_descriptor, "\n")

    def test_validate_file_structure__are_right_in_memory(self):
        reader = Reader(io.StringIO(self.example01_are_right), self.file_descriptor, "\n")
        self.assertEqual(4, reader.lines_count)

    def test_validate_file_structure__are_right_file(self):
        self.assertEqual(4, Reader(self.example01_are_right, self.file_descriptor, "\n").lines_count)
        with open('/src/tests/assets/example01_are_right.fwf') as f:
            self.assertEqual(4, Reader(f, self.file_descriptor, "\n").lines_count)
        self.assertEqual(4, Reader(self.example01_are_right, self.file_descriptor, "\n").lines_count)
        self.assertEqual(4, Reader(self.example01_are_right_lst, self.file_descriptor, "\n").lines_count)

    def test_iterate(self):
        self.assertListEqual(
            self.example01_are_right_expected,
            [row for row in Reader(self.example01_are_right, self.file_descriptor, "\n")])
        self.assertListEqual(
            self.example01_are_right_expected,
            [row for row in Reader(self.example01_are_right_lst, self.file_descriptor, "\n")])
