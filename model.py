import argparse
import sys
import datetime
import xml.etree.ElementTree as ET

from enum import Enum

# https://www.python-course.eu/python3_inheritance.php
# https://docs.python.org/3/library/enum.html

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

cpuNameType = [
    'CM0',
    'CM0PLUS',
    'CM0+',
    'CM1',
    'SC000',
    'CM23',
    'CM3',
    'CM33',
    'SC300',
    'CM4',
    'CM7',
    'CA5',
    'CA7',
    'CA8',
    'CA9',
    'CA15',
    'CA17',
    'CA53',
    'CA57',
    'CA72',
    'other',
]

endianType = [
    'little',
    'big',
    'selectable',
    'other',
]

usageType = [
    'registers',
    'buffer',
    'reserved'
]

accessType = [
    'read-only',
    'write-only',
    'read-write',
    'writeOnce',
    'read-writeOnce',
]

protectionStringType = [
    's',
    'n',
    'p'
]



class base(object):
    """Base class for all SVD elements"""

#    def __init__(self):
#        self.parent = None

    def __init__(self, parent):
        self.parent = parent

#   @classmethod
#   def from_points(cls, point_from, point_to):

    def __getattr__(self, attr):
        if self.parent is not None:
            return self.parent.__getattribute__(attr)
#        print("Has no attribute '{}'".format(attr))
#        return None
        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, attr))

class address_block(base):

    def __init__(self, parent, node):
        base.__init__(self, parent)

        self.offset = scaled_non_negative_integer(node, 'offset', True)
        self.size = scaled_non_negative_integer(node, 'size', True)
        self.usage = _get_enum(node, 'usage', usageType, True)
        self.protection = None

class interrupt(base):

    def __init__(self, parent, node):
        base.__init__(self, parent)

        self.name = _get_text(node, 'name', True)
        self.description = _get_text(node, 'description', False)
        self.value = _get_int(node, 'value', True)

class register(base):

    forward = [
        'size',
        'access',
        'reset_value'
        'reset_mask'
    ]

    def __init__(self, parent, node):
        derived_from = node.get('derivedFrom')
        if derived_from is not None:
            base_class = parent.find(derived_from)
            print("Gefunden! {}".format(base_class.name))
            self.__dict__ = dict(base_class.__dict__)

        base.__init__(self, parent)

        print("__dict__!")
        for a in self.__dict__:
            print("{}".format(a))

    #    Assign only of not None

        # Mandatory attributes for derived registers
        self.name = _get_text(node, 'name', True)
        self.description = _get_text(node, 'description', False)
        self.address_offset = _get_int(node, 'addressOffset', True)

    #       var1 = 4 if var1 is None else var1

        # Other attributes
        self.size = _get_int(node, 'size', False)
        self.access = _get_enum(node, 'access', accessType, False)
        self.protection = _get_enum(node, 'protection', protectionStringType, False)
        self.reset_value = _get_int(node, 'resetValue', False)
        self.reset_mask = _get_int(node, 'resetMask', False)

        print("Clear None elements")

class registers(base):

    def __init__(self, parent, node):
        base.__init__(self, parent)

        self.register = []
        for child in node.findall('./register'):
            self.register.append(register(self, child))

    def find(self, name):
        for register in self.register:
            if register.name == name:
                return register
        return None

class cpu(base):

    def __init__(self, parent, node):
       base.__init__(self, parent)

#      Parse all elements by list, use same type names as in dts, use enum!

       self.name = _get_enum(node, 'name', cpuNameType, True)
       self.revision = _get_text(node, 'revision', True)
       self.endian = _get_enum(node, 'endian', endianType, True)
       self.mpu_present = _get_boolean(node, 'mpuPresent', True)
       self.fpu_present = _get_boolean(node, 'fpuPresent', True)

class test1(base):

#    def __init__(self):
#       base.__init__(self)

    def __init__(self, parent):
        base.__init__(self)
        self.parent = parent
        self.name = "Name"

class test2(base):

#    def __init__(self):
#       base.__init__(self)

    def __init__(self, parent):
        base.__init__(self)
        self.parent = parent
        self.value = "Value"

class SVDdim(object):

    def __init__(self, parent, node):
        self.parent = parent

        self.index = 0
        self.end = 5

        self.dim = _get_int(node, 'dim', True)
        self.dim_increment = _get_int(node, 'dimIncrement', True)
        self.dim_text = _get_text(node, 'dimIndex', False, 0)
        self.dim_name = _get_text(node, 'dimName', False, 0)

    def __iter__(self):
        self.index = 0
        print("iterator?")
        return self

    def __next__(self):
        if self.index < self.end:
            self.index += 1
            return self.index
        raise StopIteration
