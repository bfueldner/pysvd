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

    attributes = ['size', 'access', 'protection', 'resetValue', 'resetMask']
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

        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, attr))


class Derive(Group):
    """Base for deriveable classes"""

#   elements = ['device', 'peripheral', 'register', 'cluster', 'field']

    def __init__(self, parent, node):

        # If derived, search class, copy its attributes and call base ctor
        derivedFrom = pysvd.node.Attribute(node, 'derivedFrom')
        if derivedFrom is not None:
            parts = derivedFrom.split('.')
            count = len(parts) - 1
            object = parent
            while count:
                object = object.parent
                count -= 1

            if object is None:
                raise KeyError("Can not find root element of path '{}' of parent '{}'".format(derivedFrom, parent.name))

            for name in parts:
                res = object.find(name)
                if res is None:
                    raise KeyError("Can not find path element '{}' of path '{}' in object '{}'".format(name, derivedFrom, object.name))
                object = res

            # TODO: Recursive copy dict!
            self.__dict__ = dict(object.__dict__)
            self.derived = True
        else:
            self.derived = False

        super().__init__(parent, node)


class Dim(Derive):

    def __init__(self, parent, node, name=None, offset=0):
        super().__init__(parent, node)

        self.name = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        self.description = pysvd.parser.Text(pysvd.node.Element(node, 'description'))
        self.dimName = pysvd.parser.Text(pysvd.node.Element(node, 'dimName'), self.name)

        # Replace %s with name if not None
        if name is not None:
            name = str(name)
            self.name = self.name.replace('%s', name)
            if self.description is not None:
                self.description = self.description.replace('%s', name)

            if self.dimName is not None:
                self.dimName = self.dimName.replace('%s', name)

    @classmethod
    def add_elements(cls, parent, elements, node, name):
        """Parse node elements with respect to dim entries and return a list with constucted elements"""

        for subnode in node.findall(name):
            dim = pysvd.parser.Integer(pysvd.node.Element(subnode, 'dim'))
            if dim is not None:
                dimIncrement = pysvd.parser.Integer(pysvd.node.Element(subnode, 'dimIncrement', True))
                dimIndex = pysvd.parser.Text(pysvd.node.Element(subnode, 'dimIndex'))
                if dimIndex is not None:
                    if ',' in dimIndex:
                        dimIndices = dimIndex.split(',')
                    elif '-' in dimIndex:
                        match = re.search('([0-9]+)\-([0-9]+)', dimIndex)
                        dimIndices = list(range(int(match.group(1)), int(match.group(2)) + 1))
                    else:
                        raise ValueError("Unexpected value in 'dimIndex': {}".format(dimIndex))

                    if len(dimIndices) != dim:
                        raise AttributeError("'dim' size does not match elements in 'dimIndex' ({} != {})".format(dim, len(dimIndex)))
                else:
                    dimIndices = [dim]

                offset = 0
                for index in dimIndices:
                    elements.append(cls(parent, subnode, index, offset))
                    offset += dimIncrement
            else:
                elements.append(cls(parent, subnode))
