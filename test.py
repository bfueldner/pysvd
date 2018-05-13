import string
import xml.etree.ElementTree as ET

from model import device

class base(object):

    def __init__(self):
        pass

    def append(self, item):
        pass

class parent1(object):

    def __init__(self):
        self.words = []

    def append(self, item):
        self.words.append(item)

class parent2(object):

    def __init__(self):
        self.numbers = []

    def append(self, item):
        self.numbers.append(item)

class child(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    @classmethod
    def from_node(cls, parent, list):
        for name in list:
            parent.append(cls(parent, name))

if __name__ == "__main__":
    par1 = parent1()
    child.from_node(par1, ['abc', 'def', 'ghi'])

    for word in par1.words:
        print(word.name)

    par2 = parent2()
    child.from_node(par2, ['123', '456', '789'])

    for num in par2.numbers:
        print(num.name)

    node = ET.parse("res/cortex-m3.svd").getroot()
    dev = device.parse(node)
    
    print("vendor", dev.vendor)
    print("vendorID", dev.vendor_id)
    print("name", dev.name)
    print("series", dev.series)
    print("version", dev.version)
    print("description", dev.description)
    print("licenseText", dev.license_text)
    if hasattr(dev, 'header_system_filename'):
        print("headerSystemFilename", dev.header_system_filename)
    if hasattr(dev, 'header_definitions_prefix'):
        print("headerDefinitionsPrefix", dev.header_definitions_prefix)
    print("addressUnitBits", dev.address_unit_bits)
    print("width", dev.width)

    print("size", dev.size)
    print("access", dev.access)
    print("protection", dev.protection)
    print("resetValue", hex(dev.reset_value))
    print("resetMask", hex(dev.reset_mask))
