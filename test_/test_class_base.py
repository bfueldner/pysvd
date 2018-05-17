import unittest
import xml.etree.ElementTree as ET

from model import base

class test_class_base(unittest.TestCase):

    def test_ctor_default(self):
        prnt = base()

        self.assertIsNone(prnt.parent)

    def test_ctor_child(self):
        prnt = base()
        chld = base(prnt)

        self.assertIsNone(prnt.parent)
        self.assertIsNotNone(chld.parent)
        self.assertEqual(prnt, chld.parent)

if __name__ == "__main__":
    unittest.main()
