import sys
import string
import xml.etree.ElementTree as ET

class child(object):

    def __init__(self, parent, node):
        self.parent = parent
        self.name = node.find('name').text

    @classmethod
    def add_elements(cls, parent, node, name):
        print("child.add_elements")

        elements = []
        for subnode in node.findall(name):
            elements.append(cls(parent, subnode))
        return elements

class dimchild(child):

    def __init__(self, parent, node, suffix = None):
        child.__init__(self, parent, node)
        if suffix is not None:
            self.name += suffix

    @classmethod
    def add_elements(cls, parent, node, name):
        print("dimchild.add_elements")

        elements = []
        for subnode in node.findall(name):
            dim = subnode.find('dim')
            if dim is not None:
                num = int(dim.text)
                for i in range(num):
                    elements.append(cls(parent, subnode, str(i)))
            else:
                elements.append(cls(parent, subnode))
        return elements

class root(object):

    def __init__(self, node):
        self.children = dimchild.add_elements(self, node, './child')

if __name__ == "__main__":
    xml = '''
    <root>
        <child>
            <name>UART</name>
        </child>
        <child>
            <name>GPIO_</name>
            <dim>3</dim>
        </child>
        <child>
            <name>ADC</name>
        </child>
        <child>
            <name>SPI_</name>
            <dim>2</dim>
        </child>
    </root>'''

    node = ET.fromstring(xml)
    test = root(node)
    for child in test.children:
        print("Child {}".format(child.name))
