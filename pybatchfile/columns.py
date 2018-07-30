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


import re
from datetime import datetime, date, time
from .hydrating import Hydrator


class AbstractColumn(Hydrator):
    to_str_assertion_types = None
    to_str_assertion_class = None
    to_str_none_pad = None
    to_str_pad_template = None
    hydrating_args = ['name', 'size', 'description']

    def __init__(self, _name: str, size: int, description: str=None):
        super(AbstractColumn, self).__init__()
        assert isinstance(_name, str), 'O campo name deve ser uma string'
        assert _name and _name.rstrip(), 'O campo column_name deve ser uma string válida e não branca'
        assert isinstance(size, int), 'O campo size deve ser um inteiro'
        assert size > 0, 'O campo size deve ser maior que 0'
        if description is None:
            description = _name
        else:
            assert isinstance(description, str), 'O campo description deve ser uma string'

        self.name = _name
        self.size = size
        self.description = description
        self.start = None

    @property
    def end(self):
        assert isinstance(self.start, int), 'O campo start deve ser um inteiro'
        assert self.start > 0, 'O campo start deve ser maior que 0'
        return self.start + self.size - 1

    def to_value(self, slice):
        assert isinstance(slice, str), 'Informe uma string para converter corretamente'
        assert len(slice) == self.size, "A string deve ter exatamente o tamanho do campo '%s' (%s)" % \
                                        (self.name, self.size)
        return slice

    def _validate_to_str_size(self, value):
        assert len(value) == self.size, "O valor a ser serializado para o campo '%s' não pode ser diferente de %d " \
                                         % (self.name, self.size)
        return value

    def to_str_assertion(self, value):
        return isinstance(value, self.to_str_assertion_class)

    def to_str(self, value: str):
        assert value is None or self.to_str_assertion(value), \
            "O campo '%s' só aceita '%s' or 'None'" % (self.name, self.to_str_assertion_types)

        if value is None:
            return self.to_str_none_pad * self.size
        else:
            return self._validate_to_str_size((self.to_str_pad_template % self.size).format(value))


class CharColumn(AbstractColumn):

    to_str_assertion_types = 'str'
    to_str_assertion_class = str
    to_str_none_pad = ' '
    to_str_pad_template = '{0: <%d}'

    def to_value(self, slice: str):
        return super(CharColumn, self).to_value(slice).strip()


class RightCharColumn(CharColumn):
    to_str_pad_template = "{0: >%d}"


class PositiveIntegerColumn(AbstractColumn):
    to_str_assertion_types = 'positive int'
    to_str_assertion_class = int
    to_str_none_pad = '0'
    to_str_pad_template = "{0:0%dd}"

    def to_str_assertion(self, value):
        return isinstance(value, int) and not isinstance(value, bool) and value >= 0

    def to_value(self, slice: str):
        _value = int(super(PositiveIntegerColumn, self).to_value(slice))
        assert _value >= 0, \
            "Informe uma string para converter corretamente, '%s' não é um '%s'" % (slice, self.to_str_assertion_types)
        return _value


class PositiveDecimalColumn(PositiveIntegerColumn):
    to_str_assertion_types = 'positive decimal'
    to_str_assertion_class = float
    hydrating_args = ['name', 'size', 'decimals', 'description']

    def __init__(self, _name: str, size: int,  decimals: int=2, description: str=None):
        super(PositiveDecimalColumn, self).__init__(_name, size, description)
        assert isinstance(decimals, int), 'Os decimais devem ser um inteiro'
        assert decimals > 0, 'Os decimais devem ser maior que 0'
        assert size > decimals, 'Os decimais devem ser menores que o size'
        self.decimals = decimals

    def to_value(self, slice: str):
        return super(PositiveDecimalColumn, self).to_value(slice) / pow(10, self.decimals)

    def to_str_assertion(self, value):
        return isinstance(value, float) and not isinstance(value, bool) and value >= 0.0

    def to_str(self, value: str):
        assert value is None or self.to_str_assertion(value), \
            "O campo '%s' só aceita '%s' or 'None'" % (self.name, self.to_str_assertion_types)

        if value is None:
            return self.to_str_none_pad * self.size
        else:
            _value = int(value * pow(10, self.decimals))
            return self._validate_to_str_size((self.to_str_pad_template % self.size).format(_value))


class DateTimeColumn(AbstractColumn):
    to_str_assertion_types = 'datetime'
    to_str_assertion_class = datetime
    to_str_none_pad = '0'
    format_num_elements = 5
    hydrating_args = ['name', 'format', 'description']

    def __init__(self, _name: str, _format: str='%d%m%Y%H%M', description: str=None):
        assert isinstance(_name, str), \
            'O campo name deve ser uma string'
        assert _name and _name.strip(), \
            'O campo column_name deve ser uma string válida e não branca'
        assert isinstance(_format, str), \
            "O argumento '_format' do campo '%s' deve ser uma string" % _name
        assert _format and _format.strip(), \
            "O argumento '_format' do campo '%s' deve ser uma string válida e não branca" % _name
        assert len([x for x in re.finditer(re.compile('(%[a-z,A-Z])'), _format)]) == self.format_num_elements, \
            "O argumento '_format' (%s) do campo '%s' deve ter um formato de data/hora válido" % (_format, _name)

        _size = len(datetime(2001, 12, 31, 13, 59).strftime(_format))

        self.to_str_pad_templating = ''
        super(DateTimeColumn, self).__init__(_name, _size, description)

        self.format = _format

    def to_value(self, slice: str):
        _value = super(DateTimeColumn, self).to_value(slice)
        try:
            if _value == self.to_str_none_pad * self.size:
                return None
            else:
                return datetime.strptime(_value, self.format)
        except ValueError:
            raise ValueError("O valor '%s' do campo '%s' é inválido para o formato '%s'" %
                             (_value, self.name, self.format))

    def to_str(self, value: datetime):
        assert value is None or self.to_str_assertion(value), \
            "O campo '%s' só aceita '%s' or 'None'" % (self.name, self.to_str_assertion_types)

        if value is None:
            return self.to_str_none_pad * self.size
        else:
            return self._validate_to_str_size(value.strftime(self.format))


class DateColumn(DateTimeColumn):
    to_str_assertion_types = 'date'
    to_str_assertion_class = date
    format_num_elements = 3

    def __init__(self, _name: str, _format: str='%d%m%Y', description: str=None):
        super(DateColumn, self).__init__(_name, _format, description)

    def to_value(self, slice: str):
        result = super(DateColumn, self).to_value(slice)
        return result.date() if result is not None else None


class TimeColumn(DateTimeColumn):
    to_str_assertion_types = 'time'
    to_str_assertion_class = time
    format_num_elements = 2

    def __init__(self, _name: str, _format: str='%H%M', description: str=None):
        super(TimeColumn, self).__init__(_name, _format, description)

    def to_value(self, slice: str):
        result = super(TimeColumn, self).to_value(slice)
        return result.time() if result is not None else None
