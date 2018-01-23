#!/usr/bin/env python

import time
import sys

import microdotphat             


print("""Scrolling Text

Scrolls a single word char by char across the screen.

Usage: {name} "your message"

Press Ctrl+C to exit.
""".format(name=sys.argv[0]))

text = "Ninja"

if len(sys.argv) > 1:
    text = sys.argv[1]

microdotphat.write_string(text, offset_x=0, kerning=False)
microdotphat.show()
time.sleep(0.5)

while True:
    microdotphat.scroll(amount_x=8)
    microdotphat.show()
    time.sleep(0.5)
