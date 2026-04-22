Renders
=======

Module: ``pyfwf.renders``


render_as_markdown
------------------

Renders a ``FileDescriptor`` as a Markdown table, one section per row type (HEADER, DETAILS n, FOOTER).

**Signature**

.. code-block::python
    render_as_markdown(file_descriptor: FileDescriptor, out: StringIO) -> None

================== ================= ========================================
Argument           Type              Description
================== ================= ========================================
file_descriptor    FileDescriptor    The layout to render
out                StringIO          Output buffer to write the Markdown into
================== ================= ========================================

The function writes directly to ``out`` and returns ``None``.

Output format
-------------

Each section produces a heading and a Markdown table:

.. code-block::markdown
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

Column widths in the table are adjusted to fit the longest name/type in each section.

Example
-------

.. code-block::python
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

Saving to a file
----------------

.. code-block::python
    with open('layout.md', 'w') as f:
        buf = StringIO()
        render_as_markdown(fd, buf)
        f.write(buf.getvalue())


render_as_rst
-------------

Renders a ``FileDescriptor`` as uma tabela grid RST (ReStructuredText),
uma seção por tipo de linha (HEADER, DETAILS n, FOOTER).

**Signature**

.. code-block::python
    render_as_rst(file_descriptor: FileDescriptor, out: StringIO) -> None

================== ================= ========================================
Argument           Type              Description
================== ================= ========================================
file_descriptor    FileDescriptor    The layout to render
out                StringIO          Output buffer to write the RST into
================== ================= ========================================

O resultado é escrito diretamente em ``out`` e a função retorna ``None``.

Formato de saída
----------------

Cada seção gera um título e uma tabela grid RST:

.. code-block::rst
    HEADER
    --------------------

    ===== ======= ==== ===== ==== ========== ============
    #     Column  Size Start End  Type       Description
    ===== ======= ==== ===== ==== ========== ============
    1     name    30   1     30   CharColumn Nome
    2     age     3    31    33   IntColumn  Idade
    ===== ======= ==== ===== ==== ========== ============

Exemplo
-------

.. code-block::python
    from io import StringIO
    from pyfwf.columns import CharColumn, PositiveIntegerColumn
    from pyfwf.descriptors import DetailRowDescriptor, FooterRowDescriptor, FileDescriptor
    from pyfwf.renders import render_as_rst

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
    render_as_rst(fd, buf)
    print(buf.getvalue())

render_as_html
--------------

Renders a ``FileDescriptor`` as a HTML table, one section per row type (HEADER, DETAILS n, FOOTER).

**Signature**

.. code-block::python
    render_as_html(file_descriptor: FileDescriptor, out: StringIO) -> None

================== ================= ========================================
Argument           Type              Description
================== ================= ========================================
file_descriptor    FileDescriptor    The layout to render
out                StringIO          Output buffer to write the HTML into
================== ================= ========================================

The function writes directly to ``out`` and returns ``None``.

Output format
-------------

Each section produces a <h2> heading and a HTML table:

.. code-block::html
    <h2>HEADER</h2>
    <table border="1">
      <tr><th>#</th><th>Column</th><th>Size</th><th>Start</th><th>End</th><th>Type</th><th>Description</th></tr>
      <tr><td>1</td><td>name</td><td>30</td><td>1</td><td>30</td><td>CharColumn</td><td>Nome</td></tr>
      <tr><td>2</td><td>age</td><td>3</td><td>31</td><td>33</td><td>IntColumn</td><td>Idade</td></tr>
    </table>

Example
-------

.. code-block::python
    from io import StringIO
    from pyfwf.columns import CharColumn, PositiveIntegerColumn
    from pyfwf.descriptors import DetailRowDescriptor, FooterRowDescriptor, FileDescriptor
    from pyfwf.renders import render_as_html

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
    render_as_html(fd, buf)
    print(buf.getvalue())
