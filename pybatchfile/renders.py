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


from io import StringIO
import importlib
from typing import List, Dict
from .columns import AbstractColumn
from .descriptors import FileDescriptor


def render_as_markdown(file_descriptor: FileDescriptor, out: StringIO):
    def table_header(title, max_colname_size, max_coltype_size):
        out.write(("# {title}\n\n" 
                   "|    # | {name:<%d} | Size | Start |  End | {type:<%d} | Description\n" 
                   "| ---- | {sep:-<%d} | ---- | ----- | ---- | {sep:-<%d} | -----------\n" %
                   (max_colname_size, max_coltype_size, max_colname_size, max_coltype_size)).
                  format(title=title, name='Column', type='Type', sep='-'))

    def table_body(cols, max_colname_size, max_coltype_size):
        line = 0
        template = "| {0:>4d} | {1: <%d} | {2:>4d} | {3:>5d} | {4:>4d} | {5:<%d} | {6}\n" \
                   % (max_colname_size, max_coltype_size)
        for col in cols:
            line += 1
            out.write(template.format(line, col.name, col.size, col.start, col.end, col.__class__.__name__,
                                      col.description))

    def table(title, cols):
        max_colname_size = max([len(col.name) for col in cols])
        max_coltype_size = max([len(col.__class__.__name__) for col in cols])
        table_header(title, max_colname_size, max_coltype_size)
        table_body(cols, max_colname_size, max_coltype_size)
        out.write("\n\n\n")

    if file_descriptor.header:
        table("HEADER", file_descriptor.header.columns)

    detail_num = 1
    for detail in file_descriptor.details:
        table("DETAILS %s" % detail_num, detail.columns)
        detail_num += 1

    if file_descriptor.footer:
        table("FOOTER", file_descriptor.header.columns)
