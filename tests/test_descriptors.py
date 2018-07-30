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

import json, io
from unittest import TestCase
from fwf.columns import CharColumn, RightCharColumn, PositiveIntegerColumn, PositiveDecimalColumn, \
    DateTimeColumn, DateColumn, TimeColumn
from fwf.descriptors import RowDescriptor, HeaderRowDescriptor, \
    FooterRowDescriptor, DetailRowDescriptor, FileDescriptor
from fwf.renders import render_as_markdown


class TestRowDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', RowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(RowDescriptor([CharColumn("type", 1),
                                             CharColumn("type", 1)]), RowDescriptor)

    def test_constructor_set_attr(self):
        rd = RowDescriptor([CharColumn("type", 1), CharColumn("name", 10)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(2, len(rd.columns))
        self.assertEqual(11, rd.line_size)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(TypeError, 'missing.*columns', RowDescriptor)
        self.assertRaisesRegex(AssertionError, 'columns.*List', RowDescriptor, None)
        self.assertRaisesRegex(AssertionError, 'columns.*1.*', RowDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'columns.*List', RowDescriptor, 1)

    # def test_dehydrate(self):
    #     self.assertListEqual(
    #         [{'type': 'fwf.columns.CharColumn',
    #           'attributes': {'name': 'a_char', 'size': 1, 'description': 'a_char'}}],
    #         RowDescriptor([CharColumn("a_char", 1), ]).dehydrate()
    #     )
    #     self.assertListEqual(
    #         [{'type': 'fwf.columns.RightCharColumn',
    #           'attributes': {'name': 'a_rchar', 'size': 10, 'description': 'a_rchar'}}],
    #         RowDescriptor([RightCharColumn("a_rchar", 10)]).dehydrate()
    #     )
    #     self.assertListEqual(
    #         [{'type': 'fwf.columns.PositiveIntegerColumn',
    #           'attributes': {'name': 'a_int', 'size': 20, 'description': 'a_int'}}],
    #         RowDescriptor([PositiveIntegerColumn("a_int", 20)]).dehydrate()
    #     )
    #     self.assertListEqual(
    #         [{'type': 'fwf.columns.PositiveDecimalColumn',
    #           'attributes': {'name': 'a_float', 'size': 30, 'decimals': 2, 'description': 'a_float'}}],
    #         RowDescriptor([PositiveDecimalColumn("a_float", 30)]).dehydrate()
    #     )
    #     self.assertListEqual(
    #         [{'type': 'fwf.columns.DateTimeColumn',
    #           'attributes': {'name': 'a_datetime', 'format': '%d%m%Y%H%M', 'description': 'a_datetime'}}],
    #         RowDescriptor([DateTimeColumn("a_datetime")]).dehydrate()
    #     )
    #     self.assertListEqual(
    #         [{'type': 'fwf.columns.DateColumn',
    #           'attributes': {'name': 'a_date', 'format': '%d%m%Y', 'description': 'a_date'}}],
    #         RowDescriptor([DateColumn("a_date")]).dehydrate()
    #     )
    #     self.assertListEqual(
    #         [{'type': 'fwf.columns.TimeColumn',
    #           'attributes': {'name': 'a_time', 'format': '%H%M', 'description': 'a_time'}}],
    #         RowDescriptor([TimeColumn("a_time")]).dehydrate()
    #     )


class TestHeaderRowDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', HeaderRowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(HeaderRowDescriptor([CharColumn("type", 1)]), HeaderRowDescriptor)

    def test_constructor_set_attr(self):
        rd = DetailRowDescriptor([CharColumn("type", 1)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(1, len(rd.columns))

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(TypeError, 'missing.*columns', HeaderRowDescriptor)
        self.assertRaisesRegex(AssertionError, 'columns.*1.*', HeaderRowDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'columns.*List', HeaderRowDescriptor, None)
        self.assertRaisesRegex(AssertionError, 'columns.*List', HeaderRowDescriptor, 1)


class TestFooterRowDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', FooterRowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(FooterRowDescriptor([CharColumn("type", 1)]), FooterRowDescriptor)

    def test_constructor_set_attr(self):
        rd = FooterRowDescriptor([CharColumn("type", 1), CharColumn("name", 10)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(2, len(rd.columns))

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(TypeError, 'missing.*columns', FooterRowDescriptor)
        self.assertRaisesRegex(AssertionError, 'columns.*1.*', FooterRowDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'columns.*List', FooterRowDescriptor, None)
        self.assertRaisesRegex(AssertionError, 'columns.*List', FooterRowDescriptor, 1)


class TestDetailRowDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', DetailRowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(DetailRowDescriptor([CharColumn("type", 1)]), DetailRowDescriptor)

    def test_constructor_set_attr(self):
        rd = DetailRowDescriptor([CharColumn("type", 1)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(1, len(rd.columns))

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, 'columns.*1.*', DetailRowDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'columns.*List', DetailRowDescriptor, 1)


class TestFileDescriptor(TestCase):

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

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', FileDescriptor)

    def test_constructor_all_right(self):
        f = CharColumn("type", 1)
        self.assertIsInstance(FileDescriptor([DetailRowDescriptor([f])]), FileDescriptor)
        self.assertIsInstance(FileDescriptor([DetailRowDescriptor([f])],
                                             HeaderRowDescriptor([f]),
                                             FooterRowDescriptor([f])), FileDescriptor)

    def test_constructor_wrong_args(self):
        col = CharColumn("type", 1)
        dr = DetailRowDescriptor([col])
        self.assertRaisesRegex(AssertionError, 'details.*List', FileDescriptor, col)
        self.assertRaisesRegex(AssertionError, 'details.*List', FileDescriptor, None)
        self.assertRaisesRegex(AssertionError, 'details.*List', FileDescriptor, 1)
        self.assertRaisesRegex(AssertionError, 'details.*1 DetailRow', FileDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'details.*List.*DetailRow', FileDescriptor, [1])
        self.assertRaisesRegex(AssertionError, 'details.*List.*DetailRow', FileDescriptor, [col], 1)
        self.assertRaisesRegex(AssertionError, 'details.*List', FileDescriptor, dr, 1)
        self.assertRaisesRegex(AssertionError, 'header.*HeaderRow', FileDescriptor, [dr], 1)
        self.assertRaisesRegex(AssertionError, 'footer.*FooterRow', FileDescriptor, [dr], None, 1)

    def test_constructor_set_attr(self):
        t = CharColumn("type", 1)
        fd = FileDescriptor([DetailRowDescriptor([t])], HeaderRowDescriptor([t]), FooterRowDescriptor([t]))
        self.assertIsInstance(fd, FileDescriptor)
        self.assertIsInstance(fd.header, HeaderRowDescriptor)
        self.assertIsInstance(fd.footer, FooterRowDescriptor)
        self.assertIsInstance(fd.details, list)

    def test_constructor_invalid_line_size(self):
        t = CharColumn("type", 1)
        self.assertRaisesRegex(AssertionError, 'header \(1\).*footer \(2\).*details \(\[1\]\)')

    # def test_dehydrate(self):
    #     self.assertDictEqual(json.loads(self.example01_json), self.file_descriptor.dehydrate())

    # def test_hydrate(self):
    #     FileDescriptor.hydrate(json.loads(self.example01_json))


    # def test_file_format_validate(self):
    #     fd = FileDescriptor(
    #         [
    #             DetailRowDescriptor([
    #                 CharColumn('row_type', 1),
    #                 CharColumn('name', 60),
    #                 RightCharColumn('right_name', 60),
    #                 PositiveIntegerColumn('positive_interger', 9),
    #                 PositiveDecimalColumn('positive_decimal', 9),
    #                 DateTimeColumn('datetime'),
    #                 DateColumn('date'),
    #                 TimeColumn('time'),
    #             ])
    #         ],
    #         HeaderRowDescriptor([
    #             CharColumn('row_type', 1),
    #             CharColumn('filetype', 5),
    #             CharColumn('fill', 157),
    #         ]),
    #         FooterRowDescriptor([
    #             CharColumn('row_type', 1),
    #             PositiveIntegerColumn('detail_count', 4),
    #             PositiveIntegerColumn('row_count', 4),
    #             CharColumn('fill', 154),
    #         ]),
    #     )
    #
    #


class TestRenders(TestCase):

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

    def test_render_as_markdown(self):
        with io.StringIO() as buf:
            render_as_markdown(self.file_descriptor, buf)
            self.assertEqual(self.example01_markdown, buf.getvalue())
