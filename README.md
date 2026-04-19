# Python FWF

Python library for reading and manipulating **fixed-width files (FWF)**.

## Features

- 📖 Read fixed-width format files with custom column definitions
- 🔧 Support for typed columns (integer, decimal, date, time, etc.)
- 📋 Header and footer row handling
- 🎯 Simple and intuitive API
- ✅ Fully tested (100% coverage)

## Installation

```bash
pip install pyfwf
```

## Quick Start

```python
from pyfwf.columns import CharColumn, PositiveIntegerColumn
from pyfwf.descriptors import DetailRowDescriptor, FileDescriptor
from pyfwf.readers import Reader

# Define columns
detail = DetailRowDescriptor([
    CharColumn(name='name', pos=1, size=20),
    PositiveIntegerColumn(name='age', pos=21, size=3),
])

# Create file descriptor
fd = FileDescriptor(line_size=23, details=[detail])

# Read file
with open('data.fwf', 'r') as f:
    reader = Reader(f, fd)
    for row in reader:
        print(row)
```

## Supported Column Types

- `CharColumn` - Text data
- `RightCharColumn` - Right-aligned text
- `PositiveIntegerColumn` - Positive integers
- `PositiveDecimalColumn` - Decimal numbers
- `DateColumn` - Date values
- `TimeColumn` - Time values
- `DateTimeColumn` - DateTime values

## Documentation

See [docs/](docs/) for detailed documentation and examples.

## License

MIT License © 2015 Umbrella Tech

## Author

Kelson da Costa Medeiros <kelsoncm@gmail.com>
