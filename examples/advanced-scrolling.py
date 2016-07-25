#!/usr/bin/env python

import time

from microdotphat import WIDTH, HEIGHT, set_pixel, write_string, scroll, scroll_to, show


print("""Advanced Scrolling

Advanced scrolling example which displays a message line-by-line
and then skips back to the beginning.

Press Ctrl+C to exit.
""")

rewind = True
delay = 0.03

line_height = HEIGHT + 2
             
lines = ["In the old #BILGETANK we'll keep you in the know",
         "In the old #BILGETANK we'll fix your techie woes",
         "And we'll make things",
         "And we'll break things",
         "'til we're altogether aching",
         "Then we'll grab a cup of grog down in the old #BILGETANK"]

lengths = [0] * len(lines)

offset_left = 0

for line, text in enumerate(lines):
    lengths[line] = write_string(text, offset_x=offset_left, offset_y=line_height * line)
    offset_left += lengths[line]

set_pixel(0, (len(lines) * line_height) - 1, 0)

current_line = 0

show()

while True:
    pos_x = 0
    pos_y = 0
    for current_line in range(len(lines)):
        time.sleep(delay*10)
        for y in range(lengths[current_line]):
            scroll(1,0)
            pos_x += 1
            time.sleep(delay)
            show()
        if current_line == len(lines) - 1 and rewind:
            for y in range(pos_y):
                scroll(-int(pos_x/pos_y),-1)
                show()
                time.sleep(delay)
            scroll_to(0,0)
            show()
            time.sleep(delay)
        else:
            for x in range(line_height):
                scroll(0,1)
                pos_y += 1
                show()
                time.sleep(delay)
