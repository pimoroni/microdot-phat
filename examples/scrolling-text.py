#!/usr/bin/env python

import time
import sys
             
from microdotphat import write_string, scroll, show


text = "In the old #BILGETANK we'll keep you in the know!      "

if len(sys.argv) > 1:
    text = sys.argv[1]

write_string(text, offset_x=0)

while True:
    scroll()
    show()
    time.sleep(0.05)
