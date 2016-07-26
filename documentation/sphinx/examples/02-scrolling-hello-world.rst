Scrolling Hello World
=====================

You need a few building blocks to scroll "Hello World" on Micro Dot pHAT.

First you must write the text, then scroll a little, wait a short time, scroll and repeat::

    import time

    from microdotphat import write_string, scroll, show

    length = write_string("Hello World   ")

    for x in range(length):
        scroll()
        show()
        time.sleep(0.1)
