---
layout: default
title: Reader
parent: API Reference
nav_order: 3
---

# Reader
{: .no_toc }

Module: `pyfwf.readers`
{: .label }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Reader

An iterator that reads a fixed-width file line by line and returns each row as a typed `dict`.

**Constructor**

```python
Reader(
    _iterable: Iterable[str],
    file_descriptor: FileDescriptor,
    newline: str = "\n\r",
)
```

| Argument | Type | Default | Description |
|---|---|---|---|
| `_iterable` | see below | — | Source data |
| `file_descriptor` | `FileDescriptor` | — | Layout definition |
| `newline` | `str` | `"\n\r"` | Line terminator: `"\n"`, `"\r"`, or `"\n\r"` |

**Supported input types**

| Type | Notes |
|---|---|
| `TextIOWrapper` | Standard file opened with `open()` |
| `StringIO` | In-memory text stream |
| `str` | Raw string with embedded newlines |
| `list` | List of raw line strings (each including the newline) |

Any other type raises `TypeError: Unsupported Iterable`.

**Validation**

On construction, `Reader` asserts that:

```
filesize % (line_size + len(newline)) == 0
```

If any line has the wrong length, a descriptive `AssertionError` is raised before iteration begins.

---

## Iteration

`Reader` implements the iterator protocol. Each call to `__next__` returns a `dict`:

- **First line** → parsed with `header` descriptor (if defined)
- **Last line** → parsed with `footer` descriptor (if defined and `lines_count` is known)
- **All other lines** → parsed with `details[0]` descriptor

```python
from pyfwf.readers import Reader

with open('data.fwf', 'r') as f:
    reader = Reader(f, fd)
    for row in reader:
        print(row)
```

---

## Attributes

| Attribute | Type | Description |
|---|---|---|
| `line_num` | `int` | Number of lines yielded so far |
| `lines_count` | `int` or `float` | Total number of lines (may be `float` for stream inputs) |
| `filesize` | `int` | Total byte size of the input |
| `newline` | `str` | The configured line terminator |

---

## Examples

### Reading from a file

```python
from pyfwf.readers import Reader
from pyfwf.descriptors import FileDescriptor, DetailRowDescriptor
from pyfwf.columns import CharColumn, PositiveIntegerColumn

fd = FileDescriptor(details=[
    DetailRowDescriptor([
        CharColumn('name', 20),
        PositiveIntegerColumn('score', 5),
    ])
])

with open('results.fwf', 'r') as f:
    for row in Reader(f, fd):
        print(row['name'], row['score'])
```

### Reading from a string

```python
from io import StringIO

data = "Alice Smith         00095\nBob Jones           00087\n"
for row in Reader(data, fd):
    print(row)
```

### Reading from a list

```python
lines = [
    "Alice Smith         00095\n",
    "Bob Jones           00087\n",
]
for row in Reader(lines, fd):
    print(row)
```

### File with header and footer

```python
for i, row in enumerate(Reader(f, fd)):
    if i == 0:
        print("Header:", row)
    else:
        print("Row:", row)
```
