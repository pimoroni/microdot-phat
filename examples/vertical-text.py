#!/usr/bin/env python

from microdotphat import HEIGHT, write_string, scroll_vertical, show
import time
             
lines = ['One', 'Two', 'Three', 'Four', 'Five']

for line, text in enumerate(lines):
    write_string(text, offset_y = line*7, kerning=False)

show()

while True:
    time.sleep(1)
    for x in range(7):
        scroll_vertical()
        show()
        time.sleep(0.02)
