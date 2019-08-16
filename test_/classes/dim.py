import unittest
import xml.etree.ElementTree as ET

import svd.classes

class case(unittest.TestCase):

    def test_no_name_exception(self):
        '''Required name field is missing'''

        xml = '''
        <root>
            <register>
                <dim>4</dim>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            svd.classes.dim.add_elements(None, None, node, 'register')

    def test_no_dim(self):
        '''Normal generation if dim is missing'''

        xml = '''
        <root>
            <register>
                <name>Name</name>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        test = []
        svd.classes.dim.add_elements(None, test, node, 'register')
        self.assertEqual(len(test), 1)

        self.assertEqual(test[0].name, "Name")

    def test_index_fix(self):
        '''Fixed array generation'''

        xml = '''
        <root>
            <register>
                <dim>4</dim>
                <dimIncrement>4</dimIncrement>
                <name>MyArr[%s]</name>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        test = []
        svd.classes.dim.add_elements(None, test, node, 'register')
        self.assertEqual(len(test), 1)

        self.assertEqual(test[0].name, "MyArr[4]")

    def test_index_list(self):
        '''Index generation by list'''

        xml = '''
        <root>
            <register>
                <dim>6</dim>
                <dimIncrement>4</dimIncrement>
                <dimIndex>A,B,C,D,E,Z</dimIndex>
                <name>GPIO_%s_CTRL</name>
                <description>GPIO Controller %s</description>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        test = []
        svd.classes.dim.add_elements(None, test, node, 'register')
        self.assertEqual(len(test), 6)

        self.assertEqual(test[0].name, "GPIO_A_CTRL")
        self.assertEqual(test[0].description, "GPIO Controller A")
        self.assertEqual(test[1].name, "GPIO_B_CTRL")
        self.assertEqual(test[1].description, "GPIO Controller B")
        self.assertEqual(test[2].name, "GPIO_C_CTRL")
        self.assertEqual(test[2].description, "GPIO Controller C")
        self.assertEqual(test[3].name, "GPIO_D_CTRL")
        self.assertEqual(test[3].description, "GPIO Controller D")
        self.assertEqual(test[4].name, "GPIO_E_CTRL")
        self.assertEqual(test[4].description, "GPIO Controller E")
        self.assertEqual(test[5].name, "GPIO_Z_CTRL")
        self.assertEqual(test[5].description, "GPIO Controller Z")

    def test_index_range(self):
        '''Index generation by range'''

        xml = '''
        <root>
            <register>
                <dim>4</dim>
                <dimIncrement>4</dimIncrement>
                <dimIndex>3-6</dimIndex>
                <dimName>irq%s_t</dimName>
                <name>IRQ%s</name>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        test = []
        svd.classes.dim.add_elements(None, test, node, 'register')
        self.assertEqual(len(test), 4)

        self.assertEqual(test[0].name, "IRQ3")
        self.assertEqual(test[0].dim_name, "irq3_t")
        self.assertEqual(test[1].name, "IRQ4")
        self.assertEqual(test[1].dim_name, "irq4_t")
        self.assertEqual(test[2].name, "IRQ5")
        self.assertEqual(test[2].dim_name, "irq5_t")
        self.assertEqual(test[3].name, "IRQ6")
        self.assertEqual(test[3].dim_name, "irq6_t")

    def test_index_exception(self):
        '''dimIndex can not be interpreted as integer'''

        xml = '''
        <root>
            <register>
                <dim>4</dim>
                <dimIncrement>4</dimIncrement>
                <dimIndex>4x8</dimIndex>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        with self.assertRaises(ValueError):
            svd.classes.dim.add_elements(None, None, node, 'register')

    def test_length_exception(self):
        '''dimIndex has less elements than dim requires'''

        xml = '''
        <root>
            <register>
                <dim>4</dim>
                <dimIncrement>4</dimIncrement>
                <dimIndex>A,B,C</dimIndex>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        with self.assertRaises(AttributeError):
            svd.classes.dim.add_elements(None, None, node, 'register')
