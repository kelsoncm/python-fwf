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

from unittest import TestCase
from pybatchfile.columns import CharColumn
from pybatchfile.descriptors import RowDescriptor, HeaderRowDescriptor, \
    FooterRowDescriptor, DetailRowDescriptor, FileDescriptor


class TestRowDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', RowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(RowDescriptor([CharColumn("type", 1, 1),
                                             CharColumn("type", 2, 1)]), RowDescriptor)

    def test_constructor_set_attr(self):
        rd = RowDescriptor([CharColumn("type", 1, 1), CharColumn("name", 2, 10)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(2, len(rd.columns))
        self.assertEqual(11, rd.line_size)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(TypeError, 'missing.*columns', RowDescriptor)
        self.assertRaisesRegex(AssertionError, 'columns.*List', RowDescriptor, None)
        self.assertRaisesRegex(AssertionError, 'columns.*1.*', RowDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'columns.*List', RowDescriptor, 1)

    def test_invalid_positions(self):
        self.assertRaisesRegex(AssertionError, 'field \(starts in 3\).*type \(ends in 1\)', RowDescriptor,
                               [CharColumn('type', 1, 1), CharColumn('field', 3, 1)])


class TestHeaderRowDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', HeaderRowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(HeaderRowDescriptor([CharColumn("type", 1, 1)]), HeaderRowDescriptor)

    def test_constructor_set_attr(self):
        rd = DetailRowDescriptor([CharColumn("type", 1, 1)])
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
        self.assertIsInstance(FooterRowDescriptor([CharColumn("type", 1, 1)]), FooterRowDescriptor)

    def test_constructor_set_attr(self):
        rd = FooterRowDescriptor([CharColumn("type", 1, 1), CharColumn("name", 2, 10)])
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
        self.assertIsInstance(DetailRowDescriptor([CharColumn("type", 1, 1)]), DetailRowDescriptor)

    def test_constructor_set_attr(self):
        rd = DetailRowDescriptor([CharColumn("type", 1, 1)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(1, len(rd.columns))

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, 'columns.*1.*', DetailRowDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'columns.*List', DetailRowDescriptor, 1)


class TestFileDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', FileDescriptor)

    def test_constructor_all_right(self):
        f = CharColumn("type", 1, 1)
        self.assertIsInstance(FileDescriptor([DetailRowDescriptor([f])]), FileDescriptor)
        self.assertIsInstance(FileDescriptor([DetailRowDescriptor([f])],
                                             HeaderRowDescriptor([f]),
                                             FooterRowDescriptor([f])), FileDescriptor)

    def test_constructor_wrong_args(self):
        col = CharColumn("type", 1, 1)
        dr = DetailRowDescriptor([col])
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List', FileDescriptor, col)
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List', FileDescriptor, None)
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List', FileDescriptor, 1)
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*1 DetailRow', FileDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List.*DetailRow', FileDescriptor, [1])
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List.*DetailRow', FileDescriptor, [col], 1)
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List', FileDescriptor, dr, 1)
        self.assertRaisesRegex(AssertionError, 'header_descriptor.*HeaderRow', FileDescriptor, [dr], 1)
        self.assertRaisesRegex(AssertionError, 'footer_descriptor.*FooterRow', FileDescriptor, [dr], None, 1)

    def test_constructor_set_attr(self):
        t = CharColumn("type", 1, 1)
        fd = FileDescriptor([DetailRowDescriptor([t])], HeaderRowDescriptor([t]), FooterRowDescriptor([t]))
        self.assertIsInstance(fd, FileDescriptor)
        self.assertIsInstance(fd.header_descriptor, HeaderRowDescriptor)
        self.assertIsInstance(fd.footer_descriptor, FooterRowDescriptor)
        self.assertIsInstance(fd.details_descriptors, list)

    def test_constructor_invalid_line_size(self):
        t = CharColumn("type", 1, 1)
        self.assertRaisesRegex(AssertionError, 'header \(1\).*footer \(2\).*details \(\[1\]\)')
