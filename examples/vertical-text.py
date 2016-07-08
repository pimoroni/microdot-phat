#!/usr/bin/env python
from microdotphat import HEIGHT, write_string, scroll_vertical, show
import time
             
write_string('One',   offset_y = 0)
write_string('Two',   offset_y = HEIGHT)
write_string('Three', offset_y = HEIGHT*2)

while True:
    time.sleep(1)
    for x in range(7):
        scroll_vertical()
        show()
        time.sleep(0.05)
