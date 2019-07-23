import re

import svd.classes
import svd.parser
import svd.type

x = '''
# Base elements

class device(object):
    """The element <device> provides the outermost frame of the description."""

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

        x = """
        node_cpu = node.find('./cpu')
        if node_cpu:
            attr['cpu'] = None

        self.field = []
        for child in node.findall('./peripherals/peripheral'):
            self.field.append(field(self, child))

        attr['peripherals'] = None
        """
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
    """List of field"""

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
'''
