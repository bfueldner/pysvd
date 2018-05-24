#import argparse
#import sys
#import datetime
#import xml.etree.ElementTree as ET
import re

import svd.classes
import svd.parser
import svd.type





x = """
class dim(derive):
    '''Base for dimable elements'''

    def __init__(self, parent, node):

        try:
            dim = parser.integer(node, 'dim', True)
            dim_increment = parser.integer(node, 'dimIncrement', True)
            dim_index = parser.text(node, 'dimIndex', False)
            dim_name = parser.text(node, 'dimName', False)
            if dim_index is not None:
                if ',' in dim_index:
                    dim_indices = dim_index.split(',')
                elif '-' in dim_index:
                    match = re.search('([0-9]+)\-([0-9]+)', dim_index)
                    dim_indices = list(range(int(match.group(1)), int(match.group(2)) + 1))
                else:
                    raise ValueError("Unexpected value in 'dim_index': {}".format(dim_index))

                if len(dim_indices) != dim:
                    raise AttributeError("'dim' size does not match elements in 'dim_index' ({} != {})".format(dim, len(dim_index)))
            else:
                dim_indices = dim
        except:
            print("Not dimable")

    @classmethod
    def from_node(cls, parent, list):
        for name in list:
            parent.append(cls(parent, name))


# Base elements


class device(object):
    '''The element <device> provides the outermost frame of the description.'''

    def __init__(self, node):

        attr = {}
        attr['vendor'] = parser.text(node, 'vendor', False)
        attr['vendor_id'] = parser.text(node, 'vendorID', False)
        attr['name'] = parser.text(node, 'name', True)
        attr['series'] = parser.text(node, 'series', False)
        attr['version'] = parser.text(node, 'version', True)
        attr['description'] = parser.text(node, 'description', True)
        attr['license_text'] = parser.text(node, 'licenseText', False)
        attr['header_system_filename'] = parser.text(node, 'headerSystemFilename', False)
        attr['header_definitions_prefix'] = parser.text(node, 'headerDefinitionsPrefix', False)
        attr['address_unit_bits'] = parser.integer(node, 'addressUnitBits', True)
        attr['width'] = parser.integer(node, 'width', True)

        # property group
        attr['size'] = parser.integer(node, 'size', False, 32)
        attr['access'] = parser.enum(type.access, node, 'access', False, type.access.read_write)
        attr['protection'] = parser.enum(type.protection, node, 'protection', False, type.protection.none)
        attr['reset_value'] = parser.integer(node, 'resetValue', False, 0x00000000)
        attr['reset_mask'] = parser.integer(node, 'resetMask', False, 0xFFFFFFFF)

        x = '''
        node_cpu = node.find('./cpu')
        if node_cpu:
            attr['cpu'] = None

        self.field = []
        for child in node.findall('./peripherals/peripheral'):
            self.field.append(field(self, child))

        attr['peripherals'] = None
        '''
        self.add_attributes(attr)

        cpu.parse(self, node.find('./cpu'))
        for child in node.findall('./peripherals/peripheral'):
            peripheral.parse(self, child)

    @classmethod
    def parse(cls, node):
        return cls(node)

class enumerated_value(base):
    '''An enumeratedValue defines a map between an unsigned integer and a string.'''

    def __init__(self, parent, node):
        if not (isinstance(parent, enumerated_values) or isinstance(parent, dim_array_index)):
            raise TypeError("Only parent 'enumerated_values' and 'dim_array_index' allowed")
        base.__init__(self, parent)

        attr = {}
        attr['name'] = parser.text(node, 'name', False)
        attr['description'] = parser.text(node, 'description', False)
        attr['value'] = parser.integer(node, 'value', False)
        attr['is_default'] = parser.boolean(node, 'isDefault', False)
        if attr['value'] is None and attr['is_default'] is None:
            raise SyntaxError("Either 'value' or 'isDefault' is mandatory in enumeratedValue '{}'".format(attr['name']))
        self.add_attributes(attr)











# Property group elements




# Deriveable elements
class enumerated_values(derive):
    '''The concept of enumerated values creates a map between unsigned integers and an identifier string. In addition, a description string can be associated with each entry in the map.'''

    def __init__(self, parent, node):
        if not isinstance(parent, field):
            raise TypeError("Only parent 'field' allowed")
        derive.__init__(self, parent, node)

        attr = {}
        attr['name'] = parser.text(node, 'name', False)
        attr['header_enum_name'] = parser.text(node, 'headerEnumName', False)
        attr['usage'] = parser.enum(type.enum_usage, node, 'usage', False, type.enum_usage.read_write)
        self.add_attributes(attr)

        self.enumerated_value = []
        for child in node.findall('./enumeratedValue'):
            self.enumerated_value.append(enumerated_value(self, child))


class field(derive):

    attributes = ['access']

    def __init__(self, parent, node):
        derive.__init__(self, parent, node)

        attr = {}
        attr['name'] = parser.text(node, 'name', True)
        attr['description'] = parser.text(node, 'description', False)

        # bitRangeOffsetWidthStyle
        bit_offset = parser.integer(node, 'bitOffset', False)
        bit_width = parser.integer(node, 'bitWidth', False)
        if bit_offset:
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
        if node:
            self.enumerated_values = enumerated_values(self, node)

class fields(base):
    '''List of field'''

    def __init__(self, parent, node):
        base.__init__(self, parent)

        self.field = []
        for child in node.findall('./field'):
            self.field.append(field(self, child))

class register(dim):

    def __init__(self, parent, node):
        dim.__init__(self, parent, node)

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

    @classmethod
    def parse(cls, parent, node):
        pass

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

    @classmethod
    def parse(cls, parent, node):
        pass


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
"""
