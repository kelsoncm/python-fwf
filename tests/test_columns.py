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
from fwf.columns import CharColumn, RightCharColumn, PositiveIntegerColumn, PositiveDecimalColumn, \
    DateTimeColumn, DateColumn, TimeColumn
from datetime import datetime, date, time


class TestCharColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 2', CharColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(CharColumn("type", 1, "desc"), CharColumn)

    def test_constructor_set_attr(self):
        cd = CharColumn("type", 2, "desc")
        self.assertEqual("type", cd.name)
        self.assertEqual(2, cd.size)
        self.assertEqual("desc", cd.description)

        cd2 = CharColumn("name", 1)
        self.assertEqual(1, cd2.size)
        self.assertEqual("name", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaisesRegex(AssertionError, "name", CharColumn, None, "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", CharColumn, "", "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", CharColumn, " ", "", "")

    def test_constructor_wrong_size_arg(self):
        self.assertRaisesRegex(AssertionError, "size", CharColumn, "name", "")
        self.assertRaisesRegex(AssertionError, "size.*0", CharColumn, "name", 0)

    def test_constructor_wrong_description_arg(self):
        self.assertRaisesRegex(AssertionError, "description.*string", CharColumn, "name", 1, 1)
        self.assertRaisesRegex(AssertionError, "description.*string", CharColumn, "name", 1, False)

    def test_end(self):
        cd = CharColumn("name", 2, "desc")
        cd.start = 1
        self.assertEqual(2, cd.end)

    def test_to_value_invalid(self):
        cd = CharColumn("name", 2, "desc")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 1)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "333")

    def test_to_value_valid(self):
        cd = CharColumn("name", 2, "desc")
        self.assertEqual("22", cd.to_value("22"))
        self.assertEqual("2", cd.to_value("2 "))
        self.assertEqual("2", cd.to_value(" 2"))

    def test_to_str_invalid(self):
        cd = CharColumn("name", 4, "desc")
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, 1)
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, 12345)
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, True)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, "12345")
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, "123  ")

    def test_to_str_valid(self):
        cd = CharColumn("name", 4, "desc")
        self.assertEqual("asdf", cd.to_str("asdf"))
        self.assertEqual("a   ", cd.to_str("a "))
        self.assertEqual("    ", cd.to_str(""))
        self.assertEqual("    ", cd.to_str(" "))

    def test_dehydrate(self):
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.CharColumn', 'args': ['col_name', 20, 'col_desc']},
                             CharColumn('col_name', 20, 'col_desc').dehydrate())
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.CharColumn', 'args': ['col_name', 20, 'col_name']},
                             CharColumn('col_name', 20).dehydrate())


class TestRightCharColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 2', RightCharColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(RightCharColumn("type", 2, "desc"), RightCharColumn)

    def test_constructor_set_attr(self):
        cd = RightCharColumn("type", 2, "desc")
        self.assertEqual("type", cd.name)
        self.assertEqual(2, cd.size)
        self.assertEqual("desc", cd.description)

        cd2 = RightCharColumn("name", 1)
        self.assertEqual(1, cd2.size)
        self.assertEqual("name", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaisesRegex(AssertionError, "name", RightCharColumn, None, "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", RightCharColumn, "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", RightCharColumn, " ", "")

    def test_constructor_wrong_size_arg(self):
        self.assertRaisesRegex(AssertionError, "size", RightCharColumn, "name", "")
        self.assertRaisesRegex(AssertionError, "size.*0", RightCharColumn, "name", 0)

    def test_constructor_wrong_description_arg(self):
        self.assertRaisesRegex(AssertionError, "description.*string", RightCharColumn, "name", 1, 1)
        self.assertRaisesRegex(AssertionError, "description.*string", RightCharColumn, "name", 1, False)

    def test_end(self):
        cd = RightCharColumn("name", 2, "desc")
        cd.start = 1
        self.assertEqual(2, cd.end)

    def test_to_value_invalid(self):
        cd = RightCharColumn("name", 2, "desc")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 1)
        self.assertRaisesRegex(AssertionError, "string", cd.to_value, 12345)
        self.assertRaisesRegex(AssertionError, "string", cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "333")

    def test_to_value_valid(self):
        cd = RightCharColumn("name", 2, "desc")
        self.assertEqual("22", cd.to_value("22"))
        self.assertEqual("2", cd.to_value("2 "))
        self.assertEqual("2", cd.to_value(" 2"))

    def test_to_str_invalid(self):
        cd = RightCharColumn("name", 4, "desc")
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, 1)
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, 12345)
        self.assertRaisesRegex(AssertionError, "'str' or 'None'", cd.to_str, True)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, "12345")
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, "123  ")

    def test_to_str_valid(self):
        cd = RightCharColumn("name", 4, "desc")
        self.assertEqual("asdf", cd.to_str("asdf"))
        self.assertEqual("  a ", cd.to_str("a "))
        self.assertEqual("   a", cd.to_str("a"))
        self.assertEqual("    ", cd.to_str(""))
        self.assertEqual("    ", cd.to_str(" "))
        self.assertEqual("    ", cd.to_str(None))

    def test_dehydrate(self):
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.RightCharColumn', 'args': ['col_name', 20, 'col_desc']},
                             RightCharColumn('col_name', 20, 'col_desc').dehydrate())
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.RightCharColumn', 'args': ['col_name', 20, 'col_name']},
                             RightCharColumn('col_name', 20).dehydrate())


class TestPositiveIntegerColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 2', PositiveIntegerColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(PositiveIntegerColumn("type", 1, "desc"), PositiveIntegerColumn)

    def test_constructor_set_attr(self):
        cd = PositiveIntegerColumn("type", 2, "the type")
        self.assertEqual("type", cd.name)
        self.assertEqual(2, cd.size)
        self.assertEqual("the type", cd.description)

        cd2 = PositiveIntegerColumn("name", 1)
        self.assertEqual(1, cd2.size)
        self.assertEqual("name", cd2.name)
        self.assertEqual(cd2.name, cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaisesRegex(AssertionError, "name", PositiveIntegerColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", PositiveIntegerColumn, "", "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", PositiveIntegerColumn, " ", "", "")

    def test_constructor_wrong_size_arg(self):
        self.assertRaisesRegex(AssertionError, "size", PositiveIntegerColumn, "name", "")
        self.assertRaisesRegex(AssertionError, "size.*0", PositiveIntegerColumn, "name", 0)

    def test_constructor_wrong_description_arg(self):
        self.assertRaisesRegex(AssertionError, "description.*string", PositiveIntegerColumn, "name", 1, 1)
        self.assertRaisesRegex(AssertionError, "description.*string", PositiveIntegerColumn, "name", 1, False)

    def test_end(self):
        cd = PositiveIntegerColumn("name", 2, "desc")
        cd.start = 1
        self.assertEqual(2, cd.end)

    def test_to_value_invalid(self):
        cd = PositiveIntegerColumn("name", 2, "desc")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 12)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(AssertionError, 'positive int', cd.to_value, "-1")
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "333")
        self.assertRaisesRegex(ValueError, 'invalid literal for int', cd.to_value, "A1")

    def test_to_value_valid(self):
        cd = PositiveIntegerColumn("name", 2, "desc")
        self.assertEqual(22, cd.to_value("22"))
        self.assertEqual(2, cd.to_value("2 "))
        self.assertEqual(2, cd.to_value(" 2"))

    def test_to_str_invalid(self):
        cd = PositiveIntegerColumn("name", 4, "desc")
        self.assertRaisesRegex(AssertionError, "'positive int' or 'None'", cd.to_str, '1')
        self.assertRaisesRegex(AssertionError, "'positive int' or 'None'", cd.to_str, '-123')
        self.assertRaisesRegex(AssertionError, "'positive int' or 'None'", cd.to_str, '12345')
        self.assertRaisesRegex(AssertionError, "'positive int' or 'None'", cd.to_str, True)
        self.assertRaisesRegex(AssertionError, "'positive int' or 'None'", cd.to_str, -1)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, 12345)

    def test_to_str_valid(self):
        cd = PositiveIntegerColumn("name", 4, "year")
        self.assertEqual("0001", cd.to_str(1))
        self.assertEqual("1234", cd.to_str(1234))
        self.assertEqual("0000", cd.to_str(0))
        self.assertEqual("0000", cd.to_str(None))

    def test_dehydrate(self):
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.PositiveIntegerColumn', 'args': ['col_name', 20, 'col_desc']},
                             PositiveIntegerColumn('col_name', 20, 'col_desc').dehydrate())
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.PositiveIntegerColumn', 'args': ['col_name', 20, 'col_name']},
                             PositiveIntegerColumn('col_name', 20).dehydrate())


class TestPositiveDecimalColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 2', PositiveDecimalColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(PositiveDecimalColumn("type", 3), PositiveDecimalColumn)
        self.assertIsInstance(PositiveDecimalColumn("type", 3, 2), PositiveDecimalColumn)
        self.assertIsInstance(PositiveDecimalColumn("type", 3, 2, "desc"), PositiveDecimalColumn)

    def test_constructor_set_attr(self):
        cd2 = PositiveDecimalColumn("value", 4)
        self.assertEqual(4, cd2.size)
        self.assertEqual("value", cd2.description)

        cd2 = PositiveDecimalColumn("value", 4, 2)
        self.assertEqual(4, cd2.size)
        self.assertEqual("value", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaisesRegex(AssertionError, "name", PositiveDecimalColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", PositiveDecimalColumn, "", "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", PositiveDecimalColumn, " ", "", "")

    def test_constructor_wrong_size_arg(self):
        self.assertRaisesRegex(AssertionError, "size", PositiveDecimalColumn, "name",  "")
        self.assertRaisesRegex(AssertionError, "size.*0", PositiveDecimalColumn, "name", 0)

    def test_constructor_wrong_decimals_args(self):
        self.assertRaisesRegex(AssertionError, "decimais.*inteiro", PositiveDecimalColumn, "name", 1, "1")
        self.assertRaisesRegex(AssertionError, "decimais.*maior que 0", PositiveDecimalColumn, "value", 1, 0)
        self.assertRaisesRegex(AssertionError, "decimais.*size", PositiveDecimalColumn, "value", 1)
        self.assertRaisesRegex(AssertionError, "decimais.*size", PositiveDecimalColumn, "value", 1, 2)
        self.assertRaisesRegex(AssertionError, "decimais.*size", PositiveDecimalColumn, "value", 1, 1)
        self.assertRaisesRegex(AssertionError, "decimais.*maior que 0", PositiveDecimalColumn, "value", 1, 0)

    def test_constructor_wrong_description_arg(self):
        self.assertRaisesRegex(AssertionError, "description.*string", PositiveDecimalColumn, "name", 3, 1, -1)
        self.assertRaisesRegex(AssertionError, "description.*string", PositiveDecimalColumn, "name", 3, 1, False)

    def test_end(self):
        cd = PositiveDecimalColumn("name", 2, 1, "desc")
        cd.start = 1
        self.assertEqual(2, cd.end)

    def test_to_value_invalid(self):
        cd = PositiveDecimalColumn("name", 2, 1, "desc")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 12)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, -1.0)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(AssertionError, 'positive decimal', cd.to_value, "-1")
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "333")
        self.assertRaisesRegex(ValueError, 'invalid literal for int', cd.to_value, "A1")

    def test_to_value_valid(self):
        cd = PositiveDecimalColumn("value", 3, 2)
        self.assertEqual(1.23, cd.to_value("123"))
        self.assertEqual(0.01, cd.to_value("1  "))
        self.assertEqual(0.02, cd.to_value(" 2 "))
        self.assertEqual(0.03, cd.to_value("  3"))

    def test_to_str_invalid(self):
        cd = PositiveDecimalColumn("value", 4, 2)
        self.assertRaisesRegex(AssertionError, "'positive decimal' or 'None'", cd.to_str, '1')
        self.assertRaisesRegex(AssertionError, "'positive decimal' or 'None'", cd.to_str, '-123')
        self.assertRaisesRegex(AssertionError, "'positive decimal' or 'None'", cd.to_str, '12345')
        self.assertRaisesRegex(AssertionError, "'positive decimal' or 'None'", cd.to_str, True)
        self.assertRaisesRegex(AssertionError, "'positive decimal' or 'None'", cd.to_str, -1)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, 123.45)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, 123.0)
        self.assertRaisesRegex(AssertionError, 'diferente de 4', cd.to_str, 1234.0)

    def test_to_str_valid(self):
        cd = PositiveDecimalColumn("value", 4)
        self.assertEqual("0100", cd.to_str(1.0))
        self.assertEqual("1234", cd.to_str(12.34))
        self.assertEqual("0000", cd.to_str(0.0))
        self.assertEqual("0012", cd.to_str(0.12))
        self.assertEqual("0010", cd.to_str(0.1))
        self.assertEqual("0000", cd.to_str(None))

    def test_dehydrate(self):
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.PositiveDecimalColumn', 'args': ['col_name', 20, 2, 'col_name']},
                             PositiveDecimalColumn('col_name', 20).dehydrate())
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.PositiveDecimalColumn', 'args': ['col_name', 20, 4, 'col_name']},
                             PositiveDecimalColumn('col_name', 20, 4).dehydrate())


class TestDateTimeColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', DateTimeColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(DateTimeColumn("type"), DateTimeColumn)
        self.assertIsInstance(DateTimeColumn("type", "%d%m%Y%H%M"), DateTimeColumn)
        self.assertIsInstance(DateTimeColumn("type", "%d%m%Y%H%M", "desc"), DateTimeColumn)

    def test_constructor_set_attr(self):
        cd2 = DateTimeColumn("dt")
        self.assertEqual(12, cd2.size)
        self.assertEqual("dt", cd2.description)

        cd2 = DateTimeColumn("dt", "%d%m%Y%H%M")
        self.assertEqual(12, cd2.size)
        self.assertEqual("dt", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaisesRegex(AssertionError, "name", DateTimeColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", DateTimeColumn, "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", DateTimeColumn, " ", "")

    def test_constructor_wrong_format_args(self):
        self.assertRaisesRegex(AssertionError, "_format.*string", DateTimeColumn, "dt", 0)
        self.assertRaisesRegex(AssertionError, "_format.*string", DateTimeColumn, "dt", None)
        self.assertRaisesRegex(AssertionError, "_format.*não branca", DateTimeColumn, "dt", "")
        self.assertRaisesRegex(AssertionError, "_format.*não branca", DateTimeColumn, "dt", " ")
        self.assertRaisesRegex(AssertionError, "_format.*válido", DateTimeColumn, "dt", '%d%m%Y%H')

    def test_constructor_wrong_description_arg(self):
        self.assertRaisesRegex(AssertionError, "description.*string", DateTimeColumn, "dt", description=1)
        self.assertRaisesRegex(AssertionError, "description.*string", DateTimeColumn, "dt", description=False)

    def test_end(self):
        cd = DateTimeColumn("dt")
        cd.start = 1
        self.assertEqual(12, cd.end)

    def test_to_value_invalid(self):
        cd = DateTimeColumn("dt")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 12)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, -1.0)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(ValueError, 'valor.*inválido.*formato', cd.to_value, "310220010000")

    def test_to_value_valid(self):
        cd = DateTimeColumn("dt")
        self.assertEqual(datetime(2001, 2, 28, 0, 0), cd.to_value("280220010000"))

        cd = DateTimeColumn("dt", '%d%m%y%H%M')
        self.assertEqual(datetime(2001, 2, 28, 0, 0), cd.to_value("2802010000"))

    def test_to_str_invalid(self):
        cd = DateTimeColumn("dt")
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, 1)
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, 1.1)
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, False)
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, '123')
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, '1234567890123')
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, date.today())
        self.assertRaisesRegex(AssertionError, "'datetime' or 'None'", cd.to_str, datetime.now().time())

    def test_to_str_valid(self):
        self.assertEqual("280220012359", DateTimeColumn("dt").to_str(datetime(2001, 2, 28, 23, 59)))
        self.assertEqual("000000000000", DateTimeColumn("dt").to_str(None))
        self.assertEqual("2802012359", DateTimeColumn("dt", '%d%m%y%H%M').to_str(datetime(2001, 2, 28, 23, 59)))

    def test_dehydrate(self):
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.DateTimeColumn', 'args': ['col_name', '%d%m%Y%H%M', 'col_name']},
                             DateTimeColumn('col_name').dehydrate())
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.DateTimeColumn', 'args': ['col_name', '%d%m%y%H%M', 'col_name']},
                             DateTimeColumn('col_name', '%d%m%y%H%M').dehydrate())
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.DateTimeColumn', 'args': ['col_name', '%d%m%y%H%M', 'col_desc']},
                             DateTimeColumn('col_name', '%d%m%y%H%M', 'col_desc').dehydrate())


class TestDateColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', DateColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(DateColumn("type"), DateColumn)
        self.assertIsInstance(DateColumn("type", "%d%m%Y"), DateColumn)
        self.assertIsInstance(DateColumn("type", "%d%m%Y", "desc"), DateColumn)

    def test_constructor_set_attr(self):
        cd2 = DateColumn("dt")
        self.assertEqual(8, cd2.size)
        self.assertEqual("dt", cd2.description)

        cd2 = DateColumn("dt", "%d%m%y")
        self.assertEqual(6, cd2.size)
        self.assertEqual("dt", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaisesRegex(AssertionError, "name", DateColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", DateColumn, "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", DateColumn, " ", "")

    def test_constructor_wrong_format_args(self):
        self.assertRaisesRegex(AssertionError, "_format.*string", DateColumn, "name", 0)
        self.assertRaisesRegex(AssertionError, "_format.*string", DateColumn, "name", None)
        self.assertRaisesRegex(AssertionError, "_format.*não branca", DateColumn, "name", "")
        self.assertRaisesRegex(AssertionError, "_format.*não branca", DateColumn, "name", " ")
        self.assertRaisesRegex(AssertionError, "_format.*válido", DateColumn, "name", '%d%m%Y%H')

    def test_constructor_wrong_description_arg(self):
        self.assertRaisesRegex(AssertionError, "description.*string", DateColumn, "dt", description=1)
        self.assertRaisesRegex(AssertionError, "description.*string", DateColumn, "dt", description=False)

    def test_end(self):
        cd = DateColumn("dt")
        cd.start = 1
        self.assertEqual(8, cd.end)

    def test_to_value_invalid(self):
        cd = DateColumn("dt")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 12)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, -1.0)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(ValueError, 'valor.*inválido.*formato', cd.to_value, "12345678")

    def test_to_value_valid(self):
        self.assertEqual(date(2001, 2, 28), DateColumn("dt").to_value("28022001"))
        self.assertEqual(date(2001, 2, 28), DateColumn("dt", '%d%m%y').to_value("280201"))

    def test_to_str_invalid(self):
        cd = DateColumn("dt")
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, 1)
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, 1.1)
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, False)
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, '123')
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, '1234567890123')
        self.assertRaisesRegex(AssertionError, "'date' or 'None'", cd.to_str, datetime.now().time())

    def test_to_str_valid(self):
        self.assertEqual("28022001", DateColumn("dt").to_str(date(2001, 2, 28)))
        self.assertEqual("28022001", DateColumn("dt").to_str(datetime(2001, 2, 28, 23, 59)))
        self.assertEqual("280201", DateColumn("dt", '%d%m%y').to_str(date(2001, 2, 28)))

    def test_dehydrate(self):
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.DateColumn', 'args': ['col_name', '%d%m%Y', 'col_name']},
                             DateColumn('col_name').dehydrate())
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.DateColumn', 'args': ['col_name', '%d%m%y', 'col_name']},
                             DateColumn('col_name', '%d%m%y').dehydrate())
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.DateColumn', 'args': ['col_name', '%d%m%y', 'col_desc']},
                             DateColumn('col_name', '%d%m%y', 'col_desc').dehydrate())


class TestTimeColumn(TestCase):

    def test_constructor_empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', TimeColumn)

    def test_constructor_all_right(self):
        self.assertIsInstance(TimeColumn("type"), TimeColumn)
        self.assertIsInstance(TimeColumn("type", "%H:%M"), TimeColumn)

    def test_constructor_set_attr(self):
        cd2 = TimeColumn("time")
        self.assertEqual(4, cd2.size)
        self.assertEqual("time", cd2.description)

        cd2 = TimeColumn("time", "%H:%M")
        self.assertEqual(5, cd2.size)
        self.assertEqual("time", cd2.description)

    def test_constructor_wrong_name_arg(self):
        self.assertRaisesRegex(AssertionError, "name", TimeColumn, None, "a", "a")
        self.assertRaisesRegex(AssertionError, "name.*branca", TimeColumn, "", "")
        self.assertRaisesRegex(AssertionError, "name.*branca", TimeColumn, " ", "")

    def test_constructor_wrong_format_args(self):
        self.assertRaisesRegex(AssertionError, "_format.*string", TimeColumn, "time", 0)
        self.assertRaisesRegex(AssertionError, "_format.*string", TimeColumn, "time", None)
        self.assertRaisesRegex(AssertionError, "_format.*não branca", TimeColumn, "time", "")
        self.assertRaisesRegex(AssertionError, "_format.*não branca", TimeColumn, "time", " ")
        self.assertRaisesRegex(AssertionError, "_format.*válido", TimeColumn, "time", '%d%m%Y%H')

    def test_constructor_wrong_description_arg(self):
        self.assertRaisesRegex(AssertionError, "description.*string", TimeColumn, "time", description=1)
        self.assertRaisesRegex(AssertionError, "description.*string", TimeColumn, "time", description=False)

    def test_end(self):
        cd = TimeColumn("time")
        cd.start = 1
        self.assertEqual(4, cd.end)

        cd = TimeColumn("time", '%H:%M')
        cd.start = 1
        self.assertEqual(5, cd.end)

    def test_to_value_invalid(self):
        cd = TimeColumn("time")
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, 12)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, -1.0)
        self.assertRaisesRegex(AssertionError, 'string.*corretamente', cd.to_value, True)
        self.assertRaisesRegex(AssertionError, 'tamanho do campo', cd.to_value, "1")
        self.assertRaisesRegex(ValueError, 'valor.*inválido.*formato', cd.to_value, "7894")

    def test_to_value_valid(self):
        self.assertEqual(time(23, 59), TimeColumn("time").to_value("2359"))
        self.assertEqual(time(23, 59), TimeColumn("time", '%H:%M').to_value("23:59"))

    def test_to_str_invalid(self):
        cd = TimeColumn("time")
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, 1)
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, 1.1)
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, False)
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, '123')
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, '1234567890123')
        self.assertRaisesRegex(AssertionError, "'time' or 'None'", cd.to_str, date.today())

    def test_to_str_valid(self):
        self.assertEqual("2359", TimeColumn("time").to_str(time(23, 59)))
        self.assertEqual("23:59", TimeColumn("time", '%H:%M').to_str(time(23, 59)))

    def test_dehydrate(self):
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.TimeColumn', 'args': ['col_name', '%H%M', 'col_name']},
                             TimeColumn('col_name').dehydrate())
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.TimeColumn', 'args': ['col_name', '%H%M', 'col_name']},
                             TimeColumn('col_name', '%H%M').dehydrate())
        self.assertDictEqual({'_hydrate_as': 'fwf.columns.TimeColumn', 'args': ['col_name', '%H%M', 'col_desc']},
                             TimeColumn('col_name', '%H%M', 'col_desc').dehydrate())
