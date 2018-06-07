import unittest

import svd.classes

class case(unittest.TestCase):

    def test_ctor(self):
        test = svd.classes.base(None)

        self.assertEqual(type(test), svd.classes.base)

    def test_attributes(self):
        test = svd.classes.base(None)

        attr = {}
        attr['name'] = 'test'
        attr['enable'] = True
        attr['none'] = None
        test.add_attributes(attr)

        self.assertEqual(test.name, 'test')
        self.assertTrue(test.enable)
        with self.assertRaises(AttributeError):
            self.assertNone(test.none)
