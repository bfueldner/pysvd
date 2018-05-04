from enum import Enum

class access(Enum):
    read_only = 'read-only'
    write_only = 'write-only'
    read_write = 'read-write'
    write_once = 'writeOnce'
    read_write_once = 'read-writeOnce'

class protection(Enum):
    secure = 's'
    non_secure = 'n'
    privileged = 'p'


old = '''
cpuNameType = [
    'CM0',
    'CM0PLUS',
    'CM0+',
    'CM1',
    'SC000',
    'CM23',
    'CM3',
    'CM33',
    'SC300',
    'CM4',
    'CM7',
    'CA5',
    'CA7',
    'CA8',
    'CA9',
    'CA15',
    'CA17',
    'CA53',
    'CA57',
    'CA72',
    'other',
]

endianType = [
    'little',
    'big',
    'selectable',
    'other',
]

usageType = [
    'registers',
    'buffer',
    'reserved'
]


class sauAccessType(Enum):
    callable_ = 'c'
    non_secure = 'n'

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




def _get_enum(node, tag, enum, mandatory = False, default = None):
    text_value = _get_text(node, tag, mandatory, default)
    if text_value is None and not mandatory:
        return default

    if text_value in enum:
        return text_value
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

'''
