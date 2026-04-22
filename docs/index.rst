Home
====

Python library for reading and manipulating **fixed-width files (FWF)**.

.. image:: https://img.shields.io/badge/GitHub-Repository-blue?logo=github
   :target: https://github.com/kelsoncm/python-pyfwf
   :alt: GitHub Repository

.. image:: https://github.com/kelsoncm/python-pyfwf/actions/workflows/test.yml/badge.svg
   :target: https://github.com/kelsoncm/python-pyfwf/actions/workflows/test.yml
   :alt: Test status

.. image:: https://codecov.io/gh/kelsoncm/python-pyfwf/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/kelsoncm/python-pyfwf
   :alt: Test coverage

.. image:: https://badge.fury.io/py/pyfwf.svg
   :target: https://badge.fury.io/py/pyfwf
   :alt: PyPI version

What is a fixed-width file?
---------------------------

A fixed-width file (FWF) is a plain-text file where each field occupies a
predetermined number of characters in every line. Unlike CSV, there are
no delimiters — position and length define each column.

.. code-block::none
    HDR SALES_REPORT                                   20240101
    D   Alice Smith                                    000001250
    D   Bob Jones                                      000000875
    FTR 00020000002125

Features
--------

- Read fixed-width format files with custom column definitions
- Support for typed columns: text, integer, decimal, date, time, datetime
- Header and footer row handling
- Render file descriptors as Markdown tables
- Serialise and deserialise file descriptors to/from JSON (hydration)
- 100% test coverage

Installation
------------

.. code-block:: bash

   pip install pyfwf

Requires Python 3.10+.

Quick example
-------------

.. code-block::python

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


Next steps
----------

.. toctree::
   :maxdepth: 1

   index
   getting-started
   api-descriptors
   api-columns
   api-readers
   api-renders
   api-hydrating
