---
layout: default
title: Renders
parent: API Reference
nav_order: 4
---

# Renders
{: .no_toc }

Module: `pyfwf.renders`
{: .label }

---

## render_as_markdown

Renders a `FileDescriptor` as a Markdown table, one section per row type (HEADER, DETAILS n, FOOTER).

**Signature**

```python
render_as_markdown(file_descriptor: FileDescriptor, out: StringIO) -> None
```

| Argument          | Type             | Description                              |
|-------------------|------------------|------------------------------------------|
| `file_descriptor` | `FileDescriptor` | The layout to render                     |
| `out`             | `StringIO`       | Output buffer to write the Markdown into |

The function writes directly to `out` and returns `None`.

---

## Output format

Each section produces a heading and a Markdown table:

```markdown
# HEADER

|    # | Column    | Size | Start |  End | Type       | Description
| ---- | --------- | ---- | ----- | ---- | ---------- | -----------
|    1 | row_type  |    1 |     1 |    1 | CharColumn | row_type
|    2 | file_type |    5 |     2 |    6 | CharColumn | file_type
|    3 | fill      |  157 |     7 |  163 | CharColumn | fill


# DETAILS 1

|    # | Column            | Size | Start |  End | Type                  | Description
| ---- | ----------------- | ---- | ----- | ---- | --------------------- | -----------
|    1 | row_type          |    1 |     1 |    1 | CharColumn            | row_type
|    2 | name              |   60 |     2 |   61 | CharColumn            | name
...


# FOOTER

|    # | Column       | Size | Start |  End | Type                  | Description
| ---- | ------------ | ---- | ----- | ---- | --------------------- | -----------
|    1 | row_type     |    1 |     1 |    1 | CharColumn            | row_type
|    2 | detail_count |    4 |     2 |    5 | PositiveIntegerColumn | detail_count
```

Column widths in the table are adjusted to fit the longest name/type in each section.

---

## Example

```python
from io import StringIO
from pyfwf.columns import CharColumn, PositiveIntegerColumn
from pyfwf.descriptors import DetailRowDescriptor, FooterRowDescriptor, FileDescriptor
from pyfwf.renders import render_as_markdown

fd = FileDescriptor(
    details=[
        DetailRowDescriptor([
            CharColumn('name', 30),
            PositiveIntegerColumn('age', 3),
        ])
    ],
    footer=FooterRowDescriptor([
        PositiveIntegerColumn('total_records', 10),
        CharColumn('fill', 23),
    ]),
)

buf = StringIO()
render_as_markdown(fd, buf)
print(buf.getvalue())
```

---

## Saving to a file

```python
with open('layout.md', 'w') as f:
    buf = StringIO()
    render_as_markdown(fd, buf)
    f.write(buf.getvalue())
```
