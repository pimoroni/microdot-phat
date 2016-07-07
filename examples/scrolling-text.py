#!/usr/bin/env python
from microdotphat import write_string, scroll, update
import time
             
write_string(0, 'In the old #BILGETANK we\'ll keep you in the know!      ')

while True:
    scroll()
    update()
    time.sleep(0.05)
