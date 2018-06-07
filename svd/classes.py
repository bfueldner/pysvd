import re
import copy

import svd.node
import svd.parser

class base(object):
    '''Base class for all SVD elements'''

    def __init__(self, node):
        self.node = node

    def add_attributes(self, attr):
        '''Add not 'None' entries as class attributes'''
        self.__dict__.update( {k: v for k, v in attr.items() if v is not None} )

    @classmethod
    def add_elements(cls, parent, node, name):
        '''Parse node elements and return a list with constucted elements'''
        print("base.add_elements")

        elements = []
        for subnode in node.findall(name):
            elements.append(cls(parent, subnode))
        return elements

    '''Find child with name'''
    def find(self, name):
        return None

class parent(base):
    '''Base class for parents'''

    def __init__(self, parent, node):
        base.__init__(self, node)
        self.parent = parent

class group(parent):
    '''Base class for elements with registerPropertiesGroup'''

    attributes = ['size', 'access', 'protection', 'reset_value', 'reset_mask']
#   elements = ['device', 'peripheral', 'register', 'cluster', 'field', 'sauRegionsConfig', 'addressBlock']

    def __init__(self, parent_, node):
        parent.__init__(self, parent_, node)

    def __getattr__(self, attr):
        # TODO: Also recursive until parent = None!
        if attr in self.attributes and self.parent:
            return self.parent.__getattribute__(attr)
        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, attr))

class derive(group):
    '''Base for deriveable classes'''

#   elements = ['device', 'peripheral', 'register', 'cluster', 'field']

    def __init__(self, parent, node):

        # If derived, search class, copy its attributes and call base constructor
        path = node.get('derivedFrom')
        if path:
            parts = path.split('.')
            print(parts)

            count = len(parts) - 1
            node = parent
            while count:
                node = node.parent
                count -= 1

            print("node_name", node.name)

        #    while issubclass(type(root), parent):
        #        print(type(root), root, base)
        #        root = root.parent

            for name in parts:
                res = node.find(name)
                if res is None:
                    raise KeyError("Can not find path element '{}' of '{}' in node '{}'".format(name, path, node.name))
                node = res

            print("node_name", node.name)
            self = copy.copy(node)
        #    self.__dict__ = dict(node.__dict__)
            self.derived = True
        else:
            self.derived = False

        group.__init__(self, parent, node)

        # TODO Test type on derivedFrom search and support paths! http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_enumeratedValues

class dim(derive):

    def __init__(self, parent, node, name = None, offset = 0):
        derive.__init__(self, parent, node)

        self.name = svd.parser.text(svd.node.element(node, 'name', True))
        self.description = svd.parser.text(svd.node.element(node, 'description'))
        self.dim_name = svd.parser.text(svd.node.element(node, 'dimName'))
        if name is not None:
            self.name %= (name)
            if self.description is not None:
                self.description %= (name)

            if self.dim_name is not None:
                self.dim_name %= (name)

    @classmethod
    def add_elements(cls, parent, node, name):
        '''Parse node elements with respect to dim entries and return a list with constucted elements'''

        elements = []
        for subnode in node.findall(name):
            dim = svd.parser.integer(svd.node.element(subnode, 'dim'))
            if dim is not None:
                dim_increment = svd.parser.integer(svd.node.element(subnode, 'dimIncrement', True))
                dim_index = svd.parser.text(svd.node.element(subnode, 'dimIndex'))
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
                    dim_indices = [dim]

                offset = 0
                for index in dim_indices:
                    elements.append(cls(parent, subnode, index, offset))
                    offset += dim_increment
            else:
                elements.append(cls(parent, subnode))
        return elements
