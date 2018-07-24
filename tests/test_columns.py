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
        self.assertRaisesRegex(AssertionError, 'inteiro positivo', cd.to_value, "-1")
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


"""
class PositiveDecimalColumn(PositiveIntegerColumn):
    to_str_assertion_types = 'positive decimal'
    to_str_assertion_class = float

    def __init__(self, _name: str, start: int, size: int,  decimals: int=2, description: str=None):
        super(PositiveDecimalColumn, self).__init__(_name, start, size, description)
        self.decimals = decimals

    def to_value(self, slice: str):
        return super(PositiveDecimalColumn, self).to_value(slice) / pow(10, self.decimals)

    def to_str_assertion(self, value):
        return isinstance(value, float) and not isinstance(value, bool) and int(value * pow(10, self.size)) >= 0

    def to_str(self, value: str):
        assert value is None or self.to_str_assertion(value), \
            "O campo '%s' só aceita '%s' or 'None'" % (self.name, self.to_str_assertion_types)

        if value is None:
            return self.to_str_none_pad * self.size
        else:
            _value = int(value * pow(10, self.size))
            return self._validate_to_str_size((self.to_str_pad_template % self.size).format(_value))



class DateTimeColumn(AbstractColumn):
    to_str_assertion_types = 'datetime'
    to_str_assertion_class = datetime
    to_str_none_pad = '0'

    def __init__(self, _name: str, start: int, size: int=12, _format: str='%d%m%Y%H%M', description: str=None):
        super(DateTimeColumn, self).__init__(_name, start, size, description)

        assert isinstance(_format, str), \
            "O argumento 'format' do campo '%s' deve ser uma string" % _name
        assert len(datetime(2001, 12, 31, 13, 59).strftime(_format)) == size, \
            "O campo '%s' tem um 'format' (%s) com tamanho diferente do 'size' (%s)" % (_name, _format, size)

        self.format = _format

    def to_value(self, slice: str):
        _value = super(DateTimeColumn, self).to_value(slice)
        try:
            return datetime.strptime(_value, self.format)
        except ValueError:
            raise ValueError("O valor '%s' do campo '%s' não é um valor no formato '%s'" %
                             (_value, self.name, self.format))

    def to_str(self, value: date):
        return super(DateTimeColumn, self).to_str(value or value.strftim(self.format))


class DateColumn(DateTimeColumn):
    to_str_assertion_types = 'date'
    to_str_assertion_class = date

    def __init__(self, _name: str, start: int, size: int=8, _format: str='%d%m%Y', description: str=None):
        super(CharColumn, self).__init__(_name, start, size, description)

    def to_value(self, slice: str):
        return super(DateColumn, self).to_value(slice).date()


class TimeColumn(DateTimeColumn):
    to_str_assertion_types = 'time'
    to_str_assertion_class = time

    def __init__(self, _name: str, start: int, size: int=8, _format: str='%%H%M', description: str=None):
        super(TimeColumn, self).__init__(_name, start, size, description)

    def to_value(self, slice: str):
        return super(TimeColumn, self).to_value(slice).time()

"""