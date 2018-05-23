import copy

class base(object):
    '''Base class for all SVD elements'''

    def __init__(self):
        pass

#    @classmethod
#    def create(cls):
#        return cls()

    '''Add attributes, that are not 'None' to class'''
    def add_attributes(self, attr):
        '''Add not 'None' entries as class attributes'''
        self.__dict__.update( {k: v for k, v in attr.items() if v is not None} )

    '''Find child with name'''
    def find(self, name):
        return None

class parent(base):
    '''Base class for parents'''

    def __init__(self, parent):
        self.parent = parent

#    @classmethod
#    def create(cls, parent):
#        return cls(parent)

class group(parent):
    '''Base class for elements with registerPropertiesGroup'''

    attributes = ['size', 'access', 'protection', 'reset_value', 'reset_mask']
#   elements = ['device', 'peripheral', 'register', 'cluster', 'field', 'sauRegionsConfig', 'addressBlock']

    def __init__(self, parent_):
        parent.__init__(self, parent_)

#    @classmethod
#    def create(cls, parent):
#        return cls(parent)

    def __getattr__(self, attr):
        # TODO: Also recursive until parent = None!
        if attr in self.attributes and self.parent:
            return self.parent.__getattribute__(attr)
        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, attr))

class derive(group):
    '''Base for deriveable classes'''

#   elements = ['device', 'peripheral', 'register', 'cluster', 'field']

    def __init__(self, parent_, node):
        print("DEBUG")

        # If derived, search class, copy its attributes and call base constructor
        path = node.get('derivedFrom')
        if path:
            parts = path.split('.')
            print(parts)

            count = len(parts) - 1
            node = parent_
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

        group.__init__(self, parent)

        # TODO Test type on derivedFrom search and support paths! http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_enumeratedValues
