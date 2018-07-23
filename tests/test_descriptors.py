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
from pybatchfile.descriptors import ColumnDescriptor, RowDescriptor, HeaderRowDescriptor, FooterRowDescriptor, \
                                    DetailRowDescriptor, FileDescriptor


class TestColumnDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 3', ColumnDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(ColumnDescriptor("type", 1, 1, str, [], "desc"), ColumnDescriptor)

    def test_constructor_set_attr(self):
        cd = ColumnDescriptor("type", 1, 2, str, [], "desc")
        self.assertEqual("type", cd.name)
        self.assertEqual(1, cd.start)
        self.assertEqual(2, cd.size)
        self.assertEqual(str, cd.type)
        self.assertEqual([], cd.validations)
        self.assertEqual("desc", cd.description)

        cd2 = ColumnDescriptor("name", 1, 1)
        self.assertEqual(1, cd2.start)
        self.assertEqual(1, cd2.size)
        self.assertEqual(str, cd2.type)
        self.assertEqual([], cd2.validations)
        self.assertEqual("name", cd2.description)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, "name", ColumnDescriptor, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", ColumnDescriptor, "", "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", ColumnDescriptor, " ", "", "")
        self.assertRaisesRegex(AssertionError, "start", ColumnDescriptor, "name", "", "")
        self.assertRaisesRegex(AssertionError, "start.*0", ColumnDescriptor, "name", 0, "")
        self.assertRaisesRegex(AssertionError, "size", ColumnDescriptor, "name", 1, "")
        self.assertRaisesRegex(AssertionError, "size.*0", ColumnDescriptor, "name", 1, 0)
        self.assertRaisesRegex(AssertionError, "type.*class", ColumnDescriptor, "type", 1, 1, "")
        self.assertRaisesRegex(AssertionError, "validations.*List", ColumnDescriptor, "type", 1, 1, str, "")
        self.assertRaisesRegex(AssertionError, "description.*string", ColumnDescriptor, "name", 1, 1, str, [], 1)

    def test_end(self):
        cd = ColumnDescriptor("name", 1, 2, str, [], "desc")
        self.assertEqual(2, cd.end)


class TestRowDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', RowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(RowDescriptor([ColumnDescriptor("type", 1, 1),
                                             ColumnDescriptor("type", 2, 1)]), RowDescriptor)

    def test_constructor_set_attr(self):
        rd = RowDescriptor([ColumnDescriptor("type", 1, 1), ColumnDescriptor("name", 2, 10)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(2, len(rd.columns))
        self.assertEqual(11, rd.line_size)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, 'columns.*1.*', RowDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'columns.*List', RowDescriptor, 1)

    def test_invalid_positions(self):
        self.assertRaisesRegex(AssertionError, 'field \(starts in 3\).*type \(ends in 1\)', RowDescriptor,
                               [ColumnDescriptor('type', 1, 1), ColumnDescriptor('field', 3, 1)])


class TestHeaderRowDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', HeaderRowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(HeaderRowDescriptor([ColumnDescriptor("type", 1, 1)]), HeaderRowDescriptor)

    def test_constructor_set_attr(self):
        rd = DetailRowDescriptor([ColumnDescriptor("type", 1, 1)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(1, len(rd.columns))

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, 'columns.*1.*', HeaderRowDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'columns.*List', HeaderRowDescriptor, 1)


class TestFooterRowDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', FooterRowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(FooterRowDescriptor([ColumnDescriptor("type", 1, 1)]), FooterRowDescriptor)

    def test_constructor_set_attr(self):
        rd = FooterRowDescriptor([ColumnDescriptor("type", 1, 1), ColumnDescriptor("name", 2, 10)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(2, len(rd.columns))

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, 'columns.*1.*', FooterRowDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'columns.*List', FooterRowDescriptor, 1)


class TestDetailRowDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', DetailRowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(DetailRowDescriptor([ColumnDescriptor("type", 1, 1)]), DetailRowDescriptor)

    def test_constructor_set_attr(self):
        rd = DetailRowDescriptor([ColumnDescriptor("type", 1, 1)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(1, len(rd.columns))

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, 'columns.*1.*', DetailRowDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'columns.*List', DetailRowDescriptor, 1)


class TestFileDescriptor(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', FileDescriptor)

    def test_constructor_all_right(self):
        f = ColumnDescriptor("type", 1, 1)
        self.assertIsInstance(FileDescriptor([DetailRowDescriptor([f])]), FileDescriptor)
        self.assertIsInstance(FileDescriptor([DetailRowDescriptor([f])],
                                             HeaderRowDescriptor([f]),
                                             FooterRowDescriptor([f])), FileDescriptor)

    def test_constructor_wrong_args(self):
        col = ColumnDescriptor("type", 1, 1)
        dr = DetailRowDescriptor([col])
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List', FileDescriptor, col)
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List', FileDescriptor, 1)
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*1 DetailRow', FileDescriptor, [])
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List.*DetailRow', FileDescriptor, [1])
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List.*DetailRow', FileDescriptor, [col], 1)
        self.assertRaisesRegex(AssertionError, 'details_descriptors.*List', FileDescriptor, dr, 1)
        self.assertRaisesRegex(AssertionError, 'header_descriptor.*HeaderRow', FileDescriptor, [dr], 1)
        self.assertRaisesRegex(AssertionError, 'footer_descriptor.*FooterRow', FileDescriptor, [dr], None, 1)

    def test_constructor_set_attr(self):
        t = ColumnDescriptor("type", 1, 1)
        fd = FileDescriptor([DetailRowDescriptor([t])], HeaderRowDescriptor([t]), FooterRowDescriptor([t]))
        self.assertIsInstance(fd, FileDescriptor)
        self.assertIsInstance(fd.header_descriptor, HeaderRowDescriptor)
        self.assertIsInstance(fd.footer_descriptor, FooterRowDescriptor)
        self.assertIsInstance(fd.details_descriptors, list)

    def test_constructor_invalid_line_size(self):
        t = ColumnDescriptor("type", 1, 1)
        self.assertRaisesRegex(AssertionError, 'header \(1\).*footer \(2\).*details \(\[1\]\)')
