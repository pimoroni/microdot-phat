from sys import exit, version_info

try:
    import smbus
except ImportError:
    if version_info[0] < 3:
        exit("This library requires python-smbus\nInstall with: sudo apt-get install python-smbus")
    elif version_info[0] == 3:
        exit("This library requires python3-smbus\nInstall with: sudo apt-get install python3-smbus")


ADDR = 0x61
MODE = 0b00011000
OPTS = 0b00001110 # 1110 = 35mA, 0000 = 40mA

CMD_BRIGHTNESS = 0x19
CMD_MODE = 0x00
CMD_UPDATE = 0x0C
CMD_OPTIONS = 0x0D

CMD_MATRIX_1 = 0x01
CMD_MATRIX_2 = 0x0E

MATRIX_1 = 0
MATRIX_2 = 1

class NanoMatrix:
    '''        
    _BUF_MATRIX_1 = [ # Green
#Col   1 2 3 4 5
    0b00000000, # Row 1
    0b00000000, # Row 2
    0b00000000, # Row 3
    0b00000000, # Row 4
    0b00000000, # Row 5
    0b00000000, # Row 6
    0b10000000, # Row 7, bit 8 =  decimal place
    0b00000000
]

    _BUF_MATRIX_2 = [ # Red
#Row 8 7 6 5 4 3 2 1
    0b01111111, # Col 1, bottom to top
    0b01111111, # Col 2
    0b01111111, # Col 3
    0b01111111, # Col 4
    0b01111111, # Col 5
    0b00000000,
    0b00000000,
    0b01000000  # bit 7, decimal place
]

    _BUF_MATRIX_1 = [0] * 8
    _BUF_MATRIX_2 = [0] * 8
'''

    def __init__(self, address=ADDR):
        self.address = address
        self._brightness = 127

        self.bus = smbus.SMBus(1)

        self.bus.write_byte_data(self.address, CMD_MODE, MODE)
        self.bus.write_byte_data(self.address, CMD_OPTIONS, OPTS)
        self.bus.write_byte_data(self.address, CMD_BRIGHTNESS, self._brightness)

        self._BUF_MATRIX_1 = [0] * 8
        self._BUF_MATRIX_2 = [0] * 8

    def set_brightness(self, brightness):
        self._brightness = int(brightness * 127)
        if self._brightness > 127: self._brightness = 127

        self.bus.write_byte_data(self.address, CMD_BRIGHTNESS, self._brightness)

    def set_decimal(self, m, c):

        if m == MATRIX_1:
           if c == 1:
               self._BUF_MATRIX_1[6] |= 0b10000000    
           else:
               self._BUF_MATRIX_1[6] &= 0b01111111

        elif m == MATRIX_2:

           if c == 1:
               self._BUF_MATRIX_2[7] |= 0b01000000
           else:
               self._BUF_MATRIX_2[7] &= 0b10111111

        #self.update()

    def set(self, m, data):
        for y in range(7):
            self.set_row(m, y, data[y])

    def set_row(self, m, r, data):
        for x in range(5):
            self.set_pixel(m, x, r, (data & (1 << (4-x))) > 0)

    def set_col(self, m, c, data):
        for y in range(7):
            self.set_pixel(m, c, y, (data & (1 << y)) > 0)

    def set_pixel(self, m, x, y, c):

        if m == MATRIX_1:
            if c == 1:
                self._BUF_MATRIX_1[y] |= (0b1 << x)
            else:
                self._BUF_MATRIX_1[y] &= ~(0b1 << x)
        elif m == MATRIX_2:
            if c == 1:
                self._BUF_MATRIX_2[x] |= (0b1 << y)
            else:
                self._BUF_MATRIX_2[x] &= ~(0b1 << y)

        #self.update()

    def clear(self, m):
        if m == MATRIX_1:
            self._BUF_MATRIX_1 = [0] * 8
        elif m == MATRIX_2:
            self._BUF_MATRIX_2 = [0] * 8

        self.update()

    def update(self):
        for x in range(10):
            try:
                self.bus.write_i2c_block_data(self.address, CMD_MATRIX_1, self._BUF_MATRIX_1)
                self.bus.write_i2c_block_data(self.address, CMD_MATRIX_2, self._BUF_MATRIX_2)

                self.bus.write_byte_data(self.address, CMD_UPDATE, 0x01)
                break
            except IOError:
                print("IO Error")


if __name__ == "__main__":
    import time

    m1 = NanoMatrix(address=0x63)
    m2 = NanoMatrix(address=0x62)
    m3 = NanoMatrix(address=0x61)

    def clear_matrix(n,m):
        for y in range(7):
            for x in range(5):
                n.set_pixel(m, x, y, 0)
                n.update()
                time.sleep(0.01)
        n.set_decimal(m, 0)
        n.update()
        time.sleep(0.05)

    def fill_matrix(n,m):
        for y in range(7):
            for x in range(5):
                n.set_pixel(m, x, y, 1)
                n.update()
                time.sleep(0.05)
        n.set_decimal(m, 1)
        n.update()
        time.sleep(0.05)

    while True:
        for n in [m1,m2,m3]:
            fill_matrix(n,MATRIX_2)
            fill_matrix(n,MATRIX_1)
        time.sleep(0.1)
        for n in [m1,m2,m3]:
            clear_matrix(n,MATRIX_2)
            clear_matrix(n,MATRIX_1)
        time.sleep(0.1)
