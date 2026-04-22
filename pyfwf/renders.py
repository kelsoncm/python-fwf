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

__author__ = "Kelson da Costa Medeiros <kelsoncm@gmail.com>"


from io import StringIO

from .descriptors import FileDescriptor


def render_as_markdown(file_descriptor: FileDescriptor, out: StringIO):
    def table_header(title, max_colname_size, max_coltype_size):
        out.write(
            (
                "## {title}\n\n"
                "|    # | {name:<%d} | Size | Start |  End | {type:<%d} | Description\n"
                "| ---- | {sep:-<%d} | ---- | ----- | ---- | {sep:-<%d} | -----------\n"
                % (
                    max_colname_size,
                    max_coltype_size,
                    max_colname_size,
                    max_coltype_size,
                )
            ).format(title=title, name="Column", type="Type", sep="-")
        )

    def table_body(cols, max_colname_size, max_coltype_size):
        line = 0
        template = "| {0:>4d} | {1: <%d} | {2:>4d} | {3:>5d} | {4:>4d} | {5:<%d} | {6}\n" % (
            max_colname_size,
            max_coltype_size,
        )
        for col in cols:
            line += 1
            out.write(
                template.format(
                    line,
                    col.name,
                    col.size,
                    col.start,
                    col.end,
                    col.__class__.__name__,
                    col.description,
                )
            )

    def table(title, cols, trailling=True):
        max_colname_size = max([len(col.name) for col in cols])
        max_coltype_size = max([len(col.__class__.__name__) for col in cols])
        table_header(title, max_colname_size, max_coltype_size)
        table_body(cols, max_colname_size, max_coltype_size)
        if trailling:
            out.write("\n")

    out.write("# Description\n\n")

    if file_descriptor.header:
        table("HEADER", file_descriptor.header.columns)

    detail_num = 1
    for detail in file_descriptor.details:
        table("DETAILS %s" % detail_num, detail.columns)
        detail_num += 1

    if file_descriptor.footer:
        table("FOOTER", file_descriptor.footer.columns, False)


def render_as_rst(file_descriptor: FileDescriptor, out: StringIO):
    def table(title, cols, trailling=True):
        # Calcula o tamanho máximo de cada coluna
        headers = ["#", "Column", "Size", "Start", "End", "Type", "Description"]
        rows = [
            [str(idx), col.name, str(col.size), str(col.start), str(col.end), col.__class__.__name__, col.description]
            for idx, col in enumerate(cols, 1)
        ]
        all_rows = [headers] + rows
        col_widths = [max(len(str(row[i])) for row in all_rows) for i in range(len(headers))]

        def sep():
            return " ".join(["=" * w for w in col_widths]) + "\n"

        out.write(f"{title}\n--------------------\n\n")
        out.write(sep())
        out.write(" ".join([h.ljust(col_widths[i]) for i, h in enumerate(headers)]) + "\n")
        out.write(sep())
        for row in rows:
            out.write(" ".join([str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)]) + "\n")
        out.write(sep())
        if trailling:
            out.write("\n")

    out.write("File Description\n===============\n\n")
    if file_descriptor.header:
        table("HEADER", file_descriptor.header.columns)
    detail_num = 1
    for detail in file_descriptor.details:
        table(f"DETAILS {detail_num}", detail.columns)
        detail_num += 1
    if file_descriptor.footer:
        table("FOOTER", file_descriptor.footer.columns, False)


def render_as_html(file_descriptor: FileDescriptor, out: StringIO):
    def table(title, cols, trailling=True):
        out.write(f"<h2>{title}</h2>\n")
        out.write('<table border="1">\n')
        out.write(
            "<tr><th>#</th><th>Column</th><th>Size</th><th>Start</th><th>End</th><th>Type</th><th>Description</th></tr>\n"
        )
        for idx, col in enumerate(cols, 1):
            out.write(
                f"<tr>"
                f"<td>{idx}</td>"
                f"<td>{col.name}</td>"
                f"<td>{col.size}</td>"
                f"<td>{col.start}</td>"
                f"<td>{col.end}</td>"
                f"<td>{col.__class__.__name__}</td>"
                f"<td>{col.description}</td>"
                f"</tr>\n"
            )
        out.write("</table>\n")
        if trailling:
            out.write("<br/>\n")

    out.write("<h1>Description</h1>\n")
    if file_descriptor.header:
        table("HEADER", file_descriptor.header.columns)
    detail_num = 1
    for detail in file_descriptor.details:
        table(f"DETAILS {detail_num}", detail.columns)
        detail_num += 1
    if file_descriptor.footer:
        table("FOOTER", file_descriptor.footer.columns, False)
