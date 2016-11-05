#!/usr/bin/env python

import time
import sys
             
from microdotphat import write_string, scroll, show


print("""Scrolling Text

Scrolls a message across the screen.

Usage: {name} "your message"

Press Ctrl+C to exit.
""".format(name=sys.argv[0]))

text = "In the old #BILGETANK we'll keep you in the know!      "

if len(sys.argv) > 1:
    text = sys.argv[1]

write_string(text, offset_x=0)

while True:
    scroll()
    show()
    time.sleep(0.05)
