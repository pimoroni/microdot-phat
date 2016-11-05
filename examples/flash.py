#!/usr/bin/env python

import time

from microdotphat import clear, show, set_decimal, set_pixel, WIDTH, HEIGHT


print("""Flash

Flashes all the elements.

Press Ctrl+C to exit.
""")

t = 0.5

while True:
    clear()
    show()
    time.sleep(t)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            set_pixel(x,y,1)
    for x in range(6):
        set_decimal(x,1)
    show()
    time.sleep(t)
