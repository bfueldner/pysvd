from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    a_b = 'auto-type'

class protectionStringType(Enum):
    secure = 's'
    non_secure = 'n'
    privileged = 'p'

class sauAccessType(Enum):
    callable_ = 'c'
    non_secure = 'n'

class accessType(Enum):
    read_only = 'read-only'
    write_only = 'write-only'
    read_write = 'read-write'
    write_once = 'writeOnce'
    read_write_once = 'read-writeOnce'

class modifiedWriteValuesType(Enum):
    one_to_clear = 'oneToClear'
    one_to_set = 'oneToSet'
    one_to_toggle = 'oneToToggle'
    zero_to_clear = 'zeroToClear'
    zero_to_set = 'zeroToSet'
    zero_to_toggle = 'zeroToToggle'
    clear = 'clear'
    set = 'set'
    modify = 'modify'

class readActionType(Enum):
    clear = 'clear'
    set = 'set'
    modify = 'modify'
    modify_external = 'modifyExternal'

class enumUsageType(Enum):
    read = 'read'
    write = 'write'
    read_write = 'read-write'


def _get_text(node, tag, mandatory = False, default = None):
    """Get the text for the provided tag from the provided node"""
    try:
        return node.find(tag).text
    except AttributeError:
        if mandatory:
            raise Exception("Tag '{}.{}' is mandatory, but not present!".format(node.tag, tag))
        return default

def _get_int(node, tag, mandatory = False, default = None):
    text_value = _get_text(node, tag, mandatory, default)
    try:
        text_value = text_value.strip().lower()

        # Hexadecimal
        if text_value.startswith('0x'):
            return int(text_value[2:], 16)
        # Binary
        elif text_value.startswith('0b'):
            text_value = text_value.replace('x', '0')[2:]
            return int(text_value, 2)
        # Binary (Freeescale special)
        elif text_value.startswith('#'):
            # TODO(posborne): Deal with strange #1xx case better
            #
            # Freescale will sometimes provide values that look like this:
            #   #1xx
            # In this case, there are a number of values which all mean the
            # same thing as the field is a "don't care".  For now, we just
            # replace those bits with zeros.
            text_value = text_value.replace('x', '0')[1:]
            is_bin = all(x in '01' for x in text_value)
            return int(text_value, 2) if is_bin else int(text_value)  # binary
        # Bool true
        elif text_value.startswith('true'):
            return 1
        # Bool false
        elif text_value.startswith('false'):
            return 0
        # Decimal
        else:
            return int(text_value)
    except:
        if mandatory:
            raise Exception("Tag '{}.{}' is mandatory, but not present!".format(node.tag, tag))
    return None

def _get_enum(node, tag, enum, mandatory = False, default = None):
    text_value = _get_text(node, tag, mandatory, default)
    if text_value is None and not mandatory:
        return default

    if text_value in enum:
        return text_value
    raise Exception("Value not allowed in enum type")

def _get_new_enum(enum, node, tag, mandatory = False, default = None):
    text_value = _get_text(node, tag, mandatory, default)
    if text_value is None and not mandatory:
        return default

    for pair in enum:
        if pair.value == text_value:
            return pair

    raise Exception("Value not allowed in enum type")

def _get_boolean(node, tag, mandatory = False, default = None):
    int_value = _get_int(node, tag, mandatory, default)
    if int_value == 0:
        return False
    elif int_value == 1:
        return True
    else:
        raise Exception("Value is no boolean type")

def scaled_non_negative_integer(node, tag, mandatory = False, default = None):
    return _get_int(node, tag, mandatory, default)

def access_type(node, tag, mandatory = False, default = None):
    return _get_new_enum(accessType, node, tag, mandatory, default)

if __name__ == "__main__":
    print(Color)

    for col in Color:
        print(col.name, col.value)
