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


__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


# import importlib
# from typing import Dict, List
#
#
# def get_full_class_name(instance_or_class):
#     if isinstance(instance_or_class, type):
#         return instance_or_class.__module__ + "." + instance_or_class.__qualname__
#     else:
#         return instance_or_class.__module__ + "." + instance_or_class.__class__.__qualname__
#
#
# def create_class(full_class_name, *args, **kwargs):
#     module_name, class_name = full_class_name.rsplit(".", 1)
#     MyClass = getattr(importlib.import_module(module_name), class_name)
#     return MyClass(*args, **kwargs)
#
#
# def hydrate(representation: Dict):
#     assert isinstance(representation, Dict), 'representation is not a Dict'
#     assert 'type' in representation, 'type not informed in representation'
#     assert isinstance(representation['type'], str), 'type is not a str'
#
#     if 'args' in representation:
#         assert isinstance(representation['args'], List), 'args is not a List'
#
#     args = []
#     if 'args' in representation:
#         for arg in representation['args']
#             args.append(arg)
#
#     kwargs = {}
#     if 'kwargs' in representation:
#         for kwarg in representation['kwargs']
#             kwargs.append(kwarg)
#     print(args, kwarg)
#     # instance = create_class(representation['type'], *args, **kwargs)
#
#
# class Hydrator(object):
#
#     @classmethod
#     def hydrate(cls, representation: Dict):
#         assert isinstance(representation, Dict), 'representation is not a Dict'
#         assert 'type' in representation, 'type not informed in representation'
#         assert isinstance(representation['type'], str), 'type is not a str'
#
#         if representation['type'] == get_full_class_name()
#
#         if 'args' in representation:
#             assert isinstance(representation['args'], List), 'args is not a List'
#
#         args = representation['args'] if 'args' in representation else []
#         kwargs = representation['args'] if 'kwargs' in representation else []
#
#         instance = create_class(representation['type'], *args, **kwargs)
