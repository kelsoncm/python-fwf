---
layout: default
title: Descriptors
parent: API Reference
nav_order: 2
---

# Descriptors
{: .no_toc }

Module: `pyfwf.descriptors`
{: .label }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## RowDescriptor

Base class that wraps a list of columns into a logical row layout. Not used directly — use one of the specialised subclasses below.

**Constructor**

```python
RowDescriptor(columns: List[AbstractColumn])
```

| Argument | Type | Description |
|---|---|---|
| `columns` | `list` | Non-empty list of column instances |

When constructed, each column's `start` position is automatically computed from its position in the list and the `size` of the preceding column.

**Properties**

| Property | Type | Description |
|---|---|---|
| `line_size` | `int` | Total width of a line (= `end` of the last column) |

**Methods**

| Method | Description |
|---|---|
| `get_values(row: str) -> dict` | Parse a raw line string and return a `dict` of field values |
| `validate_positions()` | Assert that columns are contiguous and start at position 1 |

---

## HeaderRowDescriptor

Marks the row layout as a **header** (first line of the file).

```python
from pyfwf.descriptors import HeaderRowDescriptor
from pyfwf.columns import CharColumn

header = HeaderRowDescriptor([
    CharColumn('row_type', 1),
    CharColumn('file_type', 5),
    CharColumn('fill', 157),
])
```

---

## FooterRowDescriptor

Marks the row layout as a **footer** (last line of the file).

```python
from pyfwf.descriptors import FooterRowDescriptor
from pyfwf.columns import CharColumn, PositiveIntegerColumn

footer = FooterRowDescriptor([
    CharColumn('row_type', 1),
    PositiveIntegerColumn('detail_count', 4),
    PositiveIntegerColumn('row_count', 4),
    CharColumn('fill', 154),
])
```

---

## DetailRowDescriptor

Marks the row layout as a **detail** (data lines).

```python
from pyfwf.descriptors import DetailRowDescriptor
from pyfwf.columns import CharColumn, PositiveIntegerColumn

detail = DetailRowDescriptor([
    CharColumn('row_type', 1),
    CharColumn('name', 60),
    PositiveIntegerColumn('age', 9),
])
```

---

## FileDescriptor

Ties header, detail(s), and footer together and validates that all row sizes match.

**Constructor**

```python
FileDescriptor(
    details: List[DetailRowDescriptor],
    header: HeaderRowDescriptor = None,
    footer: FooterRowDescriptor = None,
)
```

| Argument | Type | Required | Description |
|---|---|---|---|
| `details` | `list` | yes | At least one `DetailRowDescriptor` |
| `header` | `HeaderRowDescriptor` | no | Header layout |
| `footer` | `FooterRowDescriptor` | no | Footer layout |

**Validation rules**

- All row descriptors (header, details, footer) must have the same `line_size`.
- `details` must not be empty.

**Attributes**

| Attribute | Type | Description |
|---|---|---|
| `line_size` | `int` | Line width (taken from the first detail descriptor) |
| `header` | `HeaderRowDescriptor \| None` | Header descriptor |
| `footer` | `FooterRowDescriptor \| None` | Footer descriptor |
| `details` | `list` | List of detail descriptors |

**Example**

```python
from pyfwf.descriptors import (
    FileDescriptor,
    HeaderRowDescriptor,
    DetailRowDescriptor,
    FooterRowDescriptor,
)
from pyfwf.columns import CharColumn, PositiveIntegerColumn

fd = FileDescriptor(
    details=[
        DetailRowDescriptor([
            CharColumn('name', 30),
            PositiveIntegerColumn('age', 3),
        ])
    ],
    header=HeaderRowDescriptor([
        CharColumn('file_type', 10),
        CharColumn('fill', 23),
    ]),
    footer=FooterRowDescriptor([
        PositiveIntegerColumn('total', 10),
        CharColumn('fill', 23),
    ]),
)
```
