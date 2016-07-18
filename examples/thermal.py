#!/usr/bin/env python

import time
import datetime
from microdotphat import write_string, set_decimal, clear, show

delay = 1

while True:
    clear()
    path="/sys/class/thermal/thermal_zone0/temp"
    f = open(path, "r")
    temp_raw = int(f.read().strip())
    temp = float(temp_raw / 1000.0)
    write_string( "%.2f" % temp + "c", kerning=False)
    show()
    time.sleep(delay)
