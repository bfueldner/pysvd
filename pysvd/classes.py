import re
import pysvd


class Base(object):
    """Base class for all SVD elements"""

    def __init__(self, node):
        self.node = node
        self.parent = None

    def add_attributes(self, attr):
        """Add not 'None' entries as class attributes"""
        self.__dict__.update({k: v for k, v in attr.items() if v is not None})

    @classmethod
    def add_elements(cls, parent, elements, node, name):
        """Parse node elements and add them to elements list"""

        for subnode in node.findall(name):
            elements.append(cls(parent, subnode))

    def find(self, name):
        """Find child by name. Has to be overwritten by each node level."""
        return None


class Parent(Base):
    """Base class for parents"""

    def __init__(self, parent, node):
        super().__init__(node)
        self.parent = parent


class Group(Parent):
    """Base class for elements with registerPropertiesGroup"""

    attributes = ['size', 'access', 'protection', 'reset_value', 'reset_mask']
#   elements = ['device', 'peripheral', 'register', 'cluster', 'field', \
#               'sauRegionsConfig', 'addressBlock']

    def __init__(self, parent_, node):
        super().__init__(parent_, node)

    def __getattr__(self, attr):
        if attr in self.attributes:
            parent = self.parent
            while parent is not None:
                try:
                    return parent.__getattribute__(attr)
                except:
                    parent = parent.parent

        raise AttributeError("'{}' object has no attribute '{}'".
                             format(self.__class__.__name__, attr))


class Derive(Group):
    """Base for deriveable classes"""

#   elements = ['device', 'peripheral', 'register', 'cluster', 'field']

    def __init__(self, parent, node):

        # If derived, search class, copy its attributes and call base ctor
        derived_from = pysvd.node.Attribute(node, 'derivedFrom')
        if derived_from is not None:
            parts = derived_from.split('.')
            count = len(parts) - 1
            node = parent
            while count:
                node = node.parent
                count -= 1

            for name in parts:
                res = node.find(name)
                if res is None:
                    raise KeyError("Can not find path element '{}' of path \
                                   '{}' in node '{}'".format(
                                        name, derived_from, node.name))
                node = res

            self.__dict__ = dict(node.__dict__)
            self.derived = True
        else:
            self.derived = False

        super().__init__(parent, node)


class Dim(Derive):

    def __init__(self, parent, node, name=None, offset=0):
        super().__init__(parent, node)

        self.name = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        self.description = pysvd.parser.Text(pysvd.node.Element(node, 'description'))
        self.dim_name = pysvd.parser.Text(pysvd.node.Element(node, 'dimName'))
        if name is not None:
            self.name %= (name)
            if self.description is not None:
                self.description %= (name)

            if self.dim_name is not None:
                self.dim_name %= (name)

    @classmethod
    def add_elements(cls, parent, elements, node, name):
        """Parse node elements with respect to dim entries and return a list with constucted elements"""

        for subnode in node.findall(name):
            dim = pysvd.parser.Integer(pysvd.node.Element(subnode, 'dim'))
            if dim is not None:
                dim_increment = pysvd.parser.Integer(pysvd.node.Element(subnode, 'dimIncrement', True))
                dim_index = pysvd.parser.Text(pysvd.node.Element(subnode, 'dimIndex'))
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
