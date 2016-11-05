#!/usr/bin/env python

import math
import time

from microdotphat import clear, set_pixel, show


print("""Sine Wave

Displays a sine wave across your pHAT.

Press Ctrl+C to exit.
""")

while True:
    clear()
    t = time.time() * 10
    for x in range(45):
        y = int((math.sin(t + (x/2.5)) + 1) * 3.5)
        set_pixel(x, y, 1)
        
    show()
    time.sleep(0.01)
