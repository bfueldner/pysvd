import argparse
import sys
import datetime
import xml.etree.ElementTree as ET

def _get_text(node, tag, mandatory = False, default = None):
    """Get the text for the provided tag from the provided node"""
    try:
        return node.find(tag).text
    except AttributeError:
        if mandatory:
            raise Exception("Tag '{}.{}' is mandatory, but not present!".format(node.tag, tag))
        return default


def _get_int(node, tag, mandatory = False, default = None):
    text_value = _get_text(node, tag, mandatory, default)
    try:
        text_value = text_value.strip().lower()

        # Hexadecimal
        if text_value.startswith('0x'):
            return int(text_value[2:], 16)
        # Binary
        elif text_value.startswith('0b'):
            text_value = text_value.replace('x', '0')[2:]
            return int(text_value, 2)
        # Binary (Freeescale special)
        elif text_value.startswith('#'):
            # TODO(posborne): Deal with strange #1xx case better
            #
            # Freescale will sometimes provide values that look like this:
            #   #1xx
            # In this case, there are a number of values which all mean the
            # same thing as the field is a "don't care".  For now, we just
            # replace those bits with zeros.
            text_value = text_value.replace('x', '0')[1:]
            is_bin = all(x in '01' for x in text_value)
            return int(text_value, 2) if is_bin else int(text_value)  # binary
        # Bool true
        elif text_value.startswith('true'):
            return 1
        # Bool false
        elif text_value.startswith('false'):
            return 0
        # Decimal
        else:
            return int(text_value)
    except:
        if mandatory:
            raise Exception("Tag '{}.{}' is mandatory, but not present!".format(node.tag, tag))
    return None

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
