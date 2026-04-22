from unittest import TestCase

from pyfwf.columns import CharColumn
from pyfwf.descriptors import (
    DetailRowDescriptor,
    FileDescriptor,
    FooterRowDescriptor,
    HeaderRowDescriptor,
)
from pyfwf.readers import Reader


class TestReaderStringInput(TestCase):
    """Test Reader with string input"""

    def setUp(self):
        self.fd = FileDescriptor([DetailRowDescriptor([CharColumn("c1", 5), CharColumn("c2", 4)])])

    def test_string_input_single_newline(self):
        """Test reading from string with \\n newline"""
        content = "AAAAA BBB\n"
        reader = Reader(content, self.fd, newline="\n")
        rows = list(reader)
        self.assertEqual(1, len(rows))
        self.assertEqual({"c1": "AAAAA", "c2": "BBB"}, rows[0])

    def test_list_input_single_newline(self):
        """Test reading from list with \\n newline"""
        lines = ["AAAAA BBB\n", "CCCCC DDD\n"]
        reader = Reader(lines, self.fd, newline="\n")
        rows = list(reader)
        self.assertEqual(2, len(rows))
        self.assertEqual({"c1": "AAAAA", "c2": "BBB"}, rows[0])
        self.assertEqual({"c1": "CCCCC", "c2": "DDD"}, rows[1])

    def test_iterator_protocol(self):
        """Test iterator protocol"""
        reader = Reader("AAAAA BBB\n", self.fd, newline="\n")
        self.assertEqual(reader, iter(reader))
        row = next(reader)
        self.assertEqual({"c1": "AAAAA", "c2": "BBB"}, row)


class TestReaderWithHeader(TestCase):
    """Test Reader with header row"""

    def setUp(self):
        self.fd = FileDescriptor(
            [DetailRowDescriptor([CharColumn("d1", 5), CharColumn("d2", 4)])],
            HeaderRowDescriptor([CharColumn("h1", 5), CharColumn("h2", 4)]),
        )

    def test_header_reading(self):
        """Test reading file with header"""
        content = "HHHHH HHH\nAAAAA BBB\n"
        reader = Reader(content, self.fd, newline="\n")
        rows = list(reader)
        self.assertEqual(2, len(rows))
        self.assertEqual({"h1": "HHHHH", "h2": "HHH"}, rows[0])
        self.assertEqual({"d1": "AAAAA", "d2": "BBB"}, rows[1])


class TestReaderWithFooter(TestCase):
    """Test Reader with footer row"""

    def setUp(self):
        self.fd = FileDescriptor(
            [DetailRowDescriptor([CharColumn("d1", 5), CharColumn("d2", 4)])],
            footer=FooterRowDescriptor([CharColumn("f1", 5), CharColumn("f2", 4)]),
        )

    def test_footer_reading(self):
        """Test reading file with footer"""
        content = "AAAAA BBB\nFFFFF FFF\n"
        reader = Reader(content, self.fd, newline="\n")
        rows = list(reader)
        self.assertEqual(2, len(rows))
        self.assertEqual({"f1": "FFFFF", "f2": "FFF"}, rows[1])


class TestReaderWithBoth(TestCase):
    """Test Reader with header and footer"""

    def setUp(self):
        self.fd = FileDescriptor(
            [DetailRowDescriptor([CharColumn("d1", 5), CharColumn("d2", 4)])],
            HeaderRowDescriptor([CharColumn("h1", 5), CharColumn("h2", 4)]),
            FooterRowDescriptor([CharColumn("f1", 5), CharColumn("f2", 4)]),
        )

    def test_header_footer(self):
        """Test header and footer"""
        content = "HHHHH HHH\nAAAAA BBB\nCCCCC DDD\nFFFFF FFF\n"
        reader = Reader(content, self.fd, newline="\n")
        rows = list(reader)
        self.assertEqual(4, len(rows))


class TestReaderNewline(TestCase):
    """Test Reader newline handling"""

    def setUp(self):
        self.fd = FileDescriptor([DetailRowDescriptor([CharColumn("c1", 5), CharColumn("c2", 4)])])

    def test_newline_lf(self):
        """Test newline LF"""
        reader = Reader("AAAAA BBB\n", self.fd, newline="\n")
        rows = list(reader)
        self.assertEqual(1, len(rows))

    def test_newline_cr(self):
        """Test newline CR"""
        reader = Reader("AAAAA BBB\r", self.fd, newline="\r")
        rows = list(reader)
        self.assertEqual(1, len(rows))

    def test_multiple_lines(self):
        """Test multiple lines"""
        content = "AAAAA BBB\nCCCCC DDD\n"
        reader = Reader(content, self.fd, newline="\n")
        rows = list(reader)
        self.assertEqual(2, len(rows))
        self.assertEqual({"c1": "AAAAA", "c2": "BBB"}, rows[0])
        self.assertEqual({"c1": "CCCCC", "c2": "DDD"}, rows[1])


class TestReaderInvalid(TestCase):
    """Test Reader validation"""

    def setUp(self):
        self.fd = FileDescriptor([DetailRowDescriptor([CharColumn("c1", 5), CharColumn("c2", 4)])])

    def test_invalid_iterable(self):
        """Test invalid iterable"""
        with self.assertRaises(TypeError):
            Reader(123, self.fd)

    def test_invalid_descriptor(self):
        """Test invalid descriptor"""
        with self.assertRaises(TypeError):
            Reader("AAAAA BBB\n", "bad")

    def test_invalid_newline(self):
        """Test invalid newline"""
        with self.assertRaises(ValueError):
            Reader("AAAAA BBB\n", self.fd, newline="\t")

    def test_wrong_line_size(self):
        """Test wrong line size"""
        with self.assertRaises(ValueError):
            Reader("SHORT\n", self.fd)


class TestReaderTextIOWrapper(TestCase):
    """Test Reader TextIOWrapper branch"""

    def test_textiowrapper_branch(self):
        # Testa o ramo do TextIOWrapper para cobertura
        import io

        fd = FileDescriptor([DetailRowDescriptor([CharColumn("c1", 5), CharColumn("c2", 4)])])

        # TextIOWrapper espera um arquivo real, então criamos um mock
        class DummyTextIO(io.TextIOWrapper):
            def __init__(self):
                pass

            def read(self):
                return "AAAAA BBB\n"

        dummy = DummyTextIO()
        dummy.read = lambda: "AAAAA BBB\n"
        Reader(dummy, fd, newline="\n")


class TestReaderUnsupportedType(TestCase):
    def test_unsupported_iterable_type(self):
        fd = FileDescriptor([DetailRowDescriptor([CharColumn("c1", 5)])])

        class WeirdIterable:
            pass

        with self.assertRaises(TypeError):
            Reader(WeirdIterable(), fd)  # Iterable customizado não suportado
