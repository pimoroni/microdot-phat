#!/usr/bin/env python

import time

from microdotphat import draw_tiny, show, clear


print("""Tiny Font

Displays an IP address in a tiny, tiny number font!

Press Ctrl+C to exit.
""")

x = 0

while True:
    clear()
    draw_tiny(0,"192")
    draw_tiny(1,"178")
    draw_tiny(2,"0")
    draw_tiny(3,"68")
    draw_tiny(4,str(x))

    x += 1
    if x > 199: x = 0
    show()
    time.sleep(0.1)
