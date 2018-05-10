import unittest
import xml.etree.ElementTree as ET

from model import group

class group1(group):
    def __init__(self, parent = None):
        group.__init__(self, parent)
        self.name = "group1"
        self.size = 8

class group2(group):
    def __init__(self, parent = None):
        group.__init__(self, parent)
        self.name = "group2"
        self.size = 16

class test_class_group(unittest.TestCase):

    def test_access_group1(self):
        g1 = group1()
        chld = group(g1)

        self.assertEqual(g1.name, "group1")
        self.assertEqual(g1.size, 8)
        with self.assertRaises(AttributeError):
            self.assertIsNotNone(g1.access)

        with self.assertRaises(AttributeError):
            self.assertIsNotNone(chld.name)
        self.assertEqual(chld.size, 8)
        with self.assertRaises(AttributeError):
            self.assertIsNotNone(chld.access)

    def test_access_group2(self):
        g1 = group1()
        chld = group2(g1)

        self.assertEqual(g1.name, "group1")
        self.assertEqual(g1.size, 8)
        with self.assertRaises(AttributeError):
            self.assertIsNotNone(g1.access)

        self.assertEqual(chld.name, "group2")
        self.assertEqual(chld.size, 16)
        with self.assertRaises(AttributeError):
            self.assertIsNotNone(chld.access)

if __name__ == "__main__":
    unittest.main()
