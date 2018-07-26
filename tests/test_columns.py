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
from pybatchfile.columns import CharColumn, RightCharColumn, PositiveIntegerColumn, PositiveDecimalColumn, \
    DateTimeColumn, DateColumn, TimeColumn
from datetime import datetime, date, time


class TestCharColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 3', CharColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(CharColumn("type", 1, 1, "desc"), CharColumn)

    def test_constructor_set_attr(self):
        cd = CharColumn("type", 1, 2, "desc")
        self.assertEqual("type", cd.name)
        self.assertEqual(1, cd.start)
        self.assertEqual(2, cd.size)
        self.assertEqual("desc", cd.description)

        cd2 = CharColumn("name", 1, 1)
        self.assertEqual(1, cd2.start)
        self.assertEqual(1, cd2.size)
        self.assertEqual("name", cd2.description)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, "name", CharColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", CharColumn, "", "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", CharColumn, " ", "", "")
        self.assertRaisesRegex(AssertionError, "start", CharColumn, "name", "", "")
        self.assertRaisesRegex(AssertionError, "start.*0", CharColumn, "name", 0, "")
        self.assertRaisesRegex(AssertionError, "size", CharColumn, "name", 1, "")
        self.assertRaisesRegex(AssertionError, "size.*0", CharColumn, "name", 1, 0)
        self.assertRaisesRegex(AssertionError, "description.*string", CharColumn, "name", 1, 1, 1)

    def test_end(self):
        cd = CharColumn("name", 1, 2, "desc")
        self.assertEqual(2, cd.end)

    def test_to_value_invalid(self):
        cd = CharColumn("name", 1, 2, "desc")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 1)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "333")

    def test_to_value_valid(self):
        cd = CharColumn("name", 1, 2, "desc")
        self.assertEqual("22", cd.to_value("22"))
        self.assertEqual("2", cd.to_value("2 "))
        self.assertEqual("2", cd.to_value(" 2"))

    def test_to_str_invalid(self):
        cd = CharColumn("name", 1, 4, "desc")
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, 1)
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, 12345)
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, True)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, "12345")
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, "123  ")

    def test_to_str_valid(self):
        cd = CharColumn("name", 1, 4, "desc")
        self.assertEqual("asdf", cd.to_str("asdf"))
        self.assertEqual("a   ", cd.to_str("a "))
        self.assertEqual("    ", cd.to_str(""))
        self.assertEqual("    ", cd.to_str(" "))


class TestRightCharColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 3', RightCharColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(RightCharColumn("type", 1, 1, "desc"), RightCharColumn)

    def test_constructor_set_attr(self):
        cd = RightCharColumn("type", 1, 2, "desc")
        self.assertEqual("type", cd.name)
        self.assertEqual(1, cd.start)
        self.assertEqual(2, cd.size)
        self.assertEqual("desc", cd.description)

        cd2 = RightCharColumn("name", 1, 1)
        self.assertEqual(1, cd2.start)
        self.assertEqual(1, cd2.size)
        self.assertEqual("name", cd2.description)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, "name", RightCharColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", RightCharColumn, "", "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", RightCharColumn, " ", "", "")
        self.assertRaisesRegex(AssertionError, "start", RightCharColumn, "name", "", "")
        self.assertRaisesRegex(AssertionError, "start.*0", RightCharColumn, "name", 0, "")
        self.assertRaisesRegex(AssertionError, "size", RightCharColumn, "name", 1, "")
        self.assertRaisesRegex(AssertionError, "size.*0", RightCharColumn, "name", 1, 0)
        self.assertRaisesRegex(AssertionError, "description.*string", RightCharColumn, "name", 1, 1, 1)

    def test_end(self):
        cd = RightCharColumn("name", 1, 2, "desc")
        self.assertEqual(2, cd.end)

    def test_to_value_invalid(self):
        cd = RightCharColumn("name", 1, 2, "desc")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 1)
        self.assertRaisesRegex(AssertionError, "string", cd.to_value, 12345)
        self.assertRaisesRegex(AssertionError, "string", cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "333")

    def test_to_value_valid(self):
        cd = RightCharColumn("name", 1, 2, "desc")
        self.assertEqual("22", cd.to_value("22"))
        self.assertEqual("2", cd.to_value("2 "))
        self.assertEqual("2", cd.to_value(" 2"))

    def test_to_str_invalid(self):
        cd = RightCharColumn("name", 1, 4, "desc")
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, 1)
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, 12345)
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, True)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, "12345")
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, "123  ")

    def test_to_str_valid(self):
        cd = RightCharColumn("name", 1, 4, "desc")
        self.assertEqual("asdf", cd.to_str("asdf"))
        self.assertEqual("  a ", cd.to_str("a "))
        self.assertEqual("   a", cd.to_str("a"))
        self.assertEqual("    ", cd.to_str(""))
        self.assertEqual("    ", cd.to_str(" "))
        self.assertEqual("    ", cd.to_str(None))


class TestPositiveIntegerColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 3', PositiveIntegerColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(PositiveIntegerColumn("type", 1, 1, "desc"), PositiveIntegerColumn)

    def test_constructor_set_attr(self):
        cd = PositiveIntegerColumn("type", 1, 2, "the type")
        self.assertEqual("type", cd.name)
        self.assertEqual(1, cd.start)
        self.assertEqual(2, cd.size)
        self.assertEqual("the type", cd.description)

        cd2 = PositiveIntegerColumn("name", 1, 1)
        self.assertEqual(1, cd2.start)
        self.assertEqual(1, cd2.size)
        self.assertEqual("name", cd2.description)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, "name", PositiveIntegerColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", PositiveIntegerColumn, "", "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", PositiveIntegerColumn, " ", "", "")
        self.assertRaisesRegex(AssertionError, "start", PositiveIntegerColumn, "name", "", "")
        self.assertRaisesRegex(AssertionError, "start.*0", PositiveIntegerColumn, "name", 0, "")
        self.assertRaisesRegex(AssertionError, "size", PositiveIntegerColumn, "name", 1, "")
        self.assertRaisesRegex(AssertionError, "size.*0", PositiveIntegerColumn, "name", 1, 0)
        self.assertRaisesRegex(AssertionError, "description.*string", PositiveIntegerColumn, "name", 1, 1, 1)

    def test_end(self):
        cd = PositiveIntegerColumn("name", 1, 2, "desc")
        self.assertEqual(2, cd.end)

    def test_to_value_invalid(self):
        cd = PositiveIntegerColumn("name", 1, 2, "desc")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 12)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(AssertionError, 'positive int', cd.to_value, "-1")
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "333")
        self.assertRaisesRegex(ValueError, 'invalid literal for int', cd.to_value, "A1")

    def test_to_value_valid(self):
        cd = PositiveIntegerColumn("name", 1, 2, "desc")
        self.assertEqual(22, cd.to_value("22"))
        self.assertEqual(2, cd.to_value("2 "))
        self.assertEqual(2, cd.to_value(" 2"))

    def test_to_str_invalid(self):
        cd = PositiveIntegerColumn("name", 1, 4, "desc")
        self.assertRaisesRegex(AssertionError, "'positive int' or 'None'", cd.to_str, '1')
        self.assertRaisesRegex(AssertionError, "'positive int' or 'None'", cd.to_str, '-123')
        self.assertRaisesRegex(AssertionError, "'positive int' or 'None'", cd.to_str, '12345')
        self.assertRaisesRegex(AssertionError, "'positive int' or 'None'", cd.to_str, True)
        self.assertRaisesRegex(AssertionError, "'positive int' or 'None'", cd.to_str, -1)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, 12345)

    def test_to_str_valid(self):
        cd = PositiveIntegerColumn("name", 1, 4, "year")
        self.assertEqual("0001", cd.to_str(1))
        self.assertEqual("1234", cd.to_str(1234))
        self.assertEqual("0000", cd.to_str(0))
        self.assertEqual("0000", cd.to_str(None))


class TestPositiveDecimalColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 3', PositiveDecimalColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(PositiveDecimalColumn("type", 1, 3), PositiveDecimalColumn)
        self.assertIsInstance(PositiveDecimalColumn("type", 1, 3, 2), PositiveDecimalColumn)
        self.assertIsInstance(PositiveDecimalColumn("type", 1, 3, 2, "desc"), PositiveDecimalColumn)

    def test_constructor_set_attr(self):
        cd2 = PositiveDecimalColumn("value", 1, 4)
        self.assertEqual(1, cd2.start)
        self.assertEqual(4, cd2.size)
        self.assertEqual("value", cd2.description)

        cd2 = PositiveDecimalColumn("value", 1, 4, decimals=2)
        self.assertEqual(1, cd2.start)
        self.assertEqual(4, cd2.size)
        self.assertEqual("value", cd2.description)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, "name", PositiveDecimalColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", PositiveDecimalColumn, "", "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", PositiveDecimalColumn, " ", "", "")
        self.assertRaisesRegex(AssertionError, "start", PositiveDecimalColumn, "name", "", "")
        self.assertRaisesRegex(AssertionError, "start.*0", PositiveDecimalColumn, "name", 0, "")
        self.assertRaisesRegex(AssertionError, "size", PositiveDecimalColumn, "name", 1, "")
        self.assertRaisesRegex(AssertionError, "size.*0", PositiveDecimalColumn, "name", 1, 0)
        self.assertRaisesRegex(AssertionError, "description.*string", PositiveDecimalColumn, "name", 1, 3, 1, -1)
        self.assertRaisesRegex(AssertionError, "decimais.*inteiro", PositiveDecimalColumn, "name", 1, 1, "1")
        self.assertRaisesRegex(AssertionError, "decimais.*maior que 0", PositiveDecimalColumn, "value", 1, 1, 0)
        self.assertRaisesRegex(AssertionError, "decimais.*size", PositiveDecimalColumn, "value", 1, 1)
        self.assertRaisesRegex(AssertionError, "decimais.*size", PositiveDecimalColumn, "value", 1, 1, 2)
        self.assertRaisesRegex(AssertionError, "decimais.*size", PositiveDecimalColumn, "value", 1, 1, 1)
        self.assertRaisesRegex(AssertionError, "decimais.*maior que 0", PositiveDecimalColumn, "value", 1, 1, 0)

    def test_end(self):
        cd = PositiveDecimalColumn("name", 1, 2, 1, "desc")
        self.assertEqual(2, cd.end)

    def test_to_value_invalid(self):
        cd = PositiveDecimalColumn("name", 1, 2, 1, "desc")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 12)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, -1.0)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(AssertionError, 'positive decimal', cd.to_value, "-1")
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "333")
        self.assertRaisesRegex(ValueError, 'invalid literal for int', cd.to_value, "A1")

    def test_to_value_valid(self):
        cd = PositiveDecimalColumn("value", 1, 3, 2)
        self.assertEqual(1.23, cd.to_value("123"))
        self.assertEqual(0.01, cd.to_value("1  "))
        self.assertEqual(0.02, cd.to_value(" 2 "))
        self.assertEqual(0.03, cd.to_value("  3"))

    def test_to_str_invalid(self):
        cd = PositiveDecimalColumn("value", 1, 4, 2)
        self.assertRaisesRegex(AssertionError, "'positive decimal' or 'None'", cd.to_str, '1')
        self.assertRaisesRegex(AssertionError, "'positive decimal' or 'None'", cd.to_str, '-123')
        self.assertRaisesRegex(AssertionError, "'positive decimal' or 'None'", cd.to_str, '12345')
        self.assertRaisesRegex(AssertionError, "'positive decimal' or 'None'", cd.to_str, True)
        self.assertRaisesRegex(AssertionError, "'positive decimal' or 'None'", cd.to_str, -1)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, 123.45)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, 123.0)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, 1234.0)

    def test_to_str_valid(self):
        cd = PositiveDecimalColumn("value", 1, 4)
        self.assertEqual("0100", cd.to_str(1.0))
        self.assertEqual("1234", cd.to_str(12.34))
        self.assertEqual("0000", cd.to_str(0.0))
        self.assertEqual("0012", cd.to_str(0.12))
        self.assertEqual("0010", cd.to_str(0.1))
        self.assertEqual("0000", cd.to_str(None))


class TestDateTimeColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 2', DateTimeColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(DateTimeColumn("type", 1), DateTimeColumn)
        self.assertIsInstance(DateTimeColumn("type", 1, "%d%m%Y%H%M"), DateTimeColumn)
        self.assertIsInstance(DateTimeColumn("type", 1, "%d%m%Y%H%M", "desc"), DateTimeColumn)

    def test_constructor_set_attr(self):
        cd2 = DateTimeColumn("dt", 1)
        self.assertEqual(1, cd2.start)
        self.assertEqual(12, cd2.size)
        self.assertEqual("dt", cd2.description)

        cd2 = DateTimeColumn("dt", 1, "%d%m%Y%H%M")
        self.assertEqual(1, cd2.start)
        self.assertEqual(12, cd2.size)
        self.assertEqual("dt", cd2.description)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, "name", DateTimeColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", DateTimeColumn, "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", DateTimeColumn, " ", "")
        self.assertRaisesRegex(AssertionError, "start", DateTimeColumn, "name", "")
        self.assertRaisesRegex(AssertionError, "start.*0", DateTimeColumn, "name", 0)
        self.assertRaisesRegex(AssertionError, "_format.*string", DateTimeColumn, "name", 1, 0)
        self.assertRaisesRegex(AssertionError, "_format.*string", DateTimeColumn, "name", 1, None)
        self.assertRaisesRegex(AssertionError, "_format.*não branca", DateTimeColumn, "name", 1, "")
        self.assertRaisesRegex(AssertionError, "_format.*não branca", DateTimeColumn, "name", 1, " ")
        self.assertRaisesRegex(AssertionError, "_format.*válido", DateTimeColumn, "name", 1, '%d%m%Y%H')
        self.assertRaisesRegex(AssertionError, "description.*string", DateTimeColumn, "name", 1, description=1)

    def test_end(self):
        cd = DateTimeColumn("dt", 1)
        self.assertEqual(12, cd.end)

    def test_to_value_invalid(self):
        cd = DateTimeColumn("dt", 1)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 12)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, -1.0)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(ValueError, 'valor.*inválido.*formato', cd.to_value, "310220010000")

    def test_to_value_valid(self):
        cd = DateTimeColumn("dt", 1)
        self.assertEqual(datetime(2001, 2, 28, 0, 0), cd.to_value("280220010000"))

        cd = DateTimeColumn("dt", 1, '%d%m%y%H%M')
        self.assertEqual(datetime(2001, 2, 28, 0, 0), cd.to_value("2802010000"))

    def test_to_str_invalid(self):
        cd = DateTimeColumn("dt", 1)
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, 1)
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, 1.1)
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, False)
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, '123')
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, '1234567890123')
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, date.today())
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, datetime.now().time())

    def test_to_str_valid(self):
        self.assertEqual("280220012359", DateTimeColumn("dt", 1).to_str(datetime(2001, 2, 28, 23, 59)))
        self.assertEqual("2802012359", DateTimeColumn("dt", 1, '%d%m%y%H%M').to_str(datetime(2001, 2, 28, 23, 59)))


class TestDateColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 2', DateColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(DateColumn("type", 1), DateColumn)
        self.assertIsInstance(DateColumn("type", 1, "%d%m%Y"), DateColumn)
        self.assertIsInstance(DateColumn("type", 1, "%d%m%Y", "desc"), DateColumn)

    def test_constructor_set_attr(self):
        cd2 = DateColumn("dt", 1)
        self.assertEqual(1, cd2.start)
        self.assertEqual(8, cd2.size)
        self.assertEqual("dt", cd2.description)

        cd2 = DateColumn("dt", 1, "%d%m%y")
        self.assertEqual(1, cd2.start)
        self.assertEqual(6, cd2.size)
        self.assertEqual("dt", cd2.description)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, "name", DateColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", DateColumn, "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", DateColumn, " ", "")
        self.assertRaisesRegex(AssertionError, "start", DateColumn, "name", "")
        self.assertRaisesRegex(AssertionError, "start.*0", DateColumn, "name", 0)
        self.assertRaisesRegex(AssertionError, "_format.*string", DateColumn, "name", 1, 0)
        self.assertRaisesRegex(AssertionError, "_format.*string", DateColumn, "name", 1, None)
        self.assertRaisesRegex(AssertionError, "_format.*não branca", DateColumn, "name", 1, "")
        self.assertRaisesRegex(AssertionError, "_format.*não branca", DateColumn, "name", 1, " ")
        self.assertRaisesRegex(AssertionError, "_format.*válido", DateColumn, "name", 1, '%d%m%Y%H')
        self.assertRaisesRegex(AssertionError, "description.*string", DateColumn, "name", 1, description=1)

    def test_end(self):
        cd = DateColumn("dt", 1)
        self.assertEqual(8, cd.end)

    def test_to_value_invalid(self):
        cd = DateColumn("dt", 1)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 12)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, -1.0)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(ValueError, 'valor.*inválido.*formato', cd.to_value, "12345678")

    def test_to_value_valid(self):
        cd = DateColumn("dt", 1)
        self.assertEqual(date(2001, 2, 28), cd.to_value("28022001"))

        cd = DateColumn("dt", 1, '%d%m%y')
        self.assertEqual(date(2001, 2, 28), cd.to_value("280201"))

    def test_to_str_invalid(self):
        cd = DateColumn("dt", 1)
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, 1)
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, 1.1)
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, False)
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, '123')
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, '1234567890123')
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, datetime.now().time())

    def test_to_str_valid(self):
        self.assertEqual("28022001", DateColumn("dt", 1).to_str(date(2001, 2, 28)))
        self.assertEqual("28022001", DateColumn("dt", 1).to_str(datetime(2001, 2, 28, 23, 59)))
        self.assertEqual("280201", DateColumn("dt", 1, '%d%m%y').to_str(date(2001, 2, 28)))


class TestTimeColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 2', TimeColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(TimeColumn("type", 1), TimeColumn)
        self.assertIsInstance(TimeColumn("type", 1, "%H:%M"), TimeColumn)

    def test_constructor_set_attr(self):
        cd2 = TimeColumn("dt", 1)
        self.assertEqual(1, cd2.start)
        self.assertEqual(4, cd2.size)
        self.assertEqual("dt", cd2.description)

        cd2 = TimeColumn("dt", 1, "%H:%M")
        self.assertEqual(1, cd2.start)
        self.assertEqual(5, cd2.size)
        self.assertEqual("dt", cd2.description)

    def test_constructor_wrong_args(self):
        self.assertRaisesRegex(AssertionError, "name", TimeColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", TimeColumn, "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", TimeColumn, " ", "")
        self.assertRaisesRegex(AssertionError, "start", TimeColumn, "name", "")
        self.assertRaisesRegex(AssertionError, "start.*0", TimeColumn, "name", 0)
        self.assertRaisesRegex(AssertionError, "_format.*string", TimeColumn, "name", 1, 0)
        self.assertRaisesRegex(AssertionError, "_format.*string", TimeColumn, "name", 1, None)
        self.assertRaisesRegex(AssertionError, "_format.*não branca", TimeColumn, "name", 1, "")
        self.assertRaisesRegex(AssertionError, "_format.*não branca", TimeColumn, "name", 1, " ")
        self.assertRaisesRegex(AssertionError, "_format.*válido", TimeColumn, "name", 1, '%d%m%Y%H')
        self.assertRaisesRegex(AssertionError, "description.*string", TimeColumn, "name", 1, description=1)

    def test_end(self):
        self.assertEqual(4, TimeColumn("dt", 1).end)
        self.assertEqual(5, TimeColumn("dt", 1, '%H:%M').end)

    def test_to_value_invalid(self):
        cd = TimeColumn("dt", 1)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 12)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, -1.0)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(ValueError, 'valor.*inválido.*formato', cd.to_value, "7894")

    def test_to_value_valid(self):
        self.assertEqual(time(23, 59), TimeColumn("time", 1).to_value("2359"))
        self.assertEqual(time(23, 59), TimeColumn("time", 1, '%H:%M').to_value("23:59"))

    def test_to_str_invalid(self):
        cd = TimeColumn("time", 1)
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, 1)
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, 1.1)
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, False)
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, '123')
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, '1234567890123')
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, date.today())

    def test_to_str_valid(self):
        self.assertEqual("2359", TimeColumn("time", 1).to_str(time(23, 59)))
        self.assertEqual("23:59", TimeColumn("time", 1, '%H:%M').to_str(time(23, 59)))
