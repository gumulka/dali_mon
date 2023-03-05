class EventType:
    RESERVED = 0
    DEVICE = 1
    DEVICE_INSTANCE = 2
    DEVICE_GROUP = 3
    INSTANCE = 4
    INSTANCE_GROUP = 5


class ForwardFrame24Bit:
    def device_command(self, opcode):
        # see iec 62386-102 11.2
        code_dictionary = {
            0x00: "IDENTIFY DEVICE",
            0x01: "RESET POWER CYCLE SEEN",
            0x10: "RESET",
            0x11: "RESET MEMORY BANK (DTR0)",
            0x14: "SET SHORT ADDRESS (DTR0)",
            0x15: "ENABLE WRITE MEMORY",
            0x16: "ENABLE APPLICATION CONTROLLER",
            0x17: "DISABLE APPLICATION CONTROLLER",
            0x18: "SET OPERATING MODE (DTR0)",
            0x19: "ADD TO DEVICE GROUPS 0-15 (DTR2:DTR1)",
            0x1A: "ADD TO DEVICE GROUPS 16-31 (DTR2:DTR1)",
            0x1B: "REMOVE FROM DEVICE GROUPS 0-15 (DTR2:DTR1)",
            0x1C: "REMOVE FROM DEVICE GROUPS 16-31 (DTR2:DTR1)",
            0x1D: "START QUIESCENT MODE",
            0x1E: "STOP QUIESCENT MODE",
            0x1F: "ENABLE POWER CYCLE NOTIFICATION",
            0x20: "DISABLE POWER CYCLE NOTIFICATION",
            0x21: "SAVE PERSISTENT VARIABLES (DEPRECATED)",
            0x30: "QUERY DEVICE STATUS",
            0x31: "QUERY APPLICTAION CONTROLLER ERROR",
            0x32: "QUERY INPUT DEVICE ERROR",
            0x33: "QUERY MISSING SHORT ADDRESS",
            0x34: "QUERY VERSION NUMBER",
            0x35: "QUERY NUMBER OF INSTANCES",
            0x36: "QUERY CONTENT DTR0",
            0x37: "QUERY CONTENT DTR1",
            0x38: "QUERY CONTENT DTR2",
            0x39: "QUERY RANDOM ADDRESS (H)",
            0x3A: "QUERY RANDOM ADDRESS (M)",
            0x3B: "QUERY RANDOM ADDRESS (L)",
            0x3C: "READ MEMORY LOCATION (DTR1,DTR0)",
            0x3D: "QUERY APPLICATION CONTROL ENABLED",
            0x3E: "QUERY OPERATING MODE",
            0x3F: "QUERY MANUFACTURER SPECIFIC MODE",
            0x40: "QUERY QUIESCENT MODE",
            0x41: "QUERY DEVICE GROUPS 0-7",
            0x42: "QUERY DEVICE GROUPS 8-15",
            0x43: "QUERY DEVICE GROUPS 16-23",
            0x44: "QUERY DEVICE GROUPS 24-41",
            0x45: "QUERY POWER CYCLE NOTIFICATION",
            0x46: "QUERY DEVICE CAPABILITIES",
            0x47: "QUERY EXTENDED VERSION NUMBER (DTR0)",
            0x48: "QUERY RESET STATE",
            0x61: "SET EVENT PRIORITY (DTR0)",
            0x62: "ENABLE INSTANCE",
            0x63: "DISABLE INSTANCE",
            0x64: "SET PRIMARY INSTANCE GROUP (DTR0)",
            0x65: "SET INSTANCE GROUP 1 (DTR0)",
            0x66: "SET INSTANCE GROUP 2 (DTR0)",
            0x67: "SET EVENT SCHEME (DTR0)",
            0x68: "SET EVENT FILTER (DTR2, DTR1, DTR0)",
            0x80: "QUERY INSTANCE TYPE",
            0x81: "QUERY RESOLUTION",
            0x82: "QUERY INSTANCE ERROR",
            0x83: "QUERY INSTANCE STATUS",
            0x84: "QUERY EVENT PRIORITY",
            0x86: "QUERY INSTANCE ENABLED",
            0x88: "QUERY PRIMARY INSTANCE GROUP",
            0x89: "QUERY INSTANCE GROUP 1",
            0x8A: "QUERY INSTANCE GROUP 2",
            0x8B: "QUERY EVENT SCHEME",
            0x8C: "QUERY INPUT VALUE",
            0x8D: "QUERY INPUT VALUE LATCH",
            0x8E: "QUERY FEATURE TYPE",
            0x8F: "QUERY NEXT FEATURE TYPE",
            0x90: "QUERY EVENT FILTER 0-7",
            0x91: "QUERY EVENT FILTER 8-15",
            0x92: "QUERY EVENT FILTER 16-23",
            0x93: "QUERY INSTANCE CONFIGURATION (DTR0)",
            0x94: "QUERY AVAILABLE INSTANCE TYPES",
        }
        return code_dictionary.get(
            opcode,
            f"--- CODE 0x{opcode:02X} = {opcode} UNDEFINED CONTROL DEVICE COMMAND",
        )

    def device_special_command(self, address_byte, instance_byte, opcode_byte):
        # see iec 62386-103 table 22
        if address_byte == 0xC1:
            if instance_byte == 0x00:
                return "TERMINATE"
            elif instance_byte == 0x01:
                return f"INITIALISE (0x{opcode_byte:02X})"
            elif instance_byte == 0x02:
                return "RANDOMISE"
            elif instance_byte == 0x03:
                return "COMPARE"
            elif instance_byte == 0x04:
                return "WITHDRAW"
            elif instance_byte == 0x05:
                return f"SEARCHADDRH (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x06:
                return f"SEARCHADDRM (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x07:
                return f"SEARCHADDRL (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x08:
                return f"PROGRAM SHORT ADDRESS (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x09:
                return f"VERIFY SHORT ADDRESS (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x0A:
                return f"QUERY SHORT ADDRESS"
            elif instance_byte == 0x20:
                return f"WRITE MEMORY LOCATION DTR1, DTR0, (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x21:
                return f"WRITE MEMORY LOCATION - NO REPLY - DTR1, DTR0, (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x30:
                return f"DTR0 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}"
            elif instance_byte == 0x31:
                return f"DTR1 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}"
            elif instance_byte == 0x32:
                return f"DTR2 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}"
            elif instance_byte == 0x33:
                return f"SEND TESTFRAME (0x{opcode_byte:02X}) = {opcode_byte}"
        if address_byte == 0xC5:
            return f"DIRECT WRITE MEMORY (DTR0,0x{instance_byte:02X}) : 0x{opcode_byte:02X}"
        if address_byte == 0xC7:
            return f"DTR1:DTR0 (0x{instance_byte:02X},0x{opcode_byte:02X})"
        if address_byte == 0xC9:
            return f"DTR2:DTR1 (0x{instance_byte:02X},0x{opcode_byte:02X})"
        return f"--- CODE 0x{address_byte:02X} = {address_byte} UNKNOWN CONTROL DEVICE SPECIAL COMMAND"

    def get_event_source_type(self, frame):
        if frame & (1 << 23):
            if frame & (1 << 22):
                if frame & (1 << 15):
                    return EventType.RESERVED
                return EventType.INSTANCE_GROUP
            else:
                if frame & (1 << 15):
                    return EventType.INSTANCE
                else:
                    return EventType.DEVICE_GROUP
        else:
            if frame & (1 << 15):
                return EventType.DEVICE_INSTANCE
            else:
                return EventType.DEVICE
        return EventType.RESERVED

    @staticmethod
    def build_event_source_string(event_type, frame):
        if event_type == EventType.DEVICE:
            short_address = (frame >> 17) & 0x3F
            instance_type = (frame >> 10) & 0x1F
            return f"A{short_address:02X},T{instance_type:02X}"
        elif event_type == EventType.DEVICE_INSTANCE:
            short_address = (frame >> 17) & 0x3F
            instance_number = (frame >> 10) & 0x1F
            return f"A{short_address:02X},I{instance_number:02X}"
        elif event_type == EventType.DEVICE_GROUP:
            device_group = (frame >> 17) & 0x1F
            instance_type = (frame >> 10) & 0x1F
            return f"G{device_group:02X},T{instance_type:02X}"
        elif event_type == EventType.INSTANCE:
            instance_type = (frame >> 17) & 0x1F
            instance_number = (frame >> 10) & 0x1F
            return f"T{instance_type:02X},I{instance_number:02X}"
        elif event_type == EventType.INSTANCE_GROUP:
            device_group = (frame >> 17) & 0x1F
            instance_type = (frame >> 10) & 0x1F
            return f"IG{device_group:02X},T{instance_type:02X}"
        else:
            return ""

    @staticmethod
    def build_power_event_device(frame):
        # see iec 62386-103 9.6.2
        if frame & (1 << 12):
            device_group = (frame >> 7) & 0x1F
            group_result = f"G{device_group:02X} "
        else:
            group_result = ""
        if frame & (1 << 6):
            short_address = frame & 0x3F
            return f"{group_result}A{short_address:02X}"
        else:
            return f"{group_result}".rstrip()

    def __init__(self, frame, address_field_width=10):
        self.address_string = " " * address_field_width
        self.command_string = ""

        address_byte = (frame >> 16) & 0xFF
        instance_byte = (frame >> 8) & 0xFF
        opcode_byte = frame & 0xFF

        # see iec 62386-103 7.2.2.1
        if (frame >> 13) == 0x7F7:
            self.address_string = self.build_power_event_device(frame).ljust(
                address_field_width
            )
            self.command_string = f"POWER CYCLE EVENT"
            return
        if not (address_byte & 0x01):
            self.addressing = self.get_event_source_type(frame)
            if self.addressing == EventType.RESERVED:
                self.address_string = "".ljust(address_field_width)
                self.command_string = "RESERVED EVENT"
            else:
                self.address_string = self.build_event_source_string(
                    self.addressing, frame
                ).ljust(address_field_width)
                self.command_string = f"EVENT DATA 0x{(frame & 0x3FF):03X} = {(frame & 0x3FF)} = {(frame & 0x3FF):012b}b"
            return
        if (address_byte >= 0x00) and (address_byte <= 0x7F):
            short_address = address_byte >> 1
            self.address_string = f"A{short_address:02}".ljust(address_field_width)
            self.command_string = self.device_command(opcode_byte)
            return
        if (address_byte >= 0x80) and (address_byte <= 0xBF):
            group_address = (address_byte >> 1) & 0x0F
            self.address_string = f"G{group_address:02}".ljust(address_field_width)
            self.command_string = self.device_command(opcode_byte)
            return
        if address_byte == 0xFD:
            self.address_string = "BC unadr.".ljust(address_field_width)
            self.command_string = self.device_command(opcode_byte)
        elif address_byte == 0xFF:
            self.address_string = "BC".ljust(address_field_width)
            self.command_string = self.device_command(opcode_byte)
        elif (address_byte >= 0xC1) and (address_byte <= 0xDF):
            self.command_string = self.device_special_command(
                address_byte, instance_byte, opcode_byte
            )
        elif (address_byte >= 0xE1) and (address_byte <= 0xEF):
            self.command_string = "RESERVED"
        elif (address_byte >= 0xF1) and (address_byte <= 0xF7):
            self.command_string = "RESERVED"
        elif (address_byte >= 0xF8) and (address_byte <= 0xFB):
            self.command_string = "RESERVED"
