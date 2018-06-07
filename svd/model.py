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

# Property group elements

# Deriveable elements

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
