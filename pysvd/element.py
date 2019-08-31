import re
import pysvd


# /device
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_device.html
class Device(pysvd.classes.Base):
    """The element <device> provides the outermost frame of the description."""

    def __init__(self, node):
        self.peripheral = []

        super().__init__(node)

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['schemaVersion'] = pysvd.parser.Text(pysvd.node.Attribute(node, 'schemaVersion', True))

        attr['vendor'] = pysvd.parser.Text(pysvd.node.Element(node, 'vendor'))
        attr['vendorID'] = pysvd.parser.Text(pysvd.node.Element(node, 'vendorID'))
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['series'] = pysvd.parser.Text(pysvd.node.Element(node, 'series'))
        attr['version'] = pysvd.parser.Text(pysvd.node.Element(node, 'version', True))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description', True))
        license_text = pysvd.parser.Text(pysvd.node.Element(node, 'licenseText'))
        attr['headerSystemFilename'] = pysvd.parser.Text(pysvd.node.Element(node, 'headerSystemFilename'))
        attr['headerDefinitionsPrefix'] = pysvd.parser.Text(pysvd.node.Element(node, 'headerDefinitionsPrefix'))
        attr['addressUnitBits'] = pysvd.parser.Integer(pysvd.node.Element(node, 'addressUnitBits', True))
        attr['width'] = pysvd.parser.Integer(pysvd.node.Element(node, 'width', True))

        # property group
        attr['size'] = pysvd.parser.Integer(pysvd.node.Element(node, 'size'), 32)
        attr['access'] = pysvd.parser.Enum(pysvd.type.access, pysvd.node.Element(node, 'access'), pysvd.type.access.read_write)
        attr['protection'] = pysvd.parser.Enum(pysvd.type.protection, pysvd.node.Element(node, 'protection'), pysvd.type.protection.none)
        attr['resetValue'] = pysvd.parser.Integer(pysvd.node.Element(node, 'resetValue'), 0x00000000)
        attr['resetMask'] = pysvd.parser.Integer(pysvd.node.Element(node, 'resetMask'), 0xFFFFFFFF)

        # Clean up license text from whitespaces
        result = ''
        for line in license_text.splitlines():
            line = line.strip()
            if len(line):
                result += line + '\n'
        attr['licenseText'] = result
        self.add_attributes(attr)

        cpu = node.find('cpu')
        if cpu is not None:
            self.cpu = pysvd.element.Cpu(self, cpu)

        peripherals_node = node.find('./peripherals')
        if peripherals_node is None:
            raise SyntaxError("No element 'peripherals' found in 'device'")

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

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['name'] = pysvd.parser.Enum(pysvd.type.cpuName, pysvd.node.Element(node, 'name', True).replace('+', 'PLUS'))
        attr['revision'] = pysvd.parser.Text(pysvd.node.Element(node, 'revision', True))
        attr['endian'] = pysvd.parser.Enum(pysvd.type.endian, pysvd.node.Element(node, 'endian', True))
        attr['mpuPresent'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'mpuPresent', True))
        attr['fpuPresent'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'fpuPresent', True))

        attr['fpuDP'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'fpuDP'))
        attr['icachePresent'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'icachePresent'))
        attr['dcachePresent'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'dcachePresent'))
        attr['itcmPresent'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'itcmPresent'))
        attr['dtcmPresent'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'dtcmPresent'))
        attr['vtorPresent'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'vtorPresent'), True)

        attr['nvicPrioBits'] = pysvd.parser.Integer(pysvd.node.Element(node, 'nvicPrioBits', True))
        attr['vendorSystickConfig'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'vendorSystickConfig', True))

        attr['deviceNumInterrupts'] = pysvd.parser.Integer(pysvd.node.Element(node, 'deviceNumInterrupts'))
        attr['sauNumRegions'] = pysvd.parser.Integer(pysvd.node.Element(node, 'sauNumRegions'))
        self.add_attributes(attr)

        sau_regions_config_node = node.find('./sauRegionsConfig')
        if sau_regions_config_node is not None:
            self.sauRegionsConfig = SauRegionConfig(self, sau_regions_config_node)


class SauRegionConfig(pysvd.classes.Group):
    """Set the configuration for the Secure Attribution Unit (SAU) when they are preconfigured by HW or Firmware."""

    attributes = ['protection']

    def __init__(self, parent, node):
        self.region = []

        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['enabled'] = pysvd.parser.Boolean(pysvd.node.Attribute(node, 'enabled'))
        attr['protection'] = pysvd.parser.Enum(pysvd.type.protection, pysvd.node.Element(node, 'protectionWhenDisabled'))
        self.add_attributes(attr)

        for sau_regions_config_region_node in node.findall('region'):
            self.region.append(SauRegionsConfigRegion(self, sau_regions_config_region_node))


class SauRegionsConfigRegion(pysvd.classes.Parent):
    """Define the regions of the Secure Attribution Unit (SAU)"""

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

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

    def __init__(self, parent, node):
        self.register = []
        self.cluster = []

        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['version'] = pysvd.parser.Text(pysvd.node.Element(node, 'version'))
        attr['alternatePeripheral'] = pysvd.parser.Text(pysvd.node.Element(node, 'alternatePeripheral'))
        attr['groupName'] = pysvd.parser.Text(pysvd.node.Element(node, 'groupName'))
        attr['prependToName'] = pysvd.parser.Text(pysvd.node.Element(node, 'prependToName'))
        attr['appendToName'] = pysvd.parser.Text(pysvd.node.Element(node, 'appendToName'))
        attr['headerStructName'] = pysvd.parser.Text(pysvd.node.Element(node, 'headerStructName'))
        attr['disableDondition'] = pysvd.parser.Text(pysvd.node.Element(node, 'disableCondition'))
        attr['baseAddress'] = pysvd.parser.Integer(pysvd.node.Element(node, 'baseAddress', True))
        self.add_attributes(attr)

        address_block_node = node.find('./addressBlock')
        if address_block_node is not None:
            self.addressBlock = AddressBlock(self, address_block_node)

        interrupt_node = node.find('./interrupt')
        if interrupt_node is not None:
            self.interrupt = Interrupt(self, interrupt_node)

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

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['offset'] = pysvd.parser.Integer(pysvd.node.Element(node, 'offset', True))
        attr['size'] = pysvd.parser.Integer(pysvd.node.Element(node, 'size', True))
        attr['usage'] = pysvd.parser.Enum(pysvd.type.addressBlockUsage, pysvd.node.Element(node, 'usage', True))
        attr['protection'] = pysvd.parser.Enum(pysvd.type.protection, pysvd.node.Element(node, 'protection'))
        self.add_attributes(attr)


class Interrupt(pysvd.classes.Parent):
    """A peripheral can have multiple interrupts"""

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

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

    def parse(self, node):
        super().parse(node)


class Register(pysvd.classes.Dim):

    def __init__(self, parent, node):
        self.field = []

        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['displayName'] = pysvd.parser.Text(pysvd.node.Element(node, 'displayName'))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description'), self.derived)
        attr['alternateGroup'] = pysvd.parser.Text(pysvd.node.Element(node, 'alternateGroup'))
        attr['alternateRegister'] = pysvd.parser.Text(pysvd.node.Element(node, 'alternateRegister'))
        attr['addressOffset'] = pysvd.parser.Integer(pysvd.node.Element(node, 'addressOffset', True))

        attr['size'] = pysvd.parser.Integer(pysvd.node.Element(node, 'size'))
        attr['access'] = pysvd.parser.Enum(pysvd.type.access, pysvd.node.Element(node, 'access'))
        attr['protection'] = pysvd.parser.Enum(pysvd.type.protection, pysvd.node.Element(node, 'protection'))
        attr['resetValue'] = pysvd.parser.Integer(pysvd.node.Element(node, 'resetValue'))
        attr['resetMask'] = pysvd.parser.Integer(pysvd.node.Element(node, 'resetMask'))

        attr['dataType'] = pysvd.parser.Enum(pysvd.type.dataType, pysvd.node.Element(node, 'dataType'))
        attr['modifiedWriteValues'] = pysvd.parser.Enum(
            pysvd.type.modifiedWriteValues, pysvd.node.Element(node, 'modifiedWriteValues'), pysvd.type.modifiedWriteValues.modify)
        attr['readAction'] = pysvd.parser.Enum(pysvd.type.readAction, pysvd.node.Element(node, 'readAction'))
        self.add_attributes(attr)

        write_constraint_node = node.find('./writeConstraint')
        if write_constraint_node is not None:
            self.writeConstraint = WriteConstraint(self, write_constraint_node)

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

    def parse(self, node):
        super().parse(node)

        attr = {}
        writeAsRead = pysvd.node.Element(node, 'writeAsRead')
        useEnumeratedValues = pysvd.node.Element(node, 'useEnumeratedValues')
        range_node = node.find("./range")
        if writeAsRead is not None:
            attr['writeAsRead'] = pysvd.parser.Boolean(writeAsRead)
        elif useEnumeratedValues is not None:
            attr['useEnumeratedValues'] = pysvd.parser.Boolean(useEnumeratedValues)
        else:
            rangeMinimum = None
            rangeMaximum = None
            if range_node is not None:
                rangeMinimum = pysvd.node.Element(range_node, 'minimum')
                rangeMaximum = pysvd.node.Element(range_node, 'maximum')

            if rangeMinimum is None or rangeMaximum is None:
                raise SyntaxError("Either 'writeAsRead', 'useEnumeratedValues' or 'range' is mandatory in 'writeConstraint'")

            attr['rangeMinimum'] = pysvd.parser.Integer(rangeMinimum)
            attr['rangeMaximum'] = pysvd.parser.Integer(rangeMaximum)

        self.add_attributes(attr)


class Fields(pysvd.classes.Parent):
    """Grouping element to define bit-field properties of a register."""

    def __init__(self, parent, node):
        super().__init__(parent, node)


class Field(pysvd.classes.Dim):
    """All fields of a register are enclosed between the <fields> opening and closing tags."""

    attributes = ['access']

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description', self.derived))

        # bitRangeOffsetWidthStyle
        bitOffset = pysvd.parser.Integer(pysvd.node.Element(node, 'bitOffset'))
        bitWidth = pysvd.parser.Integer(pysvd.node.Element(node, 'bitWidth'))
        if bitOffset is not None:
            # If bitWidth is not set, default is 1
            bitWidth = 1 if bitWidth is None else bitWidth
        else:
            # bitRangeLsbMsbStyle
            lsb = pysvd.parser.Integer(pysvd.node.Element(node, 'lsb'))
            msb = pysvd.parser.Integer(pysvd.node.Element(node, 'msb'))
            if lsb is None or msb is None:
                bitRange = pysvd.parser.Text(pysvd.node.Element(node, 'bitRange'))
                if bitRange is None:
                    raise ValueError("Field '{}' has no valid bit-range".format(attr['name']))

                match = re.search('\[([0-9]+):([0-9]+)\]', bitRange)
                lsb = int(match.group(2))
                msb = int(match.group(1))

            bitOffset = lsb
            bitWidth = (msb - lsb) + 1

        attr['bitOffset'] = bitOffset
        attr['bitWidth'] = bitWidth

        attr['access'] = pysvd.parser.Enum(pysvd.type.access, pysvd.node.Element(node, 'access'))
        attr['modifiedWriteValues'] = pysvd.parser.Enum(
            pysvd.type.modifiedWriteValues, pysvd.node.Element(node, 'modifiedWriteValues'), pysvd.type.modifiedWriteValues.modify)
        attr['readAction'] = pysvd.parser.Enum(pysvd.type.readAction, pysvd.node.Element(node, 'readAction'))
        self.add_attributes(attr)

        write_constraint_node = node.find('./writeConstraint')
        if write_constraint_node is not None:
            self.writeConstraint = WriteConstraint(self, write_constraint_node)

        enumerated_values_node = node.find('./enumeratedValues')
        if enumerated_values_node is not None:
            self.enumeratedValues = EnumeratedValues(self, enumerated_values_node)


class EnumeratedValues(pysvd.classes.Derive):
    """The concept of enumerated values creates a map between unsigned integers
    and an identifier string. In addition, a description string can be
    associated with each entry in the map.
    """

    def __init__(self, parent, node):
        self.enumeratedValue = []

        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name'))
        attr['headerEnumName'] = pysvd.parser.Text(pysvd.node.Element(node, 'headerEnumName'))
        attr['usage'] = pysvd.parser.Enum(pysvd.type.enumUsage, pysvd.node.Element(node, 'usage'), pysvd.type.enumUsage.read_write)
        self.add_attributes(attr)

        for child in node.findall('./enumeratedValue'):
            self.enumeratedValue.append(EnumeratedValue(self, child))

        if len(self.enumeratedValue) < 1:
            raise SyntaxError("At least one element of enumeratedValue is needed in enumeratedValues '{}'".format(attr['name']))


class EnumeratedValue(pysvd.classes.Parent):
    """An enumeratedValue defines a map between an unsigned integer and
    a string.
    """

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name'))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description'))
        attr['value'] = pysvd.parser.Integer(pysvd.node.Element(node, 'value'))
        attr['isDefault'] = pysvd.parser.Boolean(pysvd.node.Element(node, 'isDefault'))
        if attr['value'] is None and attr['isDefault'] is None:
            raise SyntaxError("Either 'value' or 'isDefault' is mandatory in enumeratedValue '{}'".format(attr['name']))

        self.add_attributes(attr)
