#!/usr/bin/env python

import math
import time

from microdotphat import clear, set_brightness, show, write_string, WIDTH, HEIGHT


print("""Fading Text

Uses the brightness control to fade between messages.
""")

speed = 5
strings = ["One", "Two", "Three", "Four"]


string = 0
shown = True

show()

# Start time. Phase offset by math.pi/2
start = time.time()

while True:
    # Fade the brightness in/out using a sine wave
    b = (math.sin((time.time() - start) * speed) + 1) / 2
    set_brightness(b)

    # At minimum brightness, swap out the string for the next one
    if b < 0.002 and shown:
        clear()
        write_string(strings[string], kerning=False)

        string += 1
        string %= len(strings)

        show()
        shown = False

    # At maximum brightness, confirm the string has been shown
    if b > 0.998:
        shown = True

    # Sleep a bit to save resources, this wont affect the fading speed
    time.sleep(0.01)
