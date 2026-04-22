
Hydrating
=========

Module: ``pyfwf.hydrating``

Overview
--------

The hydrating module provides a lightweight serialisation mechanism that converts ``Hydrator``
subclass instances to/from plain Python dicts (suitable for JSON storage).

- **Dehydrate** — convert an object to a ``dict``
- **Hydrate** — reconstruct an object from that ``dict``

All column and descriptor classes in ``pyfwf`` extend ``Hydrator``, so a full ``FileDescriptor``
tree can be saved to JSON and restored exactly.

Hydrator (base class)
---------------------

``Hydrator`` is the base class for all serialisable objects in ``pyfwf`` (columns, descriptors).

**Class methods / instance methods**


==================================== ======================================================
Method                               Description
==================================== ======================================================
``dehydrate()``                      Serialise this instance to a ``dict``
``Hydrator.hydrate(representation)`` Class method — reconstruct an instance from a ``dict``
==================================== ======================================================

**Hydration control attributes**

Subclasses declare which attributes participate in serialisation:


======================== ============= =================================
Attribute                Type          Role
======================== ============= =================================
``hydrating_args``       ``list[str]`` Positional constructor arguments
``hydrating_kwargs``     ``list[str]`` Keyword constructor arguments
``hydrating_attributes`` ``list[str]`` Attributes set after construction
======================== ============= =================================


hydrate_object
--------------

.. code-block::python
    hydrate_object(representation: dict) -> object


Reconstruct a Python object from a representation dict.

The dict must contain `_hydrate_as` (a dotted `module.ClassName` string). Optional keys `args`, `kwargs`,
and `attributes` are passed to the constructor and post-construction attribute setting.

Nested dicts that also contain `_hydrate_as` are recursively hydrated.

**Example**

.. code-block::python
    from pyfwf.hydrating import hydrate_object

    obj = hydrate_object({
        "_hydrate_as": "pyfwf.columns.CharColumn",
        "args": ["name", 20]
    })
    # <CharColumn name='name' size=20>

dehydrate_object
----------------

.. code-block::python
    dehydrate_object(obj) -> dict


Serialise a `Hydrator` instance to a plain `dict`.

.. code-block::python
    from pyfwf.hydrating import dehydrate_object
    from pyfwf.columns import CharColumn

    col = CharColumn('name', 20)
    dehydrate_object(col)
    # {
    #   '_hydrate_as': 'pyfwf.columns.CharColumn',
    #   'args': ['name', 20, 'name']
    # }


Nested `Hydrator` instances are recursively dehydrated.

get_full_class_name
-------------------

.. code-block::python
    get_full_class_name(instance_or_class) -> str


Returns the fully-qualified class name (`module.ClassName`) for an instance or a class.

.. code-block::python
    from pyfwf.hydrating import get_full_class_name
    from pyfwf.columns import CharColumn

    get_full_class_name(CharColumn('x', 1))   # 'pyfwf.columns.CharColumn'
    get_full_class_name(CharColumn)            # 'pyfwf.columns.CharColumn'

Round-trip example
------------------

.. code-block::python
    from pyfwf.hydrating import dehydrate_object, hydrate_object
    from pyfwf.descriptors import FileDescriptor, DetailRowDescriptor
    from pyfwf.columns import CharColumn, PositiveIntegerColumn
    import json

    fd = FileDescriptor(details=[
        DetailRowDescriptor([
            CharColumn('name', 30),
            PositiveIntegerColumn('age', 3),
        ])
    ])

    # Serialise
    data = dehydrate_object(fd)
    json_str = json.dumps(data, indent=2)

    # Deserialise
    restored = hydrate_object(json.loads(json_str))
