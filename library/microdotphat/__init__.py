import atexit
import math
import time

try:
    import numpy
except ImportError:
    exit("This library requires the numpy module\nInstall with: sudo pip install numpy")

from .font import font, tinynumbers
from .matrix import NanoMatrix


n1 = NanoMatrix(address=0x63)
n2 = NanoMatrix(address=0x62)
n3 = NanoMatrix(address=0x61)

mat = [(n1, 1), (n1, 0), (n2, 1), (n2, 0), (n3, 1), (n3, 0)]

WIDTH = 45
HEIGHT = 7

buf = numpy.zeros((HEIGHT,WIDTH))
decimal = [0] * 6

scroll_x = 0
scroll_y = 0

_clear_on_exit = True
_rotate180 = False

def _exit():
    if _clear_on_exit:
        clear()
        show()

atexit.register(_exit)

def clear():
    """Clear the buffer"""

    global buf, decimal
    decimal = [0] * 6
    buf.fill(0)

def fill(c):
    """Fill the buffer either lit or unlit

    @param c Colour that should be filled onto the display: 1=lit or 0=unlit"""

    global buf
    buf.fill(c)

def set_clear_on_exit(value):
    """Set whether the display should be cleared on exit

    @param value Whether the display should be cleared on exit: True/False"""

    global _clear_on_exit
    _clear_on_exit = (value == True)

def set_rotate180(value):
    """Set whether the display should be rotated 180 degrees

    @param value Whether the display should be rotated 180 degrees: True/False"""

    global _rotate180
    _rotate180 = (value == True)

def set_col(x, col):
    """Set a whole column of the buffer

    Only useful when not scrolling vertically

    @param x Specify which column to set
    @param col An 8-bit integer, the 7 least significant bits correspond to each row"""

    for y in range(7):
        set_pixel(x, y, (col & (1 << y)) > 0)

def set_pixel(x, y, c):
    """Set the state of a single pixel in the buffer

    If the pixel falls outside the current buffer size, it will be grown automatically

    @param x The x position of the pixel to set
    @param y The y position of the pixel to set
    @param c The colour to set: 1=lit or 0=unlit"""

    global buf
    try:
        buf[y][x] = c
    except IndexError:
        if y >= buf.shape[0]:
            buf = numpy.pad(buf, ((0,y - buf.shape[0] + 1),(0,0)), mode='constant')
        if x >= buf.shape[1]:
            buf = numpy.pad(buf, ((0,0),(0,x - buf.shape[1] + 1)), mode='constant')
        buf[y][x] = c

def write_char(char, offset_x=0, offset_y=0):
    """Write a single character to the buffer

    @param char The ASCII char to write
    @param offset_x Position the character along x
    @param offset_y Position the character along y"""

    char = _get_char(char)

    for x in range(5):
        for y in range(7):
            p = (char[x] & (1 << y)) > 0
            set_pixel(offset_x + x, offset_y + y, p)

def _get_char(char):
    char_ordinal = None

    try:
        char_ordinal = ord(char) - 32
    except TypeError:
        pass

    if char_ordinal is None or char_ordinal > len(font):
        raise ValueError("Unsupported char {}".format(char))

    return font[char_ordinal]

def set_decimal(index, state):
    """Set the state of a decimal point

    @param index Index of decimal from 0 to 5
    @param state State to set: 1=lit or 0=unlit"""

    global decimal
    if index in range(6):
        decimal[index] = 1 if state else 0

def write_string(string, offset_x=0, offset_y=0, kerning=True):
    """Write a string to the buffer

    @param string The text string to write
    @param offset_x Position the text along x
    @param offset_y Position the text along y
    @param kerning Whether to kern the characters closely together or display one per matrix"""
 
    str_buf = []

    space = [0x00] * 5
    gap = [0x00] * 3

    if kerning:
        space = [0x00] * 2
        gap = [0x00]

    for char in string:
        if char == ' ':
            str_buf += space
        else:
            char_data = numpy.array(_get_char(char))
            if kerning:
                char_data = numpy.trim_zeros(char_data)
            str_buf += list(char_data)
        str_buf += gap # Gap between chars

    for x in range(len(str_buf)):
        for y in range(7):
            p = (str_buf[x] & (1 << y)) > 0
            set_pixel(offset_x + x, offset_y + y, p)

    l = len(str_buf)
    del str_buf
    return l

def scroll(amount_x=1, amount_y=0):
    """Scroll the buffer

    @param amount_x Amount to scroll along x axis
    @param amount_y Amount to scroll along y axis"""

    global scroll_x, scroll_y
    scroll_x += amount_x
    scroll_y += amount_y
    scroll_x %= buf.shape[1]
    scroll_y %= buf.shape[0]

def scroll_to(position_x=0, position_y=0):
    """Scroll to a specific position

    @param position_x Desired position along x axis
    @param position_y Desired position along y axis"""

    global scroll_x, scroll_y
    scroll_x = position_x % buf.shape[1]
    scroll_y = position_y % buf.shape[0]

def scroll_horizontal(amount=1):
    """Scroll horizontally (along x)

    @param amount Amount to scroll along x axis"""

    scroll(amount_x=amount, amount_y=0)

def scroll_vertical(amount=1):
    """Scroll vertically (along y)

    @param amount Amount to scroll along y axis"""

    scroll(amount_x=0, amount_y=amount)

def set_brightness(brightness):
    """Set the display brightness

    @param brightness Brightness to set, from 0 to 127"""
    if brightness < 0 or brightness > 127:
        raise ValueError("Brightness should be between 0 and 127")

    for m_x in range(6):
        mat[m_x][0].set_brightness(brightness)

def show():
    """Output the buffer to the display

    A copy of the buffer will be scrolled and rotated according
    to settings before being drawn to the display."""

    scrolled_buffer = numpy.copy(buf)
    scrolled_buffer = numpy.roll(scrolled_buffer, -scroll_x, axis=1)
    scrolled_buffer = numpy.roll(scrolled_buffer, -scroll_y, axis=0)

    if _rotate180:
        scrolled_buffer = numpy.rot90(scrolled_buffer[:7, :45], 2)

    for m_x in range(6):
        x = (m_x * 8)
        b = scrolled_buffer[0:7, x:x+5]

        mat[m_x][0].set_decimal(mat[m_x][1], decimal[m_x])

        for x in range(5):
            for y in range(7):
                 try:
                     mat[m_x][0].set_pixel(mat[m_x][1], x, y, b[y][x])
                 except IndexError:
                     pass # Buffer doesn't span this matrix yet
        del b
    for m_x in range(0,6,2):
        mat[m_x][0].update()

def draw_tiny(display, text):
    """Draw tiny numbers to the buffer

    Useful for drawing things like IP addresses.
    Can sometimes fit up to 3 digits on a single matrix

    @param display Index from 0 to 5 of display to target, determines buffer offset
    @param text Number to display"""

    buf = []
    for num in [int(x) for x in text]:
        buf += tinynumbers[num]
        buf += [0] # Space

    for row in range(min(len(buf),7)):
        data = buf[row]

        offset_x = display * 8
        offset_y = 6-(row % 7)

        for d in range(5):
            set_pixel(offset_x+(4-d), offset_y, (data & (1 << d)) > 0)

