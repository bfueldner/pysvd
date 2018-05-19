import unittest
import xml.etree.ElementTree as ET

from model import dim

class test_class_dimable(unittest.TestCase):
#    def test_exception(self):
#        svd = '''<region />'''
#        node = ET.fromstring(svd)
#        with self.assertRaises(SyntaxError):
#            test = region(None, node)

    def test_index_fix(self):
        svd = '''
        <register>
            <dim>4</dim>
            <dimIncrement>4</dimIncrement>
            <name>MyArr[%s]</name>
        </register>'''

        node = ET.fromstring(svd)
        test = dim(None, node)

    def test_index_list(self):
        svd = '''
        <register>
            <dim>6</dim>
            <dimIncrement>4</dimIncrement>
            <dimIndex>A,B,C,D,E,Z</dimIndex>
            <name>GPIO_%s_CTRL</name>
        </register>'''

        node = ET.fromstring(svd)
        test = dim(None, node)

    def test_index_range_numeric(self):
        svd = '''
        <register>
            <dim>4</dim>
            <dimIncrement>4</dimIncrement>
            <dimIndex>3-6</dimIndex>
            <name>IRQ%s</name>
        </register>'''

        node = ET.fromstring(svd)
        test = dim(None, node)

#    def test_index_range_alpha(self):
#        svd = '''
#        <register>
#            <dim>4</dim>
#            <dimIncrement>4</dimIncrement>
#            <dimIndex>D-F</dimIndex>
#            <name>IRQ%s</name>
#        </register>'''
#
#        node = ET.fromstring(svd)
#        test = dim(None, node)

if __name__ == "__main__":
    unittest.main()
