import unittest

import svd.classes

class case(unittest.TestCase):

    def test_ctor(self):
        test = svd.classes.group(None, None)
        child = svd.classes.group(test, None)

        self.assertEqual(type(test), svd.classes.group)
        self.assertIsNone(test.parent)
        self.assertEqual(child.parent, test)

    def test_attributes(self):
        test = svd.classes.group(None, None)

        attr = {}
        attr['name'] = 'test'
        attr['enable'] = True
        attr['none'] = None
        test.add_attributes(attr)

        self.assertEqual(test.name, 'test')
        self.assertTrue(test.enable)
        with self.assertRaises(AttributeError):
            self.assertNone(test.none)

    def test_group(self):
        test_attr = {
            'name': 'test',
            'size': 8,
            'reset_value': 0xFFFF,
            'extra': 'xxx',
        }

        child_attr = {
            'name': 'child',
            'size': 16,
        }

        test = svd.classes.group(None, None)
        test.add_attributes(test_attr)
        child = svd.classes.group(test, None)
        child.add_attributes(child_attr)

        self.assertEqual(type(test), svd.classes.group)
        self.assertIsNone(test.parent)
        self.assertEqual(child.parent, test)

        self.assertEqual(test.name, 'test')
        self.assertEqual(test.size, 8)
        self.assertEqual(test.reset_value, 0xFFFF)
        self.assertEqual(test.extra, 'xxx')

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.size, 16)
        self.assertEqual(child.reset_value, 0xFFFF)
        with self.assertRaises(AttributeError):
            self.assertIsNone(child.extra)
