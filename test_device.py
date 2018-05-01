from model import SVDdim
from model import base
from model import test1
from model import test2

import xml.etree.ElementTree as ET

if __name__ == "__main__":
    t1 = test1(None)
    t2 = test2(t1)

#    s = str("abc")
#   print("test {}".format(s.abc))

    print("name {}".format(t1.name))
#    print("value {}".format(t1.value))

    print("name {}".format(t2.name))
    print("value {}".format(t2.value))
