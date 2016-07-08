#!/usr/bin/env python
from microdotphat import write_string, scroll, show
import time
             
write_string("In the old #BILGETANK we'll keep you in the know!      ", offset_x=0)

while True:
    scroll()
    show()
    time.sleep(0.05)
