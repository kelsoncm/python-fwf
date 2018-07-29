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

#
# import json, io
from unittest import TestCase
# from pybatchfile.readers import Reader
from pybatchfile.classutils import Hydrator, hydrate_class


class WeCanTest(Hydrator):

    def __init__(self, nested=None, *args, **kwargs):
        super(WeCanTest, self).__init__()
        self.args = list(args)
        self.kwargs = kwargs
        self.nested = nested


class TestFunctionHydrate(TestCase):
    def test_hydrate_class(self):
        self.assertIsInstance(hydrate_class({'_hydrate_as': 'test_classutils.WeCanTest'}), WeCanTest)

    def test_hydrate_wrong_args__empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', hydrate_class)

    def test_hydrate_wrong_args__representation_not_dict(self):
        self.assertRaisesRegex(AssertionError, 'representation.*Dict', hydrate_class, '')

    def test_hydrate_wrong_args__type_not_informed(self):
        self.assertRaisesRegex(AssertionError, '_hydrate_as is required', hydrate_class, {})

    def test_hydrate_wrong_args__type_not_str(self):
        self.assertRaisesRegex(AssertionError, '_hydrate_as has informed.*str', hydrate_class, {'_hydrate_as': 1})

    def test_hydrate_wrong_args__type_not_exists(self):
        self.assertRaisesRegex(AttributeError, 'test_classutils.*WeCanTest2', hydrate_class,
                               {'_hydrate_as': 'test_classutils.WeCanTest2'})

    def test_hydrate_wrong_args__args_not_list(self):
        self.assertRaisesRegex(AssertionError, 'args.*List', hydrate_class,
                               {'_hydrate_as': 'test_classutils.WeCanTest', 'args': None})

    def test_hydrate_wrong_args__kwargs_not_dict(self):
        self.assertRaisesRegex(AssertionError, 'kwargs.*Dict', hydrate_class,
                               {'_hydrate_as': 'test_classutils.WeCanTest', 'kwargs': None})

    def test_hydrate_wrong_args__attributes_not_dict(self):
        self.assertRaisesRegex(AssertionError, 'attributes.*Dict', hydrate_class,
                               {'_hydrate_as': 'test_classutils.WeCanTest', 'attributes': None})

    def test_hydrate_let_args__args(self):
        instance = hydrate_class({'_hydrate_as': 'test_classutils.WeCanTest', 'args': ['nested', 'me', 12]})
        self.assertEqual(instance.nested, 'nested')
        self.assertListEqual(instance.args, ['me', 12])

    def test_hydrate_let_args__kwargs(self):
        instance = hydrate_class({'_hydrate_as': 'test_classutils.WeCanTest', 'kwargs': {'test': 'me', 'age': 12}})
        self.assertDictEqual(instance.kwargs, {'test': 'me', 'age': 12})

    def test_hydrate_let_args__attrs(self):
        instance = hydrate_class({'_hydrate_as': 'test_classutils.WeCanTest', 'attributes': {'test': 'me', 'age': 12}})
        self.assertEqual(instance.test, 'me')
        self.assertEqual(instance.age, 12)


class TestHydrator(TestCase):
    def test_hydrate_wrong__empty(self):
        self.assertRaisesRegex(TypeError, 'missing 1', Hydrator.hydrate)

    def test_hydrate__minimal(self):
        representation = {'_hydrate_as': 'test_classutils.WeCanTest'}
        self.assertIsInstance(Hydrator.hydrate(representation), Hydrator)

    def test_hydrate_let__attributes(self):
        representation = {'_hydrate_as': 'test_classutils.WeCanTest',
                          'attributes': {'test': 'me', 'age': 12}}
        instance = Hydrator.hydrate(representation)
        self.assertEqual(instance.test, 'me')
        self.assertEqual(instance.age, 12)

    def test_hydrate_let__attributes(self):
        representation = {
            '_hydrate_as': 'test_classutils.WeCanTest',
            'args': [{'_hydrate_as': 'test_classutils.WeCanTest'}, 'me', 12]
        }
        instance = Hydrator.hydrate(representation)
        self.assertEqual(instance.args, ['me', 12])
        self.assertIsInstance(instance.nested, WeCanTest)
        print(instance)
