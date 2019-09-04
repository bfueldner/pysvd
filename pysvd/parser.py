def Text(value, default=None):
    """Get text from the provided value. If None, default is returned"""

    if value is None:
        return default
    else:
        return value


def Integer(value, default=None):
    """Get integer value from the provided value.
    If None, default is returned
    """

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


def Boolean(value, default=None):
    """Get boolean value from the provided value.
    If None, default is returned
    """

    if value is None:
        return default

    value = value.lower()
    if value == 'false' or value == '0':
        return False
    elif value == 'true' or value == '1':
        return True
    else:
        raise ValueError("Can not convert str '{}' to boolean".format(value))


def Enum(enum, value, default=None):
    """Get enum value from the provided value looking up in EnumClass.
    If None, default is returned
    """
    if value is None:
        return default

    for pair in enum:
        if pair.value == value:
            return pair

    raise KeyError("Value '{}' not contained in enum type".format(value))
