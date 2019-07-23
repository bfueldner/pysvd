import unittest
import pysvd


class TestClassBase(unittest.TestCase):

    def test_ctor(self):
        test = pysvd.classes.Base(None)

        self.assertEqual(type(test), pysvd.classes.Base)

    def test_attributes(self):
        test = pysvd.classes.Base(None)

        attr = {}
        attr['name'] = 'test'
        attr['enable'] = True
        attr['none'] = None
        test.add_attributes(attr)

        self.assertEqual(test.name, 'test')
        self.assertTrue(test.enable)
        with self.assertRaises(AttributeError):
            self.assertNone(test.none)


class TestClassParent(unittest.TestCase):

    def test_ctor(self):
        test = pysvd.classes.Parent(None, None)
        child = pysvd.classes.Parent(test, None)

        self.assertEqual(type(test), pysvd.classes.Parent)
        self.assertIsNone(test.parent)
        self.assertEqual(child.parent, test)

    def test_attributes(self):
        test = pysvd.classes.Parent(None, None)

        attr = {}
        attr['name'] = 'test'
        attr['enable'] = True
        attr['none'] = None
        test.add_attributes(attr)

        self.assertEqual(test.name, 'test')
        self.assertTrue(test.enable)
        with self.assertRaises(AttributeError):
            self.assertNone(test.none)


class TestClassGroup(unittest.TestCase):

    def test_ctor(self):
        test = pysvd.classes.Group(None, None)
        child = pysvd.classes.Group(test, None)

        self.assertEqual(type(test), pysvd.classes.Group)
        self.assertIsNone(test.parent)
        self.assertEqual(child.parent, test)

    def test_attributes(self):
        test = pysvd.classes.Group(None, None)

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

        test = pysvd.classes.Group(None, None)
        test.add_attributes(test_attr)
        child = pysvd.classes.Group(test, None)
        child.add_attributes(child_attr)

        self.assertEqual(type(test), pysvd.classes.Group)
        self.assertEqual(type(child), pysvd.classes.Group)

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

    def test_group_multilevel(self):
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

        subchild_attr = {
            'name': 'subchild',
        }

        test = pysvd.classes.Group(None, None)
        test.add_attributes(test_attr)
        child = pysvd.classes.Group(test, None)
        child.add_attributes(child_attr)
        subchild = pysvd.classes.Group(child, None)
        subchild.add_attributes(subchild_attr)

        self.assertEqual(type(test), pysvd.classes.Group)
        self.assertEqual(type(child), pysvd.classes.Group)
        self.assertEqual(type(subchild), pysvd.classes.Group)

        self.assertIsNone(test.parent)
        self.assertEqual(child.parent, test)
        self.assertEqual(subchild.parent, child)

        self.assertEqual(test.name, 'test')
        self.assertEqual(test.size, 8)
        self.assertEqual(test.reset_value, 0xFFFF)
        self.assertEqual(test.extra, 'xxx')

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.size, 16)
        self.assertEqual(child.reset_value, 0xFFFF)
        with self.assertRaises(AttributeError):
            self.assertIsNone(child.extra)

        self.assertEqual(subchild.name, 'subchild')
        self.assertEqual(subchild.size, 16)
        self.assertEqual(subchild.reset_value, 0xFFFF)
        with self.assertRaises(AttributeError):
            self.assertIsNone(subchild.extra)

    def test_group_attributes(self):
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

        test = pysvd.classes.Group(None, None)
        test.add_attributes(test_attr)
        child = group_attributes(test, None)
        child.add_attributes(child_attr)

        self.assertEqual(type(test), pysvd.classes.Group)
        self.assertEqual(type(child), group_attributes)

        self.assertIsNone(test.parent)
        self.assertEqual(child.parent, test)

        self.assertEqual(test.name, 'test')
        self.assertEqual(test.size, 8)
        self.assertEqual(test.reset_value, 0xFFFF)
        self.assertEqual(test.extra, 'xxx')

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.size, 16)
        self.assertEqual(child.extra, 'xxx')

        with self.assertRaises(AttributeError):
            self.assertIsNone(child.reset_value)
