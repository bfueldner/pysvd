def text(value, default = None):
    '''Get the text for the provided tag from the provided node'''

    if value is None:
        return default
    else:
        return value

def integer(value, default = None):
    if value is None:
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

def boolean(value, default = None):
    if value is None:
        return default

    value = value.lower()
    if value == 'false' or value == '0':
        return False
    elif value == 'true' or value == '1':
        return True
    else:
        raise ValueError("Can not convert value '{}' to boolean".format(value))

def enum(enum, value, default = None):
    if value is None:
        return default

    for pair in enum:
        if pair.value == value:
            return pair

    raise KeyError("Value '{}' not contained in enum type".format(value))
