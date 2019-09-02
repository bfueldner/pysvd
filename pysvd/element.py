import re
import pysvd


# /device
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_device.html
class Device(pysvd.classes.Base):
    """The element <device> provides the outermost frame of the description.

    * Only one <device> section is allowed per file. All other elements are described within this scope.
    * A <device> contains one or more peripherals, but one <cpu> description.
    * Optional elements such as <size>, <access>, or <resetValue> defined on this level represent default values for registers and can be
      refined at lower levels.
    """

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
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_cpu.html
class Cpu(pysvd.classes.Parent):
    """The CPU section describes the processor included in the microcontroller device. This section is mandatory if the SVD file is used to
    generate the device header file.
    """

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


# /device/cpu/sauRegionsConfig
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_cpu.html#elem_sauRegionsConfig
class SauRegionConfig(pysvd.classes.Group):
    """Set the configuration for the Secure Attribution Unit (SAU) when they are preconfigured by HW or Firmware.
    """

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


# /device/cpu/sauRegionsConfig/region
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_cpu.html#elem_region
class SauRegionsConfigRegion(pysvd.classes.Parent):
    """Define the regions of the Secure Attribution Unit (SAU). The protection level is inherited from the attribute
    <protectionWhenDisabled> of the enclosing element sauRegionsConfig.
    """

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
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_peripherals.html
# All peripherals of a device are enclosed within the tag <peripherals>.
#
# Note: This level is skipped for better readability

# /device/peripherals/peripheral
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_peripherals.html#elem_peripheral
class Peripheral(pysvd.classes.Dim):
    """At least one peripheral has to be defined.

    * Each peripheral describes all registers belonging to that peripheral.
    * The address range allocated by a peripheral is defined through one or more address blocks.
    * An address block and register addresses are specified relative to the base address of a peripheral. The address block information can
      be used for constructing a memory map for the device peripherals.

    Starting version 1.3 of the SVD specification, arrays of peripherals can be specified. The single peripheral description gets
    duplicated automatically into an array. The number of array elements is specified by the <dim> element. To define arrays, the <name>
    needs the format myPeripheral[%s]. The tag <dimIncrement> specifies the address offset between two peripherals. To create copies of a
    peripheral using different names, you must use the derivedFrom attribute.
    """

    def __init__(self, parent, node):
        self.register = []
        self.cluster = []

        super().__init__(parent, node)

    def set_offset(self, value):
        self.baseAddress += value

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

            if len(self.register) < 1 and len(self.cluster) < 1:
                raise SyntaxError("At least one element of 'register' or 'cluster' is mandatory in 'registers'")

    def find(self, name):
        """Find register by name."""
        for register in self.register:
            if register.name == name:
                return register
        return None


# /device/peripherals/peripheral/addressBlock
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_peripherals.html#elem_addressBlock
class AddressBlock(pysvd.classes.Group):
    """Specify an address range uniquely mapped to this peripheral. A peripheral must have at least one address block. If a peripheral is
    derived form another peripheral, the <addressBlock> is not mandatory.
    """

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


# /device/peripherals/peripheral/interrupt
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_peripherals.html#elem_interrupt
class Interrupt(pysvd.classes.Parent):
    """A peripheral can have multiple interrupts. This entry allows the debugger to show interrupt names instead of interrupt numbers.
    """

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description'))
        attr['value'] = pysvd.parser.Integer(pysvd.node.Element(node, 'value', True))
        self.add_attributes(attr)


# /device/peripherals/peripheral/registers
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html
# All registers of a peripheral are enclosed between the <registers> opening and closing tags. Clusters define a set of registers. You can
# either use the <cluster> or the <register> element.
#
# Note: This level is skipped for better readability


# /device/pripherals/peripheral/registers/.../cluster
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_cluster
class Cluster(pysvd.classes.Dim):
    """Cluster describes a sequence of neighboring registers within a peripheral. A <cluster> specifies the addressOffset relative to the
    baseAddress of the grouping element. All <register> elements within a <cluster> specify their addressOffset relative to the cluster
    base address (<peripheral.baseAddress> + <cluster.addressOffset>).

    Multiple <register> and <cluster> sections may occur in any order. Since version 1.3 of the specification, the nesting of <cluster>
    elements is supported. Nested clusters express hierarchical structures of registers. It is predominantely targeted at the generation of
    device header files to create a C-data structure within the peripheral structure instead of a flat list of registers. Note, you can
    also specify an array of a cluster using the <dim> element.
    """

    def __init__(self, parent, node):
        self.register = []
        self.cluster = []

        super().__init__(parent, node)

    def set_offset(self, value):
        self.addressOffset += value

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['name'] = pysvd.parser.Text(pysvd.node.Element(node, 'name', True))
        attr['description'] = pysvd.parser.Text(pysvd.node.Element(node, 'description'), self.derived)
        attr['alternateCluster'] = pysvd.parser.Text(pysvd.node.Element(node, 'alternateCluster'))
        attr['headerStructName'] = pysvd.parser.Text(pysvd.node.Element(node, 'headerStructName'))
        attr['addressOffset'] = pysvd.parser.Integer(pysvd.node.Element(node, 'addressOffset', True))

        attr['size'] = pysvd.parser.Integer(pysvd.node.Element(node, 'size'))
        attr['access'] = pysvd.parser.Enum(pysvd.type.access, pysvd.node.Element(node, 'access'))
        attr['protection'] = pysvd.parser.Enum(pysvd.type.protection, pysvd.node.Element(node, 'protection'))
        attr['resetValue'] = pysvd.parser.Integer(pysvd.node.Element(node, 'resetValue'))
        attr['resetMask'] = pysvd.parser.Integer(pysvd.node.Element(node, 'resetMask'))
        self.add_attributes(attr)

        Register.add_elements(self, self.register, node, 'register')
        Cluster.add_elements(self, self.cluster, node, 'cluster')


# /device/peripherals/peripheral/registers/.../register
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_register
class Register(pysvd.classes.Dim):
    """The description of registers is the most essential part of SVD. If the elements <size>, <access>, <resetValue>, and <resetMask>
    have not been specified on a higher level, then these elements are mandatory on register level.

    A register can represent a single value or can be subdivided into individual bit-fields of specific functionality and semantics. From
    a schema perspective, the element <fields> is optional, however, from a specification perspective, <fields> are mandatory when they are
    described in the device documentation.

    You can define register arrays where the single description gets duplicated automatically. The size of the array is specified by the
    <dim> element. Register names get composed by the element <name> and the index-specific string defined in <dimIndex>. The element
    <dimIncrement> specifies the address offset between two registers.
    """

    def __init__(self, parent, node):
        self.field = []

        super().__init__(parent, node)

    def set_offset(self, value):
        self.addressOffset += value

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


# /device/peripherals/peripheral/registers/.../register/.../writeConstraint
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_writeConstraint
class WriteConstraint(pysvd.classes.Parent):
    """Define constraints for writing values to a field. You can choose between three options, which are mutualy exclusive.
    """

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


# /device/peripherals/peripheral/registers/.../register/fields
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_fields
# Grouping element to define bit-field properties of a register.
#
# Note: This level is skipped for better readability


# /device/peripherals/peripheral/registers/.../fields/field
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_field
class Field(pysvd.classes.Dim):
    """All fields of a register are enclosed between the <fields> opening and closing tags.

    A bit-field has a name that is unique within the register. The position and size within the register can be decsribed in two ways:
    * by the combination of the least significant bit's position (lsb) and the most significant bit's position (msb), or
    * the lsb and the bit-width of the field.

    A field may define an enumeratedValue in order to make the display more intuitive to read.
    """

    attributes = ['access']

    def __init__(self, parent, node):
        super().__init__(parent, node)

    def set_offset(self, value):
        self.bitOffset += value

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


# /device/peripherals/peripheral/registers/.../field/enumeratedValues
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_enumeratedValues
class EnumeratedValues(pysvd.classes.Derive):
    """The concept of enumerated values creates a map between unsigned integers and an identifier string. In addition, a description string
    can be associated with each entry in the map.

    0 <-> disabled -> "The clock source clk0 is turned off."
    1 <-> enabled  -> "The clock source clk1 is running."
    2 <-> reserved -> "Reserved values. Do not use."
    3 <-> reserved -> "Reserved values. Do not use."

    This information generates an enum in the device header file. The debugger may use this information to display the identifier string as
    well as the description. Just like symbolic constants making source code more readable, the system view in the debugger becomes more
    instructive. The detailed description can provide reference manual level details within the debugger.
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


# /device/peripherals/peripheral/registers/.../enumeratedValue
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_registers.html#elem_enumeratedValue
class EnumeratedValue(pysvd.classes.Parent):
    """An enumeratedValue defines a map between an unsigned integer and a string.
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


# /device/peripherals/peripheral/.../dimArrayIndex
# http://www.keil.com/pack/doc/cmsis/svd/html/elem_special.html#elem_dimArrayIndex
class DimArrayIndex(pysvd.classes.Parent):
    """This information is used for generating an enum in the device header file. The debugger may use this information to display the
    identifier string as well as the description. Just like symbolic constants making source code more readable, the system view in the
    debugger becomes more instructive.
    """

    def __init__(self, parent, node):
        self.enumeratedValue = []

        super().__init__(parent, node)

    def parse(self, node):
        super().parse(node)

        attr = {}
        attr['headerEnumName'] = pysvd.parser.Text(pysvd.node.Element(node, 'headerEnumName'))
        self.add_attributes(attr)

        for child in node.findall('./enumeratedValue'):
            self.enumeratedValue.append(EnumeratedValue(self, child))

        if len(self.enumeratedValue) < 1:
            raise SyntaxError("At least one element of enumeratedValue is needed in dimArrayIndex '{}'".format(attr['headerEnumName']))
