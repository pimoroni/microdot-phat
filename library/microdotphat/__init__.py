import numpy
from .matrix import NanoMatrix
from .font import font, tinynumbers
import time
import math

n1 = NanoMatrix(address=0x63)
n2 = NanoMatrix(address=0x62)
n3 = NanoMatrix(address=0x61)

mat = [(n1, 1), (n1, 0), (n2, 1), (n2, 0), (n3, 1), (n3, 0)]

WIDTH = 48
HEIGHT = 7

buf = numpy.zeros((HEIGHT,WIDTH))

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
        buf = numpy.pad(buf, ((0,0),(0,x - buf.shape[1] + 1)), mode='constant')
        buf[y][x] = c

def set_char(o_x, char):
    char = font[ord(char) - 32]
    for x in range(5):
        for y in range(7):
            p = (char[x] & (1 << y)) > 0
            set_pixel(o_x + x, y, p)

def get_char(char):
    return font[ord(char) - 32]

def write_string(o_x, string):
    str_buf = []
    for char in string:
        if char == ' ':
            str_buf += [0x00, 0x00]
        else:
            char_data = numpy.trim_zeros(numpy.array(get_char(char)))
            str_buf += list(char_data)
        str_buf += [0x00] # Gap between chars
    
    for x in range(len(str_buf)):
        for y in range(7):
            p = (str_buf[x] & (1 << y)) > 0
            set_pixel(o_x + x, y, p)

    del str_buf

def scroll():
    global buf
    buf = numpy.roll(buf, -1, axis=1)

def update():
    for m_x in range(6):
        x = (m_x * 8)
        b = buf[0:7, x:x+5]
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
