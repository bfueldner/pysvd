import svd.type

def text(node, tag, mandatory = False, default = None):
    """Get the text for the provided tag from the provided node"""
    try:
        return node.find(tag).text.strip()
    except AttributeError:
        if mandatory:
            raise SyntaxError("Tag '{}.{}' is mandatory, but not present!".format(node.tag, tag))
        return default

def integer(node, tag, mandatory = False, default = None):
    value = text(node, tag, mandatory, default)
    if value == default:
        return default

    value = value.lower()

    # Hexadecimal '0x'
    if value.startswith('0x'):
        return int(value[2:], 16)
    # Binary '0b'
    elif value.startswith('0b'):
        value = value.replace('x', '0')[2:]
        return int(value, 2)
    # Binary '#'
    elif value.startswith('#'):
        value = value.replace('x', '0')[1:]
        return int(value, 2)
    # Decimal
    else:
        return int(value)

def boolean(node, tag, mandatory = False, default = None):
    value = text(node, tag, mandatory, default)
    if value == default:
        return default

    value = value.lower()
    if value == 'false' or value == '0':
        return False
    elif value == 'true' or value == '1':
        return True
    else:
        raise ValueError("Can not convert value '{}' to boolean".format(value))

def enum(enum, node, tag, mandatory = False, default = None):
    value = text(node, tag, mandatory, default)
    if value == default:
        return default

    for pair in enum:
        if pair.value == value:
            return pair

    raise KeyError("Value '{}' not contained in enum type".format(value))
