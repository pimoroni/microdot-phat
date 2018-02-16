#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
             
from microdotphat import write_string, scroll, show


print("""Scrolling Text

Scrolls a message across the screen.

Usage: {name} "your message"

Press Ctrl+C to exit.
""".format(name=sys.argv[0]))

text = u"にほんこ゛ ヘ゜ロヘ゜ロ ＯＩＳＨＩＩＹＯ！！！"

if len(sys.argv) > 1:
    text = sys.argv[1]

write_string(text, offset_x=0)

while True:
    scroll()
    show()
    time.sleep(0.05)
