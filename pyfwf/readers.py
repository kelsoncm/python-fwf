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


from typing import Iterable, List
from io import StringIO, TextIOWrapper
from .descriptors import FileDescriptor
import collections


__all__ = ['Reader']


class Reader:

    def __init__(self, _iterable: Iterable[str], file_descriptor: FileDescriptor, newline: str="\n\r"):
        assert isinstance(_iterable, collections.Iterable), \
            'O argumento _iterable tem que ser um Iterator'
        assert isinstance(file_descriptor, FileDescriptor), \
            'O argumento file_descriptor tem que ser um FileDescriptor'
        assert isinstance(newline, str) and newline in ["\n", "\r", "\n\r"], \
            'O argumento newline tem que ser uma str e conter "\\n", "\\r" ou "\\n\\r"'

        self.iterable = _iterable
        self.file_descriptor = file_descriptor
        self.line_num = 0
        self.newline = newline
        self.lines_count = 0

        if isinstance(self.iterable, StringIO):
            self.filesize = len(self.iterable.getvalue())
        elif isinstance(self.iterable, TextIOWrapper):
            self.filesize = len(self.iterable.read())
        elif isinstance(self.iterable, str):
            self.filesize = len(self.iterable)
            self.iterable = StringIO(self.iterable)
        elif isinstance(self.iterable, List):
            self.iterable = iter(_iterable)
            self.lines_count = len(_iterable)
            self.filesize = sum([len(r) for r in _iterable])
        else:
            raise TypeError('Unsupported Iterable')

        assert float(self.filesize) % float(self.file_descriptor.line_size + len(self.newline)) == 0, \
            "Algumas linha não tem o tamanho correto (%d) ou não tem a quebra de linha adequada (%s), " \
            "total de bytes %d e total de linhas %f" % \
            (self.file_descriptor.line_size, self.newline.replace("\n", "\\n").replace("\r", "\\r"),
             self.filesize, float(self.filesize) / float(self.file_descriptor.line_size + len(self.newline)))
        self.lines_count = self.filesize / (self.file_descriptor.line_size + len(self.newline))

    def __iter__(self):
        return self

    def __next__(self):
        row = next(self.iterable)
        self.line_num += 1
        lc = row[:-len(self.newline)]
        if self.file_descriptor.header and self.line_num == 1:
            return self.file_descriptor.header.get_values(lc)
        elif self.file_descriptor.footer and self.lines_count and self.lines_count == self.line_num:
            return self.file_descriptor.footer.get_values(lc)
        else:
            return self.file_descriptor.details[0].get_values(lc)
