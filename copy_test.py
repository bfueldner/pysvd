
class parent(object):

    def __init__(self):
        self.list = []

class register(object):

    def __init__(self, parent, name):
        print("ctor", parent, name)
        self.parent = parent
        self.name = name

#    def instantiate(self, name, index):
#        print("Name = {}, Index = {}".format(name, index))
#        self.parent.list.append(name)

    @classmethod
    def from_node(cls, parent, name, list):
        index = 1
        arr = []
        for dim in list:
            dimname = name + dim
            parent.list.append(register(parent, dimname))
        #    arr.append(register(parent, name))
        #    self.instantiate(dimname, index)
            index += 1
        return arr

class reg(object):
    def __init__(self, tree, remove_reserved=False):
        self.remove_reserved = remove_reserved
        self._tree = tree
        self._root = self._tree.getroot()

    @classmethod
    def copy(cls):
        return cls()

    @classmethod
    def for_node(cls, path, remove_reserved=False):
        return cls(ET.parse(path), remove_reserved)

if __name__ == "__main__":
    my_parent = parent()
    my_register = register.from_node(my_parent, "name_", ['A', 'B', 'C', 'D'])

#    regx = reg.from_node(node)

    for reg in my_parent.list:
        print(reg.name)
