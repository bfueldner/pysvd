
class parent(object):

    def __init__(self):
        self.list = []

class register(object):

    def __init__(self, parent, name, list):
        self.parent = parent
        self.name = name
        self.index = 0

        index = 1
        for dim in list:
            dimname = self.name + dim
            self.instantiate(dimname, index)
            index += 1

    def instantiate(self, name, index):
        print("Name = {}, Index = {}".format(name, index))
        self.parent.list.append(name)


class reg(object):

    @classmethod
    def for_node(cls, path, remove_reserved=False):
        return cls(ET.parse(path), remove_reserved)

    def __init__(self, tree, remove_reserved=False):
        self.remove_reserved = remove_reserved
        self._tree = tree
        self._root = self._tree.getroot()

if __name__ == "__main__":
    my_parent = parent()
    my_register = register(my_parent, "name_", ['A', 'B', 'C', 'D'])

    regx = reg.from_node(node)

    for reg in my_parent.list:
        print(reg)
