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
    RowDescriptor,
)


class TestRowDescriptor(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 1", RowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(RowDescriptor([CharColumn("type", 1), CharColumn("type", 1)]), RowDescriptor)

    def test_constructor_set_attr(self):
        rd = RowDescriptor([CharColumn("type", 1), CharColumn("name", 10)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(2, len(rd.columns))
        self.assertEqual(11, rd.line_size)

    def test_constructor_wrong_args(self):
        self.assertRaises(TypeError, RowDescriptor)
        self.assertRaises(TypeError, RowDescriptor, None)
        self.assertRaises(ValueError, RowDescriptor, [])
        self.assertRaises(TypeError, RowDescriptor, 1)


class TestHeaderRowDescriptor(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 1", HeaderRowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(HeaderRowDescriptor([CharColumn("type", 1)]), HeaderRowDescriptor)

    def test_constructor_set_attr(self):
        rd = DetailRowDescriptor([CharColumn("type", 1)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(1, len(rd.columns))

    def test_constructor_wrong_args(self):
        self.assertRaises(TypeError, HeaderRowDescriptor)
        self.assertRaises(ValueError, HeaderRowDescriptor, [])
        self.assertRaises(TypeError, HeaderRowDescriptor, None)
        self.assertRaises(TypeError, HeaderRowDescriptor, 1)


class TestFooterRowDescriptor(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 1", FooterRowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(FooterRowDescriptor([CharColumn("type", 1)]), FooterRowDescriptor)

    def test_constructor_set_attr(self):
        rd = FooterRowDescriptor([CharColumn("type", 1), CharColumn("name", 10)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(2, len(rd.columns))

    def test_constructor_wrong_args(self):
        self.assertRaises(TypeError, FooterRowDescriptor)
        self.assertRaises(ValueError, FooterRowDescriptor, [])
        self.assertRaises(TypeError, FooterRowDescriptor, None)
        self.assertRaises(TypeError, FooterRowDescriptor, 1)


class TestDetailRowDescriptor(TestCase):
    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 1", DetailRowDescriptor)

    def test_constructor_all_right(self):
        self.assertIsInstance(DetailRowDescriptor([CharColumn("type", 1)]), DetailRowDescriptor)

    def test_constructor_set_attr(self):
        rd = DetailRowDescriptor([CharColumn("type", 1)])
        self.assertIsInstance(rd.columns, list)
        self.assertEqual(1, len(rd.columns))

    def test_constructor_wrong_args(self):
        self.assertRaises(ValueError, DetailRowDescriptor, [])
        self.assertRaises(TypeError, DetailRowDescriptor, 1)


class TestFileDescriptor(TestCase):
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

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, "missing 1", FileDescriptor)

    def test_constructor_all_right(self):
        f = CharColumn("type", 1)
        self.assertIsInstance(FileDescriptor([DetailRowDescriptor([f])]), FileDescriptor)
        self.assertIsInstance(
            FileDescriptor([DetailRowDescriptor([f])], HeaderRowDescriptor([f])),
            FileDescriptor,
        )
        self.assertIsInstance(
            FileDescriptor(
                [DetailRowDescriptor([f])],
                HeaderRowDescriptor([f]),
                FooterRowDescriptor([f]),
            ),
            FileDescriptor,
        )

    def test_constructor_wrong_args(self):
        col = CharColumn("type", 1)
        dr = DetailRowDescriptor([col])
        self.assertRaises(TypeError, FileDescriptor, col)
        self.assertRaises(TypeError, FileDescriptor, None)
        self.assertRaises(TypeError, FileDescriptor, 1)
        self.assertRaises(ValueError, FileDescriptor, [])
        self.assertRaises(TypeError, FileDescriptor, [1])
        self.assertRaises(TypeError, FileDescriptor, [col], 1)
        self.assertRaises(TypeError, FileDescriptor, dr, 1)
        self.assertRaises(TypeError, FileDescriptor, [dr], 1)
        self.assertRaises(TypeError, FileDescriptor, [dr], None, 1)

    def test_constructor_set_attr(self):
        t = CharColumn("type", 1)
        fd = FileDescriptor(
            [DetailRowDescriptor([t])],
            HeaderRowDescriptor([t]),
            FooterRowDescriptor([t]),
        )
        self.assertIsInstance(fd, FileDescriptor)
        self.assertIsInstance(fd.header, HeaderRowDescriptor)
        self.assertIsInstance(fd.footer, FooterRowDescriptor)
        self.assertIsInstance(fd.details, list)

    def test_constructor_invalid_line_size(self):
        self.assertRaises(
            ValueError,
            FileDescriptor,
            [DetailRowDescriptor([CharColumn("type", 1)])],
            HeaderRowDescriptor([CharColumn("type", 1)]),
            FooterRowDescriptor([CharColumn("type", 1), CharColumn("other", 1)]),
        )

    def test_validate_positions_col_start_not_1_manual(self):
        # Cria um RowDescriptor válido e depois corrompe o start da coluna
        col = CharColumn("col1", 2)
        rd = RowDescriptor([col])
        rd.columns[0].start = 2  # Corrupção manual
        with self.assertRaises(ValueError):
            rd.validate_positions()

    def test_validate_positions_col_not_sequential_manual(self):
        # Cria dois CharColumns válidos e depois corrompe o start do segundo
        col1 = CharColumn("col1", 2)
        col2 = CharColumn("col2", 2)
        rd = RowDescriptor([col1, col2])
        rd.columns[1].start = rd.columns[0].end + 2  # Corrupção manual
        with self.assertRaises(ValueError):
            rd.validate_positions()
