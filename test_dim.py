from model import SVDdim

import xml.etree.ElementTree as ET

if __name__ == "__main__":
    node = ET.parse("test_dim.svd").getroot()
    element = SVDdim(None, node)

    print("{}".format(element.dim))
    print("{}".format(element.dim_increment))
    print("{}".format(element.dim_text))
    print("{}".format(element.dim_name))

    for x in element:
        print("{}".format(x))

    for x in element:
        print("{}".format(x))
