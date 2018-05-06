#import argparse
#import sys
#import datetime
#import xml.etree.ElementTree as ET
import re

import parser
import type

# https://www.python-course.eu/python3_inheritance.php
# https://docs.python.org/3/library/enum.html

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

    def add_attributes(self, attr):
        """Merge not None attr into class"""
        self.__dict__.update( {k: v for k, v in attr.items() if v is not None} )

class derived_from(base):
    """Base for deriveable classes"""

    def __init__(self, parent, node):
        # If derived, search class, copy its attributes and call base constructor
        value = node.get('derivedFrom')
        if value is not None:
            _class = parent.find(value)
            if _class is None:
                raise Exception("Child '{}' not found on parent '{}' to derive from".format(value, parent.name))
            self.__dict__ = dict(_class.__dict__)

        base.__init__(self, parent)

        # TODO Test type on derivedFrom search and support paths! http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_enumeratedValues

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

class enumerated_value(base):
    '''An enumeratedValue defines a map between an unsigned integer and a string.'''

    def __init__(self, parent, node):
        base.__init__(self, parent)

        attr = {}
        attr['name'] = parser.text(node, 'name', False)
        attr['description'] = parser.text(node, 'description', False)
        attr['value'] = parser.integer(node, 'value', False)
        attr['is_default'] = parser.boolean(node, 'isDefault', False)
        if attr['value'] is None and attr['is_default'] is None:
            raise Exception("Either 'value' or 'isDefault' is mandatory in enumeratedValue '{}'".format(attr['name']))
        self.add_attributes(attr)

class enumerated_values(derived_from):
    '''The concept of enumerated values creates a map between unsigned integers and an identifier string. In addition, a description string can be associated with each entry in the map.'''

    def __init__(self, parent, node):
        derived_from.__init__(self, parent, node)

        attr = {}
        attr['name'] = parser.text(node, 'name', False)
        attr['header_enum_name'] = parser.text(node, 'headerEnumName', False)
        attr['usage'] = parser.enum(type.enum_usage, node, 'usage', False, type.enum_usage.read_write)
        self.add_attributes(attr)

        self.enumerated_value = []
        for child in node.findall('./enumeratedValue'):
            self.enumerated_value.append(enumerated_value(self, child))

class field(derived_from):

    def __init__(self, parent, node):
        derived_from.__init__(self, parent, node)

        attr = {}
        attr['name'] = parser.text(node, 'name', True)
        attr['description'] = parser.text(node, 'description', False)

        # bitRangeOffsetWidthStyle
        bit_offset = parser.integer(node, 'bitOffset', False)
        bit_width = parser.integer(node, 'bitWidth', False)
        if bit_offset is not None:
            # If bitWidth is not set, default is 1
            bit_width = 1 if bit_width is None else bit_width
        else:
            # bitRangeLsbMsbStyle
            lsb = parser.integer(node, 'lsb', False)
            msb = parser.integer(node, 'msb', False)
            if lsb is None or msb is None:
                bit_range = parser.text(node, 'bitRange', False)
                if bit_range is None:
                    raise ValueError("Field '{}' has no valid bit-range".format(attr['name']))

                match = re.search('\[([0-9]+):([0-9]+)\]', bit_range)
                lsb = int(match.group(2))
                msb = int(match.group(1))

            bit_offset = lsb
            bit_width = (msb - lsb) + 1

        attr['bit_offset'] = bit_offset
        attr['bit_width'] = bit_width

        attr['access'] = parser.enum(type.access, node, 'access', False)
        attr['modified_write_values'] = parser.enum(type.modified_write_values, node, 'modifiedWriteValues', False)
    #   write_constraint
        attr['read_action'] = parser.enum(type.read_action, node, 'readAction', False)
        self.add_attributes(attr)

        node = node.find('enumerated_values')
        if node is not None:
            self.enumerated_values = enumerated_values(self, node)

class fields(base):
    '''List of field'''

    def __init__(self, parent, node):
        base.__init__(self, parent)

        self.field = []
        for child in node.findall('./field'):
            self.field.append(field(self, child))

class register(derived_from):

    def __init__(self, parent, node):
        derived_from.__init__(self, parent, node)

        # Mandatory attributes for derived registers
        attr = {}
        attr['name'] = parser.text(node, 'name', True)
        attr['description'] = parser.text(node, 'description', False)
        attr['address_offset'] = parser.integer(node, 'addressOffset', True)

        # Other attributes
        attr['size'] = parser.integer(node, 'size', False)
        attr['access'] = parser.enum(type.access, node, 'access', False)
        attr['protection'] = parser.enum(type.protection, node, 'protection', False)
        attr['reset_value'] = parser.integer(node, 'resetValue', False)
        attr['reset_mask'] = parser.integer(node, 'resetMask', False)
        self.add_attributes(attr)

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
