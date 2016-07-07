#!/usr/bin/env python
import time
import math
from microdotphat import clear, set_pixel, update 

while True:
    clear()
    t = time.time() * 10
    for x in range(45):
        y = int((math.sin(t + (x/2.5)) + 1) * 3.5)
        set_pixel(x, y, 1)
        
    update()
    time.sleep(0.01)
