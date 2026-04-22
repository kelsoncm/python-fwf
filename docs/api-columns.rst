
Columns
=======

Module: ``pyfwf.columns``

AbstractColumn
--------------

Base class for all column types. Not used directly.

**Constructor arguments**

=============== ======= ======== =============================================
Argument        Type    Required Description
=============== ======= ======== =============================================
``_name``       ``str`` yes      Field name (used as dict key when reading)
``size``        ``int`` yes      Width of the field in characters
``description`` ``str`` no       Human-readable description; defaults to _name
=============== ======= ======== =============================================

**Instance attributes set after attaching to a descriptor**

========= ======= =========================================================
Name      Type    Description
========= ======= =========================================================
``start`` ``int`` 1-based start position in the line
``end``   ``int`` 1-based end position (computed: ``start`` + ``size`` - 1)
========= ======= =========================================================

**Methods**

=============================== =====================================================
Method                          Description
=============================== =====================================================
``to_value(slice: str) -> Any`` Parse a fixed-width string slice into a Python value
``to_str(value: Any) -> str``   Serialise a Python value back to a fixed-width string
=============================== =====================================================

CharColumn
----------

Left-aligned text field. Trailing spaces are stripped on read.

.. code-block::python
    from pyfwf.columns import CharColumn

    col = CharColumn('name', 20)
    col.to_value('Alice Smith         ')  # 'Alice Smith'
    col.to_str('Alice Smith')             # 'Alice Smith         '
    col.to_str(None)                      # '                    '

RightCharColumn
---------------

Right-aligned text field. Behaviour is identical to `CharColumn` on read (spaces stripped);
on write, the value is right-aligned within the field width.

.. code-block::python
    from pyfwf.columns import RightCharColumn

    col = RightCharColumn('code', 10)
    col.to_str('ABC')   # '       ABC'

PositiveIntegerColumn
---------------------

Non-negative integer field. Zero-padded on write.

.. code-block::python
    from pyfwf.columns import PositiveIntegerColumn

    col = PositiveIntegerColumn('count', 9)
    col.to_value('000001234')   # 1234
    col.to_str(1234)             # '000001234'
    col.to_str(None)             # '000000000'

**Constraints**
- Value must be `>= 0`.
- Booleans are rejected.

PositiveDecimalColumn
---------------------

Non-negative decimal field stored as an integer with implicit decimal places.

**Constructor arguments** (in addition to base)

=============== ======= ======== =============================================
Argument        Type    Default  Description
=============== ======= ======== =============================================
``decimals``    ``int`` ``2``    Number of implicit decimal places
=============== ======= ======== =============================================

.. code-block::python
    from pyfwf.columns import PositiveDecimalColumn

    col = PositiveDecimalColumn('price', 9, decimals=2)
    col.to_value('000001250')   # 12.50  (1250 / 10^2)
    col.to_str(12.50)            # '000001250'
    col.to_str(None)             # '000000000'

**Constraints**
- `decimals` must be a positive integer.
- `size > decimals`.
- Value must be a `float >= 0.0`.

DateTimeColumn
--------------

Date-and-time field using `strftime`/`strptime` format strings.

**Constructor arguments** (in addition to base — note: `size` is derived from the format)

=============== ======= ================== ==============================
Argument        Type    Default            Description
=============== ======= ================== ==============================
``_name``       ``str`` —                  Field name
``_format``     ``str`` ``'%d%m%Y%H%M'``   ``strftime``-compatible format
``description`` ``str`` ``None``           Human-readable description
=============== ======= ================== ==============================

.. code-block::python
    from pyfwf.columns import DateTimeColumn
    from datetime import datetime

    col = DateTimeColumn('created_at')            # size derived as 12
    col.to_value('311220241330')                  # datetime(2024, 12, 31, 13, 30)
    col.to_str(datetime(2024, 12, 31, 13, 30))   # '311220241330'
    col.to_str(None)                              # '000000000000'

---

## DateColumn

Date-only subclass of `DateTimeColumn`. Returns a `datetime.date`.

=============== ======= ================== ===================================
Argument        Type    Default            Description
=============== ======= ================== ===================================
``_format``     ``str`` ``'%d%m%Y'``       Must contain exactly 3 format codes
=============== ======= ================== ===================================

.. code-block::python
    from pyfwf.columns import DateColumn
    from datetime import date

    col = DateColumn('birth_date')
    col.to_value('31122024')           # date(2024, 12, 31)
    col.to_str(date(2024, 12, 31))    # '31122024'

TimeColumn
----------

Time-only subclass of `DateTimeColumn`. Returns a `datetime.time`.


=============== ======= ================== ===================================
Argument        Type    Default            Description
=============== ======= ================== ===================================
``_format``     ``str`` ``'%H%M'``         Must contain exactly 2 format codes
=============== ======= ================== ===================================

.. code-block::python
    from pyfwf.columns import TimeColumn
    from datetime import time

    col = TimeColumn('check_in')
    col.to_value('1330')           # time(13, 30)
    col.to_str(time(13, 30))      # '1330'

Column type summary
-------------------

========================= ============ ======== =========
Class                     Python type  Pad char Alignment
========================= ============ ======== =========
``CharColumn``            ``str``      space    left
``RightCharColumn``       ``str``      space    right
``PositiveIntegerColumn`` ``int``      ``0``    right
``PositiveDecimalColumn`` ``float``    ``0``    right
``DateTimeColumn``        ``datetime`` ``0``    —
``DateColumn``            ``date``     ``0``    —
``TimeColumn``            ``time``     ``0``    —
========================= ============ ======== =========

All columns accept ``None`` on write and produce a fully-padded blank/zero string.
