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


from typing import Iterator
from .descriptors import FileDescriptor
import collections
import csv


class Reader:

    def __init__(self, _iterable: Iterator[str], file_descriptor: FileDescriptor, lines_count: int=None):
        assert isinstance(_iterable, collections.Iterable), \
            'O argumento _iterable tem que ser um Iterator'
        assert isinstance(file_descriptor, FileDescriptor), \
            'O argumento file_descriptor tem que ser um FileDescriptor'
        assert (not isinstance(lines_count, bool) and isinstance(lines_count, int)) or lines_count is None, \
            'O argumento lines_count tem que ser um int ou um None'

        import itertools
        it1, it2 = itertools.tee(_iterable, 2)
        self.iterable = it1
        self.to_validate_line_size = it2
        self.file_descriptor = file_descriptor
        self.lines_count = lines_count
        self.line_num = 0

    @staticmethod
    def _get_line_content(r):
        if r.endswith("\r\n"):
            return r[:-2]
        elif r.endswith("\r") or r.endswith("\n"):
            return r[:-1]
        else:
            return r

    def validate_file_structure(self):
        line = 0
        file_line_size = self.file_descriptor._line_size
        for row in self.to_validate_line_size:
            line_size = len(self._get_line_content(row))
            assert line_size == self.file_descriptor._line_size, \
                'Wrong line size on %d, instead of %d we have %s: [%s]' % (line, file_line_size, line_size, row)
            line += 1
        return line

    def __iter__(self):
        return self

    def __next__(self):
        row = next(self.iterable)
        self.line_num += 1
        print(self.line_num, self.lines_count)
        if self.file_descriptor.header and self.line_num == 1:
            return self.file_descriptor.header.get_values(self._get_line_content(row))
        elif self.file_descriptor.footer and self.lines_count and self.lines_count == self.line_num:
            return self.file_descriptor.footer.get_values(self._get_line_content(row))
        else:
            return self.file_descriptor.details[0].get_values(self._get_line_content(row))
