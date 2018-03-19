# -*- coding: utf-8 -*-

"""A library for driving the Pimoroni Micro Dot pHAT Raspberry Pi add-on.

This library creates a virtual buffer of unlimited size onto which you
can write text and icons for scrolling around the Micro Dot pHAT display.

Methods are included for rotating and scrolling, plus writing text either
kerned to one pixel spacing, or spaced to place one character per matrix.

"""

import atexit
from sys import exit

try:
    import numpy
except ImportError:
    raise ImportError("This library requires the numpy module\nInstall with: sudo pip install numpy")

from .font import font as _font, tinynumbers as _tinynumbers
from .matrix import NanoMatrix

__version__ = '0.2.1'

WIDTH = 45
HEIGHT = 7

_is_setup = False
_buf = numpy.zeros((HEIGHT,WIDTH))
_decimal = [0] * 6

_scroll_x = 0
_scroll_y = 0

_clear_on_exit = True
_rotate180 = False
_mirror = False

def _exit():
    if _clear_on_exit:
        clear()
        show()

def clear():
    """Clear the buffer"""

    global _buf, _decimal
    _decimal = [0] * 6
    _buf = numpy.zeros((HEIGHT,WIDTH))
    _scroll_x = 0
    _scroll_y = 0

def fill(c):
    """Fill the buffer either lit or unlit

    :param c: Colour that should be filled onto the display: 1=lit or 0=unlit
    
    """

    global _buf
    _buf.fill(c)

def set_clear_on_exit(value):
    """Set whether the display should be cleared on exit

    Set this to false if you want to display a fixed message after
    your Python script exits.

    :param value: Whether the display should be cleared on exit: True/False

    """

    global _clear_on_exit
    _clear_on_exit = (value == True)

def set_rotate180(value):
    """Set whether the display should be rotated 180 degrees

    :param value: Whether the display should be rotated 180 degrees: True/False

    """

    global _rotate180
    _rotate180 = (value == True)

def set_mirror(value):
    """Set whether the display should be flipped left to right (mirrored)

    :param value: Whether the display should be flipped left to right: True/False

    """

    global _mirror
    _mirror = (value == True)

def set_col(x, col):
    """Set a whole column of the buffer

    Only useful when not scrolling vertically

    :param x: Specify which column to set
    :param col: An 8-bit integer, the 7 least significant bits correspond to each row

    """

    for y in range(7):
        set_pixel(x, y, (col & (1 << y)) > 0)

def set_pixel(x, y, c):
    """Set the state of a single pixel in the buffer

    If the pixel falls outside the current buffer size, it will be grown automatically

    :param x: The x position of the pixel to set
    :param y: The y position of the pixel to set
    :param c: The colour to set: 1=lit or 0=unlit

    """

    global _buf

    c = 1 if c else 0

    try:
        _buf[y][x] = c
    except IndexError:
        if y >= _buf.shape[0]:
            _buf = numpy.pad(_buf, ((0,y - _buf.shape[0] + 1),(0,0)), mode='constant')
        if x >= _buf.shape[1]:
            _buf = numpy.pad(_buf, ((0,0),(0,x - _buf.shape[1] + 1)), mode='constant')
        _buf[y][x] = c

def write_char(char, offset_x=0, offset_y=0):
    """Write a single character to the buffer

    :param char: The ASCII char to write
    :param offset_x: Position the character along x (default 0)
    :param offset_y: Position the character along y (default 0)

    """

    char = _get_char(char)

    for x in range(5):
        for y in range(7):
            p = (char[x] & (1 << y)) > 0
            set_pixel(offset_x + x, offset_y + y, p)

def _get_char(char):
    char_ordinal = None

    try:
        char_ordinal = ord(char)
    except TypeError:
        pass

    if char_ordinal == 65374:
        char_ordinal = 12316

    if char_ordinal is None or char_ordinal not in _font:
        raise ValueError("Unsupported char {}".format(char))

    return _font[char_ordinal]


def set_decimal(index, state):
    """Set the state of a _decimal point

    :param index: Index of _decimal from 0 to 5
    :param state: State to set: 1=lit or 0=unlit

    """

    global _decimal
    if index in range(6):
        _decimal[index] = 1 if state else 0

def write_string(string, offset_x=0, offset_y=0, kerning=True):
    """Write a string to the buffer

    :returns: The length, in pixels, of the written string.

    :param string: The text string to write

    :param offset_x: Position the text along x (default 0)
    :param offset_y: Position the text along y (default 0)
    :param kerning: Whether to kern the characters closely together or display one per matrix (default True)

    :Examples:

    Write a string to the buffer, aligning one character per dislay, This is
    ideal for displaying still messages up to 6 characters long::

        microdotphat.write_string("Bilge!", kerning=False)

    Write a string to buffer, with the characters as close together as possible.
    This is ideal for writing text which you intend to scroll::

        microdotphat.write_string("Hello World!")
    
    """
 
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


    if not kerning:
        while len(str_buf) < WIDTH + 3:
            str_buf += [0x00]

    for x in range(len(str_buf)):
        for y in range(7):
            p = (str_buf[x] & (1 << y)) > 0
            set_pixel(offset_x + x, offset_y + y, p)

    l = len(str_buf)
    del str_buf
    return l

def scroll(amount_x=0, amount_y=0):
    """Scroll the buffer

    Will scroll by 1 pixel horizontall if no arguments are supplied.

    :param amount_x: Amount to scroll along x axis (default 0)
    :param amount_y: Amount to scroll along y axis (default 0)

    :Examples:

    Scroll vertically::

       microdotphat.scroll(amount_y=1)

    Scroll diagonally::

       microdotphat.scroll(amount_x=1,amount_y=1)

    """

    global _scroll_x, _scroll_y
    if amount_x == 0 and amount_y == 0:
        amount_x = 1

    _scroll_x += amount_x
    _scroll_y += amount_y
    _scroll_x %= _buf.shape[1]
    _scroll_y %= _buf.shape[0]

def scroll_to(position_x=0, position_y=0):
    """Scroll to a specific position

    :param position_x: Desired position along x axis (default 0)
    :param position_y: Desired position along y axis (default 0)
    
    """

    global _scroll_x, _scroll_y
    _scroll_x = position_x % _buf.shape[1]
    _scroll_y = position_y % _buf.shape[0]

def scroll_horizontal(amount=1):
    """Scroll horizontally (along x)

    Will scroll one pixel horizontally if no amount is supplied.

    :param amount: Amount to scroll along x axis (default 1)

    """

    scroll(amount_x=amount, amount_y=0)

def scroll_vertical(amount=1):
    """Scroll vertically (along y)

    Will scroll one pixel vertically if no amount is supplied.

    :param amount: Amount to scroll along y axis (default 1)

    """

    scroll(amount_x=0, amount_y=amount)

def set_brightness(brightness):
    """Set the display brightness

    :param brightness: Brightness to set, from 0.0 to 1.0

    """

    setup()

    if brightness < 0 or brightness > 1:
        raise ValueError("Brightness should be between 0.0 and 1.0")

    for m_x in range(6):
        _mat[m_x][0].set_brightness(brightness)

def show():
    """Output the buffer to the display

    A copy of the buffer will be scrolled and rotated according
    to settings before being drawn to the display.

    """

    setup()

    scrolled_buffer = numpy.copy(_buf)
    scrolled_buffer = numpy.roll(scrolled_buffer, -_scroll_x, axis=1)
    scrolled_buffer = numpy.roll(scrolled_buffer, -_scroll_y, axis=0)

    if _rotate180:
        scrolled_buffer = numpy.rot90(scrolled_buffer[:7, :45], 2)

    if _mirror:
        scrolled_buffer = numpy.fliplr(scrolled_buffer[:7, :45])

    for m_x in range(6):
        x = (m_x * 8)
        b = scrolled_buffer[0:7, x:x+5]

        _mat[m_x][0].set_decimal(_mat[m_x][1], _decimal[m_x])

        for x in range(5):
            for y in range(7):
                 try:
                     _mat[m_x][0].set_pixel(_mat[m_x][1], x, y, b[y][x])
                 except IndexError:
                     pass # Buffer doesn't span this matrix yet
        del b
    for m_x in range(0,6,2):
        _mat[m_x][0].update()

def draw_tiny(display, text):
    """Draw tiny numbers to the buffer

    Useful for drawing things like IP addresses.
    Can sometimes fit up to 3 digits on a single matrix

    :param display: Index from 0 to 5 of display to target, determines buffer offset
    :param text: Number to display

    """

    _buf = []
    try:
        for num in [int(x) for x in text]:
            _buf += _tinynumbers[num]
            _buf += [0] # Space

    except ValueError:
        raise ValueError("text should contain only numbers: '{text}'".format(text=text))

    for row in range(min(len(_buf),7)):
        data = _buf[row]

        offset_x = display * 8
        offset_y = 6-(row % 7)

        for d in range(5):
            set_pixel(offset_x+(4-d), offset_y, (data & (1 << d)) > 0)

def setup():
    global _is_setup, _n1, _n2, _n3, _mat

    if _is_setup:
        return True

    _n1 = NanoMatrix(address=0x63)
    _n2 = NanoMatrix(address=0x62)
    _n3 = NanoMatrix(address=0x61)

    _mat = [(_n1, 1), (_n1, 0), (_n2, 1), (_n2, 0), (_n3, 1), (_n3, 0)]

    atexit.register(_exit)

    _is_setup = True

