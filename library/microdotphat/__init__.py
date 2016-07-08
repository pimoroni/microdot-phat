import numpy
from .matrix import NanoMatrix
from .font import font, tinynumbers
import time
import math
import atexit

n1 = NanoMatrix(address=0x63)
n2 = NanoMatrix(address=0x62)
n3 = NanoMatrix(address=0x61)

mat = [(n1, 1), (n1, 0), (n2, 1), (n2, 0), (n3, 1), (n3, 0)]

WIDTH = 45
HEIGHT = 7

buf = numpy.zeros((HEIGHT,WIDTH))
scroll_x = 0
scroll_y = 0

clear_on_exit = True

def _exit():
    global buf
    if clear_on_exit:
        buf.fill(0)
        show()

atexit.register(_exit)

def clear():
    global buf
    buf.fill(0)

def fill(c):
    global buf
    buf.fill(c)

def set_col(x, col):
    for y in range(7):
        set_pixel(x, y, (col & (1 << y)) > 0)

def set_pixel(x, y, c):
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
    char = font[ord(char) - 32]
    for x in range(5):
        for y in range(7):
            p = (char[x] & (1 << y)) > 0
            set_pixel(offset_x + x, offset_y + y, p)

def _get_char(char):
    return font[ord(char) - 32]

def write_string(string, offset_x=0, offset_y=0, kerning=True):
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
    global scroll_x, scroll_y
    scroll_x += amount_x
    scroll_y += amount_y
    scroll_x %= buf.shape[1]
    scroll_y %= buf.shape[0]

def scroll_to(position_x=0, position_y=0):
    global scroll_x, scroll_y
    scroll_x = position_x % buf.shape[1]
    scroll_y = position_y % buf.shape[0]

def scroll_horizontal(amount=1):
    scroll(amount_x=amount, amount_y=0)

def scroll_vertical(amount=1):
    scroll(amount_x=0, amount_y=amount)

def set_brightness(brightness):
    for m_x in range(6):
        mat[m_x][0].set_brightness(brightness)

def show():
    scrolled_buffer = numpy.roll(buf, -scroll_x, axis=1)
    scrolled_buffer = numpy.roll(scrolled_buffer, -scroll_y, axis=0)
    for m_x in range(6):
        x = (m_x * 8)
        b = scrolled_buffer[0:7, x:x+5]
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
