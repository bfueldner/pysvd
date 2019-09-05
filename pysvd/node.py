import re


def Element(node, tag, mandatory=False):
    """Get the element text for the provided tag from the provided node"""

    value = node.findtext(tag)
    if value is None:
        if mandatory:
            raise SyntaxError("Element '{}.{}' is mandatory, but not present!".format(node.tag, tag))
        return None
    else:
        value = re.sub(r'\s+', ' ', value)
        return value.strip()


def Attribute(node, tag, mandatory=False):
    """Get the attribute text for the provided tag from the provided node"""

    value = node.get(tag)
    if value is None:
        if mandatory:
            raise SyntaxError("Attribute '{}@{}' is mandatory, but not present!".format(node.tag, tag))
        return None
    else:
        value = re.sub(r'\s+', ' ', value)
        return value.strip()
