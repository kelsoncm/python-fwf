---
layout: home
title: Home
nav_order: 1
---

# pyfwf

Python library for reading and manipulating **fixed-width files (FWF)**.

[![Tests](https://github.com/kelsoncm/python-fwf/actions/workflows/test.yml/badge.svg)](https://github.com/kelsoncm/python-fwf/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/kelsoncm/python-fwf/branch/main/graph/badge.svg)](https://codecov.io/gh/kelsoncm/python-fwf)
[![PyPI version](https://badge.fury.io/py/pyfwf.svg)](https://badge.fury.io/py/pyfwf)

---

## What is a fixed-width file?

A fixed-width file (FWF) is a plain-text file where each field occupies a predetermined number of characters in every line. Unlike CSV, there are no delimiters — position and length define each column.

```
HDR SALES_REPORT                                   20240101
D   Alice Smith                                    000001250
D   Bob Jones                                      000000875
FTR 00020000002125
```

---

## Features

- Read fixed-width format files with custom column definitions
- Support for typed columns: text, integer, decimal, date, time, datetime
- Header and footer row handling
- Render file descriptors as Markdown tables
- Serialise and deserialise file descriptors to/from JSON (hydration)
- 100% test coverage

---

## Installation

```bash
pip install pyfwf
```

Requires Python 3.10+.

---

## Quick example

```python
from pyfwf.columns import CharColumn, PositiveIntegerColumn, PositiveDecimalColumn
from pyfwf.descriptors import DetailRowDescriptor, FileDescriptor
from pyfwf.readers import Reader

detail = DetailRowDescriptor([
    CharColumn('name', 30),
    PositiveIntegerColumn('age', 3),
    PositiveDecimalColumn('salary', 9, decimals=2),
])

fd = FileDescriptor(details=[detail])

with open('data.fwf', 'r') as f:
    reader = Reader(f, fd)
    for row in reader:
        print(row)
# {'name': 'Alice Smith', 'age': 30, 'salary': 3500.00}
```

---

## Next steps

- [Getting Started](getting-started) — step-by-step walkthrough
- [API Reference — Columns](api/columns) — all column types explained
- [API Reference — Descriptors](api/descriptors) — `FileDescriptor`, `RowDescriptor`
- [API Reference — Reader](api/readers) — reading FWF files
- [API Reference — Renders](api/renders) — generating Markdown tables
- [API Reference — Hydrating](api/hydrating) — JSON serialisation
