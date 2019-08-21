import re
import pysvd


# /device
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_device.html
class Device(pysvd.classes.Base):
    """The element <device> provides the outermost frame of the description."""

    def __init__(self, node):
        super().__init__(node)

        attr = {}
        attr['schema_version'] = pysvd.parser.Text(pysvd.node.Attribute(node, 'schemaVersion', True))

        attr['vendor'] = pysvd.parser.Text(pysvd.node.Element(node, 'vendor'))
        attr['vendor_id'] = pysvd.parser.Text(pysvd.node.Element(node, 'vendorID'))
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['series'] = pysvd.parser.Text(pysvd.node.Element(node, 'series'))
        attr['version'] = pysvd.parser.Text(pysvd.node.Element(node, 'version', True))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description', True))
        license_text = pysvd.parser.Text(pysvd.node.Element(node, 'licenseText'))
        attr['header_system_filename'] = pysvd.parser.Text(pysvd.node.Element(node, 'headerSystemFilename'))
        attr['header_definitions_prefix'] = pysvd.parser.Text(pysvd.node.Element(node, 'headerDefinitionsPrefix'))
        attr['address_unit_bits'] = pysvd.parser.Integer(pysvd.node.Element(node, 'addressUnitBits', True))
        attr['width'] = pysvd.parser.Integer(pysvd.node.Element(node, 'width', True))

        # property group
        attr['size'] = pysvd.parser.Integer(pysvd.node.Element(node, 'size'), 32)
        attr['access'] = pysvd.parser.Enum(pysvd.type.access, pysvd.node.Element(node, 'access'), pysvd.type.access.read_write)
        attr['protection'] = pysvd.parser.Enum(pysvd.type.protection, pysvd.node.Element(node, 'protection'), pysvd.type.protection.none)
        attr['reset_value'] = pysvd.parser.Integer(pysvd.node.Element(node, 'resetValue'), 0x00000000)
        attr['reset_mask'] = pysvd.parser.Integer(pysvd.node.Element(node, 'resetMask'), 0xFFFFFFFF)

        # Clean up license text from whitespaces
        result = ''
        for line in license_text.splitlines():
            line = line.strip()
            if len(line):
                result += line + '\n'
        attr['license_text'] = result
        self.add_attributes(attr)

        cpu = node.find('cpu')
        if cpu is not None:
            self.cpu = pysvd.element.Cpu(self, cpu)

        peripherals_node = node.find('./peripherals')
        if peripherals_node is None:
            raise SyntaxError("No element 'peripherals' found in 'device'")

        self.peripheral = []
        Peripheral.add_elements(self, self.peripheral, peripherals_node, 'peripheral')

        if len(self.peripheral) < 1:
            raise SyntaxError("At least one element of 'peripheral' is mandatory in 'peripherals'")

    def find(self, name):
        """Find peripheral by name."""
        for peripheral in self.peripheral:
            if peripheral.name == name:
                return peripheral
        return None


# /device/cpu
class Cpu(pysvd.classes.Parent):
    """The CPU section describes the processor included in the microcontroller device."""

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['name'] = pysvd.parser.Enum(pysvd.type.cpuName, pysvd.node.Element(node, 'name', True).replace('+', 'PLUS'))
        attr['revision'] = pysvd.parser.Text(pysvd.node.Element(node, 'revision', True))
        attr['endian'] = pysvd.parser.Enum(pysvd.type.endian, pysvd.node.Element(node, 'endian', True))
        attr['mpu_present'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'mpuPresent', True))
        attr['fpu_present'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'fpuPresent', True))

        attr['fpu_dp'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'fpuDP'))
        attr['icache_present'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'icachePresent'))
        attr['dcache_present'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'dcachePresent'))
        attr['itcm_present'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'itcmPresent'))
        attr['dtcm_present'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'dtcmPresent'))
        attr['vtor_present'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'vtorPresent'), True)

        attr['nvic_prio_bits'] = pysvd.parser.Integer(pysvd.node.Element(node, 'nvicPrioBits', True))
        attr['vendor_systick_config'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'vendorSystickConfig', True))

        attr['device_num_interrupts'] = pysvd.parser.Integer(pysvd.node.Element(node, 'deviceNumInterrupts'))
        attr['sau_num_regions'] = pysvd.parser.Integer(pysvd.node.Element(node, 'sauNumRegions'))
        self.add_attributes(attr)

        sau_regions_config_node = node.find('sauRegionsConfig')
        if sau_regions_config_node is not None:
            self.sau_regions_config = SauRegionConfig(self, sau_regions_config_node)


class SauRegionConfig(pysvd.classes.Group):
    """Set the configuration for the Secure Attribution Unit (SAU) when they are preconfigured by HW or Firmware."""

    attributes = ['protection']

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['enabled'] = pysvd.parser.Boolean(pysvd.node.Attribute(node, 'enabled'))
        attr['protection'] = pysvd.parser.Enum(pysvd.type.protection, pysvd.node.Element(node, 'protectionWhenDisabled'))
        self.add_attributes(attr)

        self.region = []
        for sau_regions_config_region_node in node.findall('region'):
            self.region.append(SauRegionsConfigRegion(self, sau_regions_config_region_node))


class SauRegionsConfigRegion(pysvd.classes.Parent):
    """Define the regions of the Secure Attribution Unit (SAU)"""

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['enabled'] = pysvd.parser.Boolean(pysvd.node.Attribute(node, 'enabled'), True)
        attr['name'] = pysvd.parser.Text(pysvd.node.Attribute(node, 'name'))

        attr['base'] = pysvd.parser.Integer(pysvd.node.Element(node, 'base', True))
        attr['limit'] = pysvd.parser.Integer(pysvd.node.Element(node, 'limit', True))
        attr['access'] = pysvd.parser.Enum(pysvd.type.sauAccess, pysvd.node.Element(node, 'access', True))
        self.add_attributes(attr)


# /device/peripherals
class Peripherals(pysvd.classes.Parent):
    """All peripherals of a device are enclosed within the tag <peripherals>."""

    def __init__(self, parent, node):
        super().__init__(parent, node)


class Peripheral(pysvd.classes.Dim):
    """At least one peripheral has to be defined."""

    def __init__(self, parent, node, name=None, offset=0):
        super().__init__(parent, node, name, offset)

        attr = {}
        attr['version'] = pysvd.parser.Text(pysvd.node.Element(node, 'version'))
        attr['alternate_peripheral'] = pysvd.parser.Text(pysvd.node.Element(node, 'alternatePeripheral'))
        attr['group_name'] = pysvd.parser.Text(pysvd.node.Element(node, 'groupName'))
        attr['prepend_to_name'] = pysvd.parser.Text(pysvd.node.Element(node, 'prependToName'))
        attr['append_to_name'] = pysvd.parser.Text(pysvd.node.Element(node, 'appendToName'))
        attr['header_struct_name'] = pysvd.parser.Text(pysvd.node.Element(node, 'headerStructName'))
        attr['disable_condition'] = pysvd.parser.Text(pysvd.node.Element(node, 'disableCondition'))
        attr['base_address'] = pysvd.parser.Integer(pysvd.node.Element(node, 'baseAddress', True))
        self.add_attributes(attr)

        address_block_node = node.find('./addressBlock')
        if address_block_node is not None:
            self.address_block = AddressBlock(self, address_block_node)

        interrupt_node = node.find('./interrupt')
        if interrupt_node is not None:
            self.interrupt = Interrupt(self, interrupt_node)

        self.register = []
        self.cluster = []
        registers_node = node.find('./registers')
        if registers_node is not None:
            Register.add_elements(self, self.register, registers_node, 'register')
            Cluster.add_elements(self, self.cluster, registers_node, 'cluster')

            if len(self.register) < 1:
                raise SyntaxError("At least one element of 'register' is mandatory in 'registers'")

    def find(self, name):
        """Find register by name."""
        for register in self.register:
            if register.name == name:
                return register
        return None


class AddressBlock(pysvd.classes.Group):
    """Specify an address range uniquely mapped to this peripheral"""

    attributes = ['protection']

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['offset'] = pysvd.parser.Integer(pysvd.node.Element(node, 'offset', True))
        attr['size'] = pysvd.parser.Integer(pysvd.node.Element(node, 'size', True))
        attr['usage'] = pysvd.parser.Enum(pysvd.type.usage, pysvd.node.Element(node, 'usage', True))
        attr['protection'] = pysvd.parser.Enum(pysvd.type.protection, pysvd.node.Element(node, 'protection'))
        self.add_attributes(attr)


class Interrupt(pysvd.classes.Parent):
    """A peripheral can have multiple interrupts"""

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description'))
        attr['value'] = pysvd.parser.Integer(pysvd.node.Element(node, 'value', True))
        self.add_attributes(attr)

# /device/peripherals/peripheral/registers element

# /device/peripherals/registers


class Registers(pysvd.classes.Parent):
    """All registers of a peripheral are enclosed between the <registers> opening and closing tags. Clusters define a
    set of registers. You can either use the <cluster> or the <register> element.
    """

    def __init__(self, parent, node):
        super().__init__(parent, node)


class Cluster(pysvd.classes.Dim):

    def __init__(self, parent, node, name=None, offset=0):
        super().__init__(parent, node, name, offset)


class Register(pysvd.classes.Dim):

    def __init__(self, parent, node, name=None, offset=0):
        super().__init__(parent, node, name, offset)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['display_name'] = pysvd.parser.Text(pysvd.node.Element(node, 'displayName'))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description'))
        attr['alternate_group'] = pysvd.parser.Text(pysvd.node.Element(node, 'alternateGroup'))
        attr['alternate_register'] = pysvd.parser.Text(pysvd.node.Element(node, 'alternateRegister'))
        attr['address_offset'] = pysvd.parser.Integer(pysvd.node.Element(node, 'addressOffset', True))

        attr['size'] = pysvd.parser.Integer(pysvd.node.Element(node, 'size'))
        attr['access'] = pysvd.parser.Enum(pysvd.type.access, pysvd.node.Element(node, 'access'))
        attr['protection'] = pysvd.parser.Enum(pysvd.type.protection, pysvd.node.Element(node, 'protection'))
        attr['reset_value'] = pysvd.parser.Integer(pysvd.node.Element(node, 'resetValue'))
        attr['reset_mask'] = pysvd.parser.Integer(pysvd.node.Element(node, 'resetMask'))

        attr['data_type'] = pysvd.parser.Enum(pysvd.type.dataType, pysvd.node.Element(node, 'dataType'))
        attr['modified_write_values'] = pysvd.parser.Enum(
            pysvd.type.modifiedWriteValues, pysvd.node.Element(node, 'modifiedWriteValues'), pysvd.type.modifiedWriteValues.modify)
        attr['read_action'] = pysvd.parser.Enum(pysvd.type.readAction, pysvd.node.Element(node, 'readAction'))
        self.add_attributes(attr)

        write_constraint_node = node.find('./writeConstraint')
        if write_constraint_node is not None:
            self.write_constraint = WriteConstraint(self, write_constraint_node)

        self.field = []
        fields_node = node.find('./fields')
        if fields_node is not None:
            Field.add_elements(self, self.field, fields_node, 'field')

            if len(self.field) < 1:
                raise SyntaxError("At least one element of 'field' is mandatory in 'fields'")

    def find(self, name):
        """Find field by name."""
        for field in self.field:
            if field.name == name:
                return field
        return None


class WriteConstraint(pysvd.classes.Parent):
    """Define constraints for writing values to a field. You can choose between three options, which are mutualy exclusive."""

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        write_as_read = pysvd.node.Element(node, 'writeAsRead')
        use_enumerated_values = pysvd.node.Element(node, 'useEnumeratedValues')
        range_node = node.find("./range")
        if write_as_read is not None:
            attr['write_as_read'] = pysvd.parser.Boolean(write_as_read)
        elif use_enumerated_values is not None:
            attr['use_enumerated_values'] = pysvd.parser.Boolean(use_enumerated_values)
        else:
            range_minimum = None
            range_maximum = None
            if range_node is not None:
                range_minimum = pysvd.node.Element(range_node, 'minimum')
                range_maximum = pysvd.node.Element(range_node, 'maximum')

            if range_minimum is None or range_maximum is None:
                raise SyntaxError("Either 'writeAsRead', 'useEnumeratedValues' or 'range' is mandatory in 'writeConstraint'")

            attr['range_minimum'] = pysvd.parser.Integer(range_minimum)
            attr['range_maximum'] = pysvd.parser.Integer(range_maximum)

        self.add_attributes(attr)


class Fields(pysvd.classes.Parent):
    """Grouping element to define bit-field properties of a register."""

    def __init__(self, parent, node):
        super().__init__(parent, node)


class Field(pysvd.classes.Dim):
    """All fields of a register are enclosed between the <fields> opening and closing tags."""

    attributes = ['access']

    def __init__(self, parent, node, name=None, offset=0):
        super().__init__(parent, node, name, offset)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description'))

        # bitRangeOffsetWidthStyle
        bit_offset = pysvd.parser.Integer(pysvd.node.Element(node, 'bitOffset'))
        bit_width = pysvd.parser.Integer(pysvd.node.Element(node, 'bitWidth'))
        if bit_offset is not None:
            # If bitWidth is not set, default is 1
            bit_width = 1 if bit_width is None else bit_width
        else:
            # bitRangeLsbMsbStyle
            lsb = pysvd.parser.Integer(pysvd.node.Element(node, 'lsb'))
            msb = pysvd.parser.Integer(pysvd.node.Element(node, 'msb'))
            if lsb is None or msb is None:
                bit_range = pysvd.parser.Text(pysvd.node.Element(node, 'bitRange'))
                if bit_range is None:
                    raise ValueError("Field '{}' has no valid bit-range".format(attr['name']))

                match = re.search('\[([0-9]+):([0-9]+)\]', bit_range)
                lsb = int(match.group(2))
                msb = int(match.group(1))

            bit_offset = lsb
            bit_width = (msb - lsb) + 1

        attr['bit_offset'] = bit_offset
        attr['bit_width'] = bit_width

        attr['access'] = pysvd.parser.Enum(pysvd.type.access, pysvd.node.Element(node, 'access'))
        attr['modified_write_values'] = pysvd.parser.Enum(
            pysvd.type.modifiedWriteValues, pysvd.node.Element(node, 'modifiedWriteValues'), pysvd.type.modifiedWriteValues.modify)
        attr['read_action'] = pysvd.parser.Enum(pysvd.type.readAction, pysvd.node.Element(node, 'readAction'))
        self.add_attributes(attr)

        write_constraint_node = node.find('./writeConstraint')
        if write_constraint_node is not None:
            self.write_constraint = WriteConstraint(self, write_constraint_node)

        enumerated_values_node = node.find('./enumerated_values')
        if enumerated_values_node is not None:
            self.enumerated_values = EnumeratedValues(self, enumerated_values_node)


class EnumeratedValues(pysvd.classes.Parent):
    """The concept of enumerated values creates a map between unsigned integers
    and an identifier string. In addition, a description string can be
    associated with each entry in the map.
    """

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name'))
        attr['header_enum_name'] = pysvd.parser.Text(pysvd.node.Element(node, 'headerEnumName'))
        attr['usage'] = pysvd.parser.Enum(pysvd.type.enumUsage, pysvd.node.Element(node, 'usage'), pysvd.type.enumUsage.read_write)
        self.add_attributes(attr)

        self.enumerated_value = []
        for child in node.findall('./enumeratedValue'):
            self.enumerated_value.append(EnumeratedValue(self, child))

        if len(self.enumerated_value) < 1:
            raise SyntaxError("At least one element of enumeratedValue is needed in enumeratedValues '{}'".format(attr['name']))


class EnumeratedValue(pysvd.classes.Parent):
    """An enumeratedValue defines a map between an unsigned integer and
    a string.
    """

    def __init__(self, parent, node):
        super().__init__(parent, node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name'))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description'))
        attr['value'] = pysvd.parser.Integer(pysvd.node.Element(node, 'value'))
        attr['is_default'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'isDefault'))
        if attr['value'] is None and attr['is_default'] is None:
            raise SyntaxError("Either 'value' or 'isDefault' is mandatory in enumeratedValue '{}'".format(attr['name']))
        self.add_attributes(attr)
