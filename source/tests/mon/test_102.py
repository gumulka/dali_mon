import pytest
import DALI

ADDRESS_WIDTH = 14


def test_backframe():
    for data in range(0x100):
        decoded_command = DALI.Decode(8, data, DALI.DeviceType.NONE)
        target_command = " " * ADDRESS_WIDTH + f"DATA 0x{data:02X}"
        assert decoded_command.cmd()[: len(target_command)] == target_command


def test_broadcast_dapc():
    # refer to iec62386 102 7.2.1
    for level in range(0x100):
        decoded_command = DALI.Decode(16, (0xFE00 + level), DALI.DeviceType.NONE)
        target_command = "BC GEAR".ljust(ADDRESS_WIDTH) + f"DAPC {level}"
        assert decoded_command.cmd() == target_command


def test_short_address_dapc():
    # refer to iec62386 102 7.2.1
    for short_address in range(0x40):
        for level in range(0x100):
            decoded_command = DALI.Decode(
                16, ((short_address << 9) + level), DALI.DeviceType.NONE
            )
            target_command = (
                f"G{short_address:02}".ljust(ADDRESS_WIDTH) + f"DAPC {level}"
            )
            assert decoded_command.cmd() == target_command


def test_group_address_dapc():
    # refer to iec62386 102 7.2.1
    for group_address in range(0x10):
        for level in range(0x100):
            decoded_command = DALI.Decode(
                16, (0x8000 + (group_address << 9) + level), DALI.DeviceType.NONE
            )
            target_command = (
                f"GG{group_address:02}".ljust(ADDRESS_WIDTH) + f"DAPC {level}"
            )
            assert decoded_command.cmd() == target_command


def test_reserved():
    # refer to iec62386 102 7.2.1
    target_command = " " * ADDRESS_WIDTH + "RESERVED"
    for code in range(0xCC00, 0xFC00):
        decoded_command = DALI.Decode(16, code, DALI.DeviceType.NONE)
        assert decoded_command.cmd() == target_command


# refer to iec62386 102 Table 15
@pytest.mark.parametrize(
    "name,opcode",
    [
        ("OFF", 0x00),
        ("UP", 0x01),
        ("DOWN", 0x02),
        ("STEP UP", 0x03),
        ("STEP DOWN", 0x04),
        ("RECALL MAX LEVEL", 0x05),
        ("RECALL MIN LEVEL", 0x06),
        ("STEP DOWN AND OFF", 0x07),
        ("ON AND STEP UP", 0x08),
        ("ENABLE DAPC SEQUENCE", 0x09),
        ("GO TO LAST ACTIVE LEVEL", 0x0A),
        ("CONTINOUS UP", 0x0B),
        ("CONTINOUS DOWN", 0x0C),
        ("RESET", 0x20),
        ("STORE ACTUAL LEVEL IN DTR0", 0x21),
        ("SAVE PERSISTENT VARIABLES (DEPRECATED)", 0x22),
        ("SET OPERATING MODE (DTR0)", 0x23),
        ("RESET MEMORY BANK (DTR0)", 0x24),
        ("IDENTIFY DEVICE", 0x25),
        ("SET MAX LEVEL (DTR0)", 0x2A),
        ("SET MIN LEVEL (DTR0)", 0x2B),
        ("SET SYSTEM FAILURE LEVEL (DTR0)", 0x2C),
        ("SET POWER ON LEVEL (DTR0)", 0x2D),
        ("SET FADE TIME (DTR0)", 0x2E),
        ("SET FADE RATE (DTR0)", 0x2F),
        ("SET EXTENDED FADE TIME (DTR0)", 0x30),
    ],
)
def test_command(name, opcode):
    # broadcast
    decoded_command = DALI.Decode(16, (0xFF00 + opcode), DALI.DeviceType.NONE)
    target_command = "BC GEAR".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    # broadcast unadressed
    decoded_command = DALI.Decode(16, (0xFD00 + opcode), DALI.DeviceType.NONE)
    target_command = "BC GEAR UN".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    # short address
    for short_address in range(0x40):
        decoded_command = DALI.Decode(
            16, (0x0100 + (short_address << 9) + opcode), DALI.DeviceType.NONE
        )
        target_command = f"G{short_address:02}".ljust(ADDRESS_WIDTH) + name
        assert decoded_command.cmd() == target_command
    # group address
    for group_address in range(0x10):
        decoded_command = DALI.Decode(
            16, (0x8100 + (group_address << 9) + opcode), DALI.DeviceType.NONE
        )
        target_command = f"GG{group_address:02}".ljust(ADDRESS_WIDTH) + name
        assert decoded_command.cmd() == target_command


@pytest.mark.parametrize(
    "name,opcode",
    [
        ("GO TO SCENE", 0x10),
        ("SET SCENE (DTR0)", 0x40),
        ("REMOVE FROM SCENE", 0x50),
        ("ADD TO GROUP", 0x60),
        ("REMOVE FROM GROUP", 0x70),
        ("QUERY SCENE LEVEL", 0xB0),
    ],
)
def test_count_command(name, opcode):
    for counter in range(0x10):
        scene_opcode = opcode + counter
        scene_name = name + f" {counter}"
        test_command(scene_name, scene_opcode)


@pytest.mark.parametrize(
    "opcode",
    [
        0x0D,
        0x0E,
        0x0F,
        0x26,
        0x27,
        0x28,
        0x29,
        0x31,
        0x32,
        0x33,
        0x34,
        0x35,
        0x36,
        0x37,
        0x38,
        0x39,
        0x3A,
        0x3B,
        0x3C,
        0x3D,
        0x3E,
        0x3F,
        0x82,
        0x83,
        0x84,
        0x85,
        0x86,
        0x87,
        0x88,
        0x89,
        0x8A,
        0x8B,
        0x8C,
        0x8D,
        0x8E,
        0x8F,
        0xAB,
        0xAC,
        0xAD,
        0xAE,
        0xAF,
        0xC6,
        0xC7,
        0xC8,
        0xC9,
        0xCA,
        0xCB,
    ],
)
def test_undefined_codes(opcode):
    # broadcast
    decoded_command = DALI.Decode(16, (0xFF00 + opcode), DALI.DeviceType.NONE)
    target_command = "BC GEAR".ljust(ADDRESS_WIDTH) + "---"
    assert decoded_command.cmd()[: len(target_command)] == target_command
    # broadcast unadressed
    decoded_command = DALI.Decode(16, (0xFD00 + opcode), DALI.DeviceType.NONE)
    target_command = "BC GEAR UN".ljust(ADDRESS_WIDTH) + "---"
    assert decoded_command.cmd()[: len(target_command)] == target_command
    # short address
    for short_address in range(0x40):
        decoded_command = DALI.Decode(
            16, (0x0100 + (short_address << 9) + opcode), DALI.DeviceType.NONE
        )
        target_command = f"G{short_address:02}".ljust(ADDRESS_WIDTH) + "---"
        assert decoded_command.cmd()[: len(target_command)] == target_command
    # group address
    for group_address in range(0x10):
        decoded_command = DALI.Decode(
            16, (0x8100 + (group_address << 9) + opcode), DALI.DeviceType.NONE
        )
        target_command = f"GG{group_address:02}".ljust(ADDRESS_WIDTH) + "---"
        assert decoded_command.cmd()[: len(target_command)] == target_command


@pytest.mark.parametrize(
    "name,address_byte",
    [
        ("TERMINATE", 0xA1),
        ("RANDOMISE", 0xA7),
        ("COMPARE", 0xA9),
        ("WITHDRAW", 0xAB),
        ("PING", 0xAD),
        ("QUERY SHORT ADDRESS", 0xBB),
    ],
)
def test_simple_special_command(name, address_byte):
    # valid opcode byte
    decoded_command = DALI.Decode(16, (address_byte << 8), DALI.DeviceType.NONE)
    target_command = " " * ADDRESS_WIDTH + name
    assert decoded_command.cmd() == target_command
    # invalid opcode byte
    for opcode_byte in range(1, 0x100):
        decoded_command = DALI.Decode(
            16, ((address_byte << 8) + opcode_byte), DALI.DeviceType.NONE
        )
        target_command = " " * ADDRESS_WIDTH + "---"
        assert decoded_command.cmd()[: len(target_command)] == target_command


def test_initialise_short_address():
    for short_address in range(0x40):
        frame_data = 0xA500 + (short_address << 1) + 1
        decoded_command = DALI.Decode(16, frame_data, DALI.DeviceType.NONE)
        target_command = " " * ADDRESS_WIDTH + f"INITIALISE (G{short_address:02})"
        assert decoded_command.cmd() == target_command


@pytest.mark.parametrize(
    "data,target_command",
    [
        (0xA5FF, "INITIALISE (UNADDRESSED)"),
        (0xA500, "INITIALISE (ALL)"),
        (0xA550, "INITIALISE (NONE) - 0x50"),
    ],
)
def test_initialise_special_cases(data, target_command):
    decoded_command = DALI.Decode(16, data, DALI.DeviceType.NONE)
    assert decoded_command.cmd() == " " * ADDRESS_WIDTH + target_command
