def element(node, tag, mandatory = False):
    '''Get the element text for the provided tag from the provided node'''

    value = node.findtext(tag) #.strip()
    if value is None:
        if mandatory:
            raise SyntaxError("Element '{}.{}' is mandatory, but not present!".format(node.tag, tag))
        return None
    else:
        return value.strip()

def attribute(node, tag, mandatory = False):
    '''Get the attribute text for the provided tag from the provided node'''

    value = node.get(tag)
    if value is None:
        if mandatory:
            raise SyntaxError("Attribute '{}@{}' is mandatory, but not present!".format(node.tag, tag))
        return None
    else:
        return value.strip()
