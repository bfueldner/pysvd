import copy

def clone(obj):
    print("clone", obj, obj.node)
    return type(obj).clone(obj)

class cpy(object):

    def __init__(self):
        pass

    @classmethod
    def ceate(cls, node):
        # Copy from original object
        res = copy.copy(obj)

        # Parse and add specific attributes
        res.parse(node)

class test1(object):

    def __init__(self, node):
        self.name = "test1"
        self.node = node

    @classmethod
    def clone(cls, inst):
        return cls(inst.node)

#Clonen in Basisklasse aufrufen, aber
#Ableitung muss clone funktion implementieren. Sollte die globale Funktion ersetzen.

if __name__ == "__main__":
    node = "knoten"

    t1 = test1(node)
    t1.extra = '123'
    t2 = clone(t1)
    t3 = copy.copy(t1)
    print(t1, t2, t3)
    print(type(t1), type(t2), type(t3))
    print(t1.__dict__, t2.__dict__, t3.__dict__)
