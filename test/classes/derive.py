import unittest
import xml.etree.ElementTree as ET

import svd.classes

def peripheral_key(peripheral):
    return peripheral.name

class base_class(svd.classes.base):

    def __init__(self):
        svd.classes.base.__init__(self)
        self.children = []

    def add(self, obj):
        self.children.append(obj)

    def find(self, name):
        print("base_class.find")
        return next((x for x in self.children if x.name == name), None)

class parent_class(svd.classes.parent):

    def __init__(self, parent):
        svd.classes.parent.__init__(self, parent)
        self.children = []

    def add(self, obj):
        self.children.append(obj)

    def find(self, name):
        print("parent_class.find")
        return next((x for x in self.children if x.name == name), None)

    def copy(self):
        return parent_class()

class case(unittest.TestCase):

    def test_ctor(self):
        xml = '''
        <node derivedFrom="branch.leaf" />
        '''
        node = ET.fromstring(xml)

        xxx = '''
        root = base_class()
        root.name = 'root'
        branch = parent_class(root)
        branch.name = 'branch'
        root.add(branch)
        leaf = parent_class(branch)
        leaf.name = 'leaf'
        branch.add(leaf)

        test = svd.classes.derive(branch, node)
        print(type(test), type(leaf))
    #    print(type(test.parent), type(leaf.parent))
        print(test, leaf)
    #    print(test.parent, leaf.parent)
        print(test.__dict__)
        print(leaf.__dict__)

        self.assertEqual(test.parent, leaf.parent)

    #    self.assertUnequal()
    #    self.assertEqual(type(test), svd.classes.base)
        '''
