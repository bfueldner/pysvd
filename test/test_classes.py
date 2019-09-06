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
        self.name = "root"
        self.register = []

        super().__init__(node)

    def parse(self, node):
        super().parse(node)

        HelperClassDeriveRegister.add_elements(self, self.register, node, 'register')

    def find(self, name):
        for register in self.register:
            if register.name == name:
                return register
        return None


class HelperClassDeriveRegister(pysvd.classes.Derive):

    def __init__(self, parent, node):
        self.field = []

        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'name', pysvd.parser.Text, True)
        self.add_attribute(node, 'description', pysvd.parser.Text, True)
        self.add_attribute(node, 'addressOffset', pysvd.parser.Integer)
        self.add_attribute(node, 'size', pysvd.parser.Integer)

        HelperClassDeriveField.add_elements(self, self.field, node, 'field')

    def find(self, name):
        for field in self.field:
            if field.name == name:
                return field
        return None


class HelperClassDeriveField(pysvd.classes.Derive):

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        self.add_attribute(node, 'name', pysvd.parser.Text, True)
        self.add_attribute(node, 'description', pysvd.parser.Text, True)
        self.add_attribute(node, 'access', pysvd.type.access)


class HelperClassDim(pysvd.classes.Dim):

    def __init__(self, parent, node):
        self.offset = 0
        super().__init__(parent, node)

    def set_offset(self, value):
        self.offset += value

    def parse(self, node):
        super().parse(node)


class TestClassBase(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(pysvd.classes.Base, object))

    def test_ctor(self):
        test = pysvd.classes.Base(None)

        self.assertEqual(type(test), pysvd.classes.Base)
        self.assertIsNone(test.node)
        self.assertIsNone(test.parent)
        self.assertIsNone(test.derivedFrom)

    def test_attributes(self):
        test = pysvd.classes.Base(None)

        attr = {}
        attr['name'] = 'test'
        attr['enable'] = True
        attr['none'] = None
        test.__dict__.update(attr)

        self.assertEqual(test.name, 'test')
        self.assertTrue(test.enable)
        with self.assertRaises(AttributeError):
            self.assertNone(test.none)

    def test_find(self):
        test = pysvd.classes.Base(None)

        self.assertIsNone(test.find("test"))


class TestClassParent(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(pysvd.classes.Parent, pysvd.classes.Base))

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
        test.__dict__.update(attr)

        self.assertEqual(test.name, 'test')
        self.assertTrue(test.enable)
        with self.assertRaises(AttributeError):
            self.assertNone(test.none)

    def test_find(self):
        test = pysvd.classes.Parent(None,  None)

        self.assertIsNone(test.find("test"))


class TestClassGroup(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(pysvd.classes.Group, pysvd.classes.Parent))

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
        test.__dict__.update(attr)

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
        test.__dict__.update(test_attr)
        child = pysvd.classes.Group(test, None)
        child.__dict__.update(child_attr)

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
        test.__dict__.update(test_attr)
        child = pysvd.classes.Group(test, None)
        child.__dict__.update(child_attr)
        subchild = pysvd.classes.Group(child, None)
        subchild.__dict__.update(subchild_attr)

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
        test.__dict__.update(test_attr)
        child = HelperClassGroupAttributes(test, None)
        child.__dict__.update(child_attr)

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

    def test_inheritance(self):
        self.assertTrue(issubclass(pysvd.classes.Derive, pysvd.classes.Group))

    def test_unknown_element_exception(self):
        xml = '''
        <root>
            <register>
                <name>TimerCtrl0</name>
                <description>Timer Control Register</description>
            </register>
            <register derivedFrom="UartCtrl0">
                <name>TimerCtrl1</name>
                <description>Derived Timer</description>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        with self.assertRaises(KeyError):
            HelperClassDeriveRoot(node)

    def test_path_level_exception(self):
        xml = '''
        <root>
            <register>
                <name>TimerCtrl0</name>
                <description>Timer Control Register</description>
            </register>
            <register derivedFrom="TimerCtrl0.BitField0">
                <name>TimerCtrl1</name>
                <description>Derived Timer</description>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        with self.assertRaises(KeyError):
            HelperClassDeriveRoot(node)

    def test_one_level(self):
        xml = '''
        <root>
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
        </root>'''

        node = ET.fromstring(xml)
        test = HelperClassDeriveRoot(node)

        self.assertEqual(len(test.register), 2)

        self.assertEqual(type(test.register[0]), HelperClassDeriveRegister)
        self.assertEqual(test.register[0].name, "TimerCtrl0")
        self.assertEqual(test.register[0].description, "Timer Control Register")
        self.assertEqual(test.register[0].addressOffset, 0)
        self.assertEqual(test.register[0].size, 32)
        self.assertIsNone(test.register[0].derivedFrom)

        self.assertEqual(type(test.register[1]), HelperClassDeriveRegister)
        self.assertEqual(test.register[1].name, "TimerCtrl1")
        self.assertEqual(test.register[1].description, "Derived Timer")
        self.assertEqual(test.register[1].addressOffset, 4)
        self.assertEqual(test.register[1].size, 32)
        self.assertEqual(test.register[1].derivedFrom, test.register[0])

    def test_two_level(self):
        xml = '''
        <root>
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
                    <access>read-only</access>
                </field>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        test = HelperClassDeriveRoot(node)

        self.assertEqual(len(test.register), 2)

        self.assertEqual(type(test.register[0]), HelperClassDeriveRegister)
        self.assertEqual(test.register[0].name, "TimerCtrl0")
        self.assertEqual(test.register[0].description, "Timer Control Register")
        self.assertEqual(test.register[0].addressOffset, 0)
        self.assertEqual(test.register[0].size, 32)
        self.assertIsNone(test.register[0].derivedFrom)

        self.assertEqual(len(test.register[0].field), 1)

        self.assertEqual(test.register[0].field[0].name, "BitField0")
        self.assertEqual(test.register[0].field[0].description, "Bit field 0")
        self.assertEqual(test.register[0].field[0].access, pysvd.type.access.read_write)
        self.assertIsNone(test.register[0].field[0].derivedFrom)

        self.assertEqual(type(test.register[1]), HelperClassDeriveRegister)
        self.assertEqual(test.register[1].name, "TimerCtrl1")
        self.assertEqual(test.register[1].description, "Derived Timer")
        self.assertEqual(test.register[1].addressOffset, 4)
        self.assertEqual(test.register[1].size, 32)
        self.assertEqual(test.register[1].derivedFrom, test.register[0])

        self.assertEqual(len(test.register[1].field), 2)

        self.assertEqual(test.register[1].field[0].name, "BitField0")
        self.assertEqual(test.register[1].field[0].description, "Bit field 0")
        self.assertEqual(test.register[1].field[0].access, pysvd.type.access.read_write)
        self.assertIsNone(test.register[1].field[0].derivedFrom)

        self.assertEqual(test.register[1].field[1].name, "BitField1")
        self.assertEqual(test.register[1].field[1].description, "Bit field 1")
        self.assertEqual(test.register[1].field[1].access, pysvd.type.access.read_only)
        self.assertEqual(test.register[1].field[1].derivedFrom, test.register[0].field[0])

    def test_derive_from_derived(self):
        xml = '''
        <root>
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
                    <access>read-only</access>
                </field>
            </register>
            <register derivedFrom="TimerCtrl1">
                <name>TimerCtrl2</name>
                <description>Double Derived Timer</description>
                <addressOffset>0x8</addressOffset>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        test = HelperClassDeriveRoot(node)

        self.assertEqual(len(test.register), 3)

        self.assertEqual(type(test.register[0]), HelperClassDeriveRegister)
        self.assertEqual(test.register[0].name, "TimerCtrl0")
        self.assertEqual(test.register[0].description, "Timer Control Register")
        self.assertEqual(test.register[0].addressOffset, 0)
        self.assertEqual(test.register[0].size, 32)
        self.assertIsNone(test.register[0].derivedFrom)

        self.assertEqual(len(test.register[0].field), 1)

        self.assertEqual(test.register[0].field[0].name, "BitField0")
        self.assertEqual(test.register[0].field[0].description, "Bit field 0")
        self.assertEqual(test.register[0].field[0].access, pysvd.type.access.read_write)
        self.assertIsNone(test.register[0].field[0].derivedFrom)

        self.assertEqual(type(test.register[1]), HelperClassDeriveRegister)
        self.assertEqual(test.register[1].name, "TimerCtrl1")
        self.assertEqual(test.register[1].description, "Derived Timer")
        self.assertEqual(test.register[1].addressOffset, 4)
        self.assertEqual(test.register[1].size, 32)
        self.assertEqual(test.register[1].derivedFrom, test.register[0])

        self.assertEqual(len(test.register[1].field), 2)

        self.assertEqual(test.register[1].field[0].name, "BitField0")
        self.assertEqual(test.register[1].field[0].description, "Bit field 0")
        self.assertEqual(test.register[1].field[0].access, pysvd.type.access.read_write)
        self.assertIsNone(test.register[1].field[0].derivedFrom)

        self.assertEqual(test.register[1].field[1].name, "BitField1")
        self.assertEqual(test.register[1].field[1].description, "Bit field 1")
        self.assertEqual(test.register[1].field[1].access, pysvd.type.access.read_only)
        self.assertEqual(test.register[1].field[1].derivedFrom, test.register[0].field[0])

        self.assertEqual(type(test.register[2]), HelperClassDeriveRegister)
        self.assertEqual(test.register[2].name, "TimerCtrl2")
        self.assertEqual(test.register[2].description, "Double Derived Timer")
        self.assertEqual(test.register[2].addressOffset, 8)
        self.assertEqual(test.register[2].size, 32)
        self.assertEqual(test.register[2].derivedFrom, test.register[1])

        self.assertEqual(len(test.register[2].field), 2)

        self.assertEqual(test.register[2].field[0].name, "BitField0")
        self.assertEqual(test.register[2].field[0].description, "Bit field 0")
        self.assertEqual(test.register[2].field[0].access, pysvd.type.access.read_write)
        self.assertIsNone(test.register[2].field[0].derivedFrom)

        self.assertEqual(test.register[2].field[1].name, "BitField1")
        self.assertEqual(test.register[2].field[1].description, "Bit field 1")
        self.assertEqual(test.register[2].field[1].access, pysvd.type.access.read_only)
        self.assertEqual(test.register[2].field[1].derivedFrom, test.register[0].field[0])


class TestClassDim(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(pysvd.classes.Dim, pysvd.classes.Derive))
        self.assertTrue(issubclass(HelperClassDim, pysvd.classes.Dim))

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
                <description>Description</description>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        test = []
        pysvd.classes.Dim.add_elements(None, test, node, 'register')
        self.assertEqual(len(test), 1)

        self.assertEqual(test[0].name, "Name")
        self.assertEqual(test[0].description, "Description")

    def test_index_minimal(self):
        '''Minimal register generation'''

        xml = '''
        <root>
            <register>
                <dim>4</dim>
                <dimIncrement>2</dimIncrement>
                <name>PORT%s</name>
                <description>Port %s</description>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        test = []
        HelperClassDim.add_elements(None, test, node, 'register')
        self.assertEqual(len(test), 4)

        self.assertEqual(test[0].name, "PORT0")
        self.assertEqual(test[0].description, "Port 0")
        self.assertEqual(test[0].offset, 0)

        self.assertEqual(test[1].name, "PORT1")
        self.assertEqual(test[1].description, "Port 1")
        self.assertEqual(test[1].offset, 2)

        self.assertEqual(test[2].name, "PORT2")
        self.assertEqual(test[2].description, "Port 2")
        self.assertEqual(test[2].offset, 4)

        self.assertEqual(test[3].name, "PORT3")
        self.assertEqual(test[3].description, "Port 3")
        self.assertEqual(test[3].offset, 6)

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
        HelperClassDim.add_elements(None, test, node, 'register')
        self.assertEqual(len(test), 6)

        self.assertEqual(test[0].name, "GPIO_A_CTRL")
        self.assertEqual(test[0].description, "GPIO Controller A")
        self.assertEqual(test[0].offset, 0)
        self.assertEqual(test[1].name, "GPIO_B_CTRL")
        self.assertEqual(test[1].description, "GPIO Controller B")
        self.assertEqual(test[1].offset, 4)
        self.assertEqual(test[2].name, "GPIO_C_CTRL")
        self.assertEqual(test[2].description, "GPIO Controller C")
        self.assertEqual(test[2].offset, 8)
        self.assertEqual(test[3].name, "GPIO_D_CTRL")
        self.assertEqual(test[3].description, "GPIO Controller D")
        self.assertEqual(test[3].offset, 12)
        self.assertEqual(test[4].name, "GPIO_E_CTRL")
        self.assertEqual(test[4].description, "GPIO Controller E")
        self.assertEqual(test[4].offset, 16)
        self.assertEqual(test[5].name, "GPIO_Z_CTRL")
        self.assertEqual(test[5].description, "GPIO Controller Z")
        self.assertEqual(test[5].offset, 20)

    def test_index_range(self):
        '''Index generation by range'''

        xml = '''
        <root>
            <register>
                <dim>4</dim>
                <dimIncrement>8</dimIncrement>
                <dimIndex>3-6</dimIndex>
                <dimName>irq%s_t</dimName>
                <name>IRQ%s</name>
                <description>Interrupt %s</description>
            </register>
        </root>'''

        node = ET.fromstring(xml)
        test = []
        HelperClassDim.add_elements(None, test, node, 'register')
        self.assertEqual(len(test), 4)

        self.assertEqual(test[0].name, "IRQ3")
        self.assertEqual(test[0].description, "Interrupt 3")
        self.assertEqual(test[0].dimName, "irq3_t")
        self.assertEqual(test[0].offset, 0)
        self.assertEqual(test[1].name, "IRQ4")
        self.assertEqual(test[1].description, "Interrupt 4")
        self.assertEqual(test[1].dimName, "irq4_t")
        self.assertEqual(test[1].offset, 8)
        self.assertEqual(test[2].name, "IRQ5")
        self.assertEqual(test[2].description, "Interrupt 5")
        self.assertEqual(test[2].dimName, "irq5_t")
        self.assertEqual(test[2].offset, 16)
        self.assertEqual(test[3].name, "IRQ6")
        self.assertEqual(test[3].description, "Interrupt 6")
        self.assertEqual(test[3].dimName, "irq6_t")
        self.assertEqual(test[3].offset, 24)

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
