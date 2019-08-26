import unittest
import xml.etree.ElementTree as ET

import pysvd


# Used in TestClassGroup.test_group_attributes
class HelperClassGroupAttributes(pysvd.classes.Group):

    attributes = ['extra']

    def __init__(self, parent, node):
        super().__init__(parent, node)


class HelperClassDeriveRoot(pysvd.classes.Base):

    def __init__(self, node):
        super().__init__(node)

        self.name = "root"
        self.register = []
        HelperClassDeriveRegister.add_elements(self, self.register, node, 'register')

    def find(self, name):
        for register in self.register:
            if register.name == name:
                return register
        return None


class HelperClassDeriveRegister(pysvd.classes.Derive):

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description', True))
        attr['addressOffset'] = pysvd.parser.Integer(pysvd.node.Element(node, 'addressOffset'))
        attr['size'] = pysvd.parser.Integer(pysvd.node.Element(node, 'size'))
        self.add_attributes(attr)

        self.field = []
        HelperClassDeriveField.add_elements(self, self.field, node, 'field')

    def find(self, name):
        for field in self.field:
            if field.name == name:
                return field
        return None


class HelperClassDeriveField(pysvd.classes.Derive):

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description', True))
        attr['access'] = pysvd.parser.Enum(pysvd.type.access, pysvd.node.Element(node, 'access'))
        self.add_attributes(attr)


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
            'resetValue': 0xFFFF,
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
        self.assertEqual(test.resetValue, 0xFFFF)
        self.assertEqual(test.extra, 'xxx')

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.size, 16)
        self.assertEqual(child.resetValue, 0xFFFF)
        with self.assertRaises(AttributeError):
            self.assertIsNone(child.extra)

    def test_group_multilevel(self):
        test_attr = {
            'name': 'test',
            'size': 8,
            'resetValue': 0xFFFF,
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
        self.assertEqual(test.resetValue, 0xFFFF)
        self.assertEqual(test.extra, 'xxx')

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.size, 16)
        self.assertEqual(child.resetValue, 0xFFFF)
        with self.assertRaises(AttributeError):
            self.assertIsNone(child.extra)

        self.assertEqual(subchild.name, 'subchild')
        self.assertEqual(subchild.size, 16)
        self.assertEqual(subchild.resetValue, 0xFFFF)
        with self.assertRaises(AttributeError):
            self.assertIsNone(subchild.extra)

    def test_group_attributes(self):
        test_attr = {
            'name': 'test',
            'size': 8,
            'resetValue': 0xFFFF,
            'extra': 'xxx',
        }

        child_attr = {
            'name': 'child',
            'size': 16,
        }

        test = pysvd.classes.Group(None, None)
        test.add_attributes(test_attr)
        child = HelperClassGroupAttributes(test, None)
        child.add_attributes(child_attr)

        self.assertEqual(type(test), pysvd.classes.Group)
        self.assertEqual(type(child), HelperClassGroupAttributes)

        self.assertIsNone(test.parent)
        self.assertEqual(child.parent, test)

        self.assertEqual(test.name, 'test')
        self.assertEqual(test.size, 8)
        self.assertEqual(test.resetValue, 0xFFFF)
        self.assertEqual(test.extra, 'xxx')

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.size, 16)
        self.assertEqual(child.extra, 'xxx')

        with self.assertRaises(AttributeError):
            self.assertIsNone(child.reset_value)


class TestClassDerive(unittest.TestCase):

    def test_exception(self):
        xml = '''
        <registers>
            <register>
                <name>TimerCtrl0</name>
                <description>Timer Control Register</description>
            </register>
            <register derivedFrom="UartCtrl0">
                <name>TimerCtrl1</name>
                <description>Derived Timer</description>
            </register>
        </registers>'''

        node = ET.fromstring(xml)
        with self.assertRaises(KeyError):
            HelperClassDeriveRoot(node)

    def test_one_level(self):
        xml = '''
        <registers>
            <register>
                <name>TimerCtrl0</name>
                <description>Timer Control Register</description>
                <addressOffset>0x0</addressOffset>
                <access>read-write</access>
                <resetValue>0x00008001</resetValue>
                <resetMask>0x0000ffff</resetMask>
                <size>32</size>
            </register>
            <register derivedFrom="TimerCtrl0">
                <name>TimerCtrl1</name>
                <description>Derived Timer</description>
                <addressOffset>0x4</addressOffset>
            </register>
        </registers>'''

        node = ET.fromstring(xml)
        test = HelperClassDeriveRoot(node)

        self.assertEqual(len(test.register), 2)

        self.assertEqual(type(test.register[0]), HelperClassDeriveRegister)
        self.assertEqual(test.register[0].name, "TimerCtrl0")
        self.assertEqual(test.register[0].description, "Timer Control Register")
        self.assertEqual(test.register[0].addressOffset, 0)
        self.assertEqual(test.register[0].size, 32)
        self.assertFalse(test.register[0].derived)

        self.assertEqual(type(test.register[1]), HelperClassDeriveRegister)
        self.assertEqual(test.register[1].name, "TimerCtrl1")
        self.assertEqual(test.register[1].description, "Derived Timer")
        self.assertEqual(test.register[1].addressOffset, 4)
        self.assertEqual(test.register[1].size, 32)
        self.assertTrue(test.register[1].derived)

    def test_two_level(self):
        xml = '''
        <registers>
            <register>
                <name>TimerCtrl0</name>
                <description>Timer Control Register</description>
                <addressOffset>0x0</addressOffset>
                <access>read-write</access>
                <resetValue>0x00008001</resetValue>
                <resetMask>0x0000ffff</resetMask>
                <size>32</size>
                <field>
                    <name>BitField0</name>
                    <description>Bit field 0</description>
                    <access>read-write</access>
                </field>
            </register>
            <register derivedFrom="TimerCtrl0">
                <name>TimerCtrl1</name>
                <description>Derived Timer</description>
                <addressOffset>0x4</addressOffset>
                <field derivedFrom="TimerCtrl0.BitField0">
                    <name>BitField1</name>
                    <description>Bit field 1</description>
                </field>
            </register>
        </registers>'''

        node = ET.fromstring(xml)
        test = HelperClassDeriveRoot(node)

        self.assertEqual(len(test.register), 2)

        self.assertEqual(type(test.register[0]), HelperClassDeriveRegister)
        self.assertEqual(test.register[0].name, "TimerCtrl0")
        self.assertEqual(test.register[0].description, "Timer Control Register")
        self.assertEqual(test.register[0].addressOffset, 0)
        self.assertEqual(test.register[0].size, 32)
        self.assertFalse(test.register[0].derived)

        self.assertEqual(len(test.register[0].field), 1)

        self.assertEqual(test.register[0].field[0].name, "BitField0")
        self.assertEqual(test.register[0].field[0].description, "Bit field 0")
        self.assertEqual(test.register[0].field[0].access, pysvd.type.access.read_write)
        self.assertFalse(test.register[0].field[0].derived)

        self.assertEqual(type(test.register[1]), HelperClassDeriveRegister)
        self.assertEqual(test.register[1].name, "TimerCtrl1")
        self.assertEqual(test.register[1].description, "Derived Timer")
        self.assertEqual(test.register[1].addressOffset, 4)
        self.assertEqual(test.register[1].size, 32)
        self.assertTrue(test.register[1].derived)

        self.assertEqual(len(test.register[1].field), 1)

        self.assertEqual(test.register[1].field[0].name, "BitField1")
        self.assertEqual(test.register[1].field[0].description, "Bit field 1")
        self.assertEqual(test.register[1].field[0].access, pysvd.type.access.read_write)
        self.assertTrue(test.register[1].field[0].derived)


class TestClassDim(unittest.TestCase):

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
            pysvd.classes.Dim.add_elements(None, None, node, 'register')

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
        pysvd.classes.Dim.add_elements(None, test, node, 'register')
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
        pysvd.classes.Dim.add_elements(None, test, node, 'register')
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
        pysvd.classes.Dim.add_elements(None, test, node, 'register')
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
        pysvd.classes.Dim.add_elements(None, test, node, 'register')
        self.assertEqual(len(test), 4)

        self.assertEqual(test[0].name, "IRQ3")
        self.assertEqual(test[0].dimName, "irq3_t")
        self.assertEqual(test[1].name, "IRQ4")
        self.assertEqual(test[1].dimName, "irq4_t")
        self.assertEqual(test[2].name, "IRQ5")
        self.assertEqual(test[2].dimName, "irq5_t")
        self.assertEqual(test[3].name, "IRQ6")
        self.assertEqual(test[3].dimName, "irq6_t")

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
            pysvd.classes.Dim.add_elements(None, None, node, 'register')

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
            pysvd.classes.Dim.add_elements(None, None, node, 'register')
