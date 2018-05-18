#import argparse
#import sys
#import datetime
#import xml.etree.ElementTree as ET

import svd.type

def text(node, tag, mandatory = False, default = None):
    """Get the text for the provided tag from the provided node"""
    try:
        return node.find(tag).text.strip()
    except AttributeError:
        if mandatory:
            raise SyntaxError("Tag '{}.{}' is mandatory, but not present!".format(node.tag, tag))
        return default

def integer(node, tag, mandatory = False, default = None):
    value = text(node, tag, mandatory, default)
    if value == default:
        return default

    value = value.lower()

    # Hexadecimal '0x'
    if value.startswith('0x'):
        return int(value[2:], 16)
    # Binary '0b'
    elif value.startswith('0b'):
        value = value.replace('x', '0')[2:]
        return int(value, 2)
    # Binary '#'
    elif value.startswith('#'):
        value = value.replace('x', '0')[1:]
        return int(value, 2)
    # Decimal
    else:
        return int(value)

def boolean(node, tag, mandatory = False, default = None):
    value = text(node, tag, mandatory, default)
    if value == default:
        return default

    value = value.lower()
    if value == 'false' or value == '0':
        return False
    elif value == 'true' or value == '1':
        return True
    else:
        raise ValueError("Can not convert value '{}' to boolean".format(value))

def enum(enum, node, tag, mandatory = False, default = None):
    value = text(node, tag, False, None)
    if value is None and not mandatory:
        return default

    for pair in enum:
        if pair.value == value:
            return pair

    raise KeyError("Value '{}' not contained in enum type".format(value))



old ='''
class SVDdim(object):

    def __init__(self, parent, node):
        self.parent = parent

        self.dim = _get_int(node, 'dim', True)
        self.dim_increment = _get_int(node, 'dimIncrement', True)
        self.dim_text = _get_text(node, 'dimIndex', False, 0)
        self.dim_name = _get_text(node, 'dimName', False, 0)

#        self.reference = None
#        self.timestamp = Timestamp(self, None)

#        if node is None:
#            return

#        timestamp_node = node.find('timestamp')

#        self.reference = node.get('reference')
#        self.timestamp = Timestamp(self, timestamp_node)

class Parser(object):
    """The SVDParser is responsible for mapping the SVD XML to Python Objects"""

    def __init__(self, path):
        self._tree = ET.parse(path)
        self._root = self._tree.getroot()

        print self._root
        print self._root.tag

        self.test = SVDdim(self, self._root)

class base(object):
    """docstring for ."""

    def __init__(self):
        self.parent = None
    #    super(, self).__init__()
    #    self.arg = arg

    def __getattr__(self, attr):
        print "__getattr__ {}".format(attr)
        return "xxx"

class derived(object):

    def __init__(self):
        base.__init__(self)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description = "SVD to register source file conversion tool.")
    arg_parser.add_argument('--svd', '-x', metavar = 'file', type = str, required = True, help = "SVD file")
#   arg_parser.add_argument('--output', '-o', metavar = 'filename', type = argparse.FileType('w'), required = True, help = "Output filename")
    args = arg_parser.parse_args()

    # Load device description
    tree = Parser(args.svd)
    print tree.test.dim
    print tree.test.dim_increment
    print tree.test.dim_text
    print tree.test.dim_name

    for n in Fib(1000):
        print n

    test = base()
    print test.parent
    print test.irgendwas

#    for person in tree.people:
#        print("{} ({} - {}) {}".format(person.name, person.birth.timestamp.value, person.death.timestamp.value, person.age))
'''
