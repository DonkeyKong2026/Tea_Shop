#!/usr/bin/env python3
"""
mcp9808 Temperature Sensor Driver for Python 3.x.x

Revised by: Ran Yang, September 2025
Revised 9/26/2026: address check, MCP9808 class name, negative-limit encoding fix

read_temperature() intentionally returns whole degrees only (Lab 6 Task 3 adds the fraction).

Pin Configuration for Raspberry Pi 4:
- Vdd to GPIO1 (3.3V)
- Gnd to any GPIO ground
- SCL to GPIO3
- SDA to GPIO2
- Alert to a user-defined GPIO pin (can be left floating)
- A0, A1, and A2 define the chip's address. Max 8 chips (0b000 to 0b111) can be used simultaneously.
  Floating all address pins results in address 0b000 = 0x18; A0 tied to 3.3V gives 0x19.
- The LIS3DH accelerometer also uses 0x18. If both are on the bus, tie the LIS3DH SDO
  pin to 3.3V (the LIS3DH moves to 0x19).
"""

import smbus2


class mcp9808:
    DEFAULT_ADDRESS = 0x18
    REG_CONFIG = 0x01
    REG_TEMPERATURE = 0x05
    REG_TCRITICAL = 0x04
    REG_RESOLUTION = 0x08

    def __init__(self, i2c_addr=DEFAULT_ADDRESS):
        self.i2c_addr = i2c_addr
        self.bus = smbus2.SMBus(1)

        # Manufacturer ID register 0x06 must read 0x0054, otherwise another chip answers here
        try:
            manufacturer_id = self._swap_bytes(self.bus.read_word_data(self.i2c_addr, 0x06))
        except OSError:
            raise Exception(f'No device answered at address 0x{i2c_addr:01X}. '
                            'Run i2cdetect -y 1 and check the wiring.')
        if manufacturer_id != 0x0054:
            raise Exception(f'The device at address 0x{i2c_addr:02X} is not an MCP9808. '
                            'Is the LIS3DH also at 0x18? Tie its SDO pin to 3.3V so it moves to 0x19.')

    def configure(self, config_value=0):
        config_value = self._swap_bytes(config_value)
        self.bus.write_word_data(self.i2c_addr, self.REG_CONFIG, config_value)
        read_config = self._swap_bytes(
            self.bus.read_word_data(self.i2c_addr, self.REG_CONFIG))
        print(f'Temperature sensor configured as: {bin(read_config)}')

    def read_temperature(self):
        temphex = self.bus.read_word_data(self.i2c_addr, self.REG_TEMPERATURE)
        # convert from big-endian to little-endian
        temphex = ((temphex & 0x00ff) << 8) + ((temphex & 0xff00) >> 8)
        temphex = temphex & 0x1fff
        sign = (temphex & 0x1000) >> 12
        temphex = temphex & 0xfff
        integer_part = temphex >> 4
        if sign:
            return integer_part - 256
        else:
            return integer_part

    def set_critical_temperature(self, temp_c):
        temp_encoded = self._encode_temperature(temp_c)
        self._write_word(self.REG_TCRITICAL, temp_encoded)

    def set_resolution(self, resolution=0.0625):
        resolution_map = {0.5: 0, 0.25: 1, 0.125: 2, 0.0625: 3}
        self.bus.write_byte_data(
            self.i2c_addr, self.REG_RESOLUTION, resolution_map.get(resolution, 3))

    def _swap_bytes(self, value):
        return ((value & 0xFF) << 8) | ((value & 0xFF00) >> 8)

    def _write_word(self, reg, value):
        """Write a 16-bit word to the specified register."""
        self.bus.write_word_data(self.i2c_addr, reg, self._swap_bytes(value))

    def _encode_temperature(self, temp_c):
        """Encode temperature for writing to registers."""
        if temp_c < 0:
            # brackets matter: without them Python computes x ^ (0x1FFF + 1)
            return ((int(abs(temp_c) * 16) & 0xFFF) ^ 0x1FFF) + 1
        return int(temp_c * 16) & 0xFFF


# The Lab 6 manual imports the class as MCP9808; both names work.
MCP9808 = mcp9808
