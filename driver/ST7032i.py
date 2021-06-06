from machine import I2C
import time

ST7032_I2C_ADDRESS = 0x3E

class Device:
    """Class for communicating with an I2C device.

    Allows reading and writing 8-bit, 16-bit, and byte array values to
    registers on the device."""

    def __init__(self, address, i2c):
        """Create an instance of the I2C device at the specified address using
        the specified I2C interface object."""
        self._address = address
        self._i2c = i2c

    def writeRaw8(self, value):
        """Write an 8-bit value on the bus (without register)."""
        value = value & 0xFF
        self._i2c.writeto(self._address, value)

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""
        b=bytearray(1)
        b[0]=value & 0xFF
        self._i2c.writeto_mem(self._address, register, b)

    def write16(self, register, value):
        """Write a 16-bit value to the specified register."""
        value = value & 0xFFFF
        b=bytearray(2)
        b[0]= value & 0xFF
        b[1]= (value>>8) & 0xFF
        self.i2c.writeto_mem(self._address, register, value)

    def readRaw8(self):
        """Read an 8-bit value on the bus (without register)."""
        return int.from_bytes(self._i2c.readfrom(self._address, 1),'little') & 0xFF

    def readU8(self, register):
        """Read an unsigned byte from the specified register."""
        return int.from_bytes(
            self._i2c.readfrom_mem(self._address, register, 1),'little') & 0xFF

    def readS8(self, register):
        """Read a signed byte from the specified register."""
        result = self.readU8(register)
        if result > 127:
            result -= 256
        return result

    def readU16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = int.from_bytes(
            self._i2c.readfrom_mem(self._address, register, 2),'little') & 0xFFFF
        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result

    def readS16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = self.readU16(register, little_endian)
        if result > 32767:
            result -= 65536
        return result

    def readU16LE(self, register):
        """Read an unsigned 16-bit value from the specified register, in little
        endian byte order."""
        return self.readU16(register, little_endian=True)

    def readU16BE(self, register):
        """Read an unsigned 16-bit value from the specified register, in big
        endian byte order."""
        return self.readU16(register, little_endian=False)

    def readS16LE(self, register):
        """Read a signed 16-bit value from the specified register, in little
        endian byte order."""
        return self.readS16(register, little_endian=True)

    def readS16BE(self, register):
        """Read a signed 16-bit value from the specified register, in big
        endian byte order."""
        return self.readS16(register, little_endian=False)

class ST7032i:
    def __init__(self, i2c_address=ST7032_I2C_ADDRESS, i2c=None):
        if i2c is None:
            raise ValueError('An I2C object is required.')
        self._device = Device(i2c_address, i2c)
        self.__initialize()

    def __initialize(self):
        self.write_instruction(0x38) # function set: 8 bit, 2 line
        self.write_instruction(0x39) # function set: 8 bit, 2 line, IS=1
        self.write_instruction(0x14) # internal OSC freq
        self.write_instruction(0x70) # contrast set
        self.write_instruction(0x56) # Power/ICON/Constrast
        self.write_instruction(0x6c) # Follower control
        time.sleep(0.2)             # wait time > 200 ms
        self.write_instruction(0x38) # function set: 8 bit, 2 line, IS=0
        self.write_instruction(0x06) # Entry mode set
        self.write_instruction(0x0c) # Display on/off
        self.write_instruction(0x01) # Clear display
        time.sleep(0.01)             # wait time > 1.08 ms
        self.write_instruction(0x02) # return home
        time.sleep(0.01)             # wait time > 1.08 ms

    def return_home(self):
        """ return to home position """
        self.write_instruction(0x02) # return home
        time.sleep(0.01)             # wait time > 1.08 ms

    def reset_display(self):
        """ Clear display and return to home position. """
        self.write_instruction(0x01) # clear display
        time.sleep(0.01)             # wait time > 1.08 ms
        self.return_home()

    def set_contrast(self, contrast):
        """ Set contrast (0 - 15). """
        if contrast < 0:
            contrast = 0
        if contrast > 0x0f:
            contrast = 0x0f
        self.write_instruction(0x39)
        self.write_instruction(0x70 + contrast)

    def set_cursor(self, x, y):
        """ set cursor location (address counter)."""
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        ddram_addr = y * 0x40 + x
        self.write_instruction(0x80 + ddram_addr) # set DDRAM address

    def set_entry_mode(self, increment, shift):
        mode = 0x04
        if (increment):
            mode = mode + 2
        if (shift):
            mode = mode + 1
        self.write_instruction(mode)

    def print(self, str, wait = 0):
        for c in str:
            self.write_data(ord(c))
            if (wait > 0):
                time.sleep(wait)

    def write_instruction(self, data):
        self._device.write8(0x00, data)

    def write_data(self, data):
        self._device.write8(0x40, data)
