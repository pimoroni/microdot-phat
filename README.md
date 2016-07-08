![Micro Dot pHAT](microdot-phat-logo.png)

An unashamedly old school LED matrix display board, with up to 30x7 pixels, using the Lite-On LTP-305 matrices. Use between 1 and 6 matrices in your choice of red and/or green. Perfect for building a retro scrolling message display or a tiny 30 band spectrum analyser.

<!-- Available from Pimoroni: https://shop.pimoroni.com/products/micro-dot-phat -->

##Installation

We've created a super-easy installation script that will install all pre-requisites and get your Micro Dot pHAT up and running in a jiffy. To run it fire up Terminal which you'll find in Menu -> Accessories -> Terminal on your Raspberry Pi desktop like so:

![Finding the terminal](terminal.jpg)

In the new terminal window type:

```bash
curl -sS get.pimoroni.com/microdotphat | bash
```

If you choose to download examples you'll find them in `/home/pi/Pimoroni/microdotphat/examples`.

##Usage

The Micro Dot pHAT library has two functions that should cover most use cases: `set_pixel` and `write_string`. We'll take a look at some simple examples of these functions.

The width of each matrix is 8x7 pixels, with the last 3 of those pixels being "imaginary" ones to correct for the gap between adjacent matrices so, if you're using all 6 displays, the total width will be 45x7 pixels.

###set_pixel

You can light up the top left pixel of the display second from the left by doing the following:

```
from microdotphat import clear, set_pixel, show

clear()
set_pixel(8, 0, 1)
show()
```

We clear the matrices first, then call the `set_pixel` function, passing in the x and y coordinates of the pixel we want to light, with a third parameter, `1`, that tells the function to switch the pixel on (`0` would switch it off).

Finally, we call `show` to push the data to the matrices. Remember that the first pixel on the second display will be index 8, because the pixels are indexed from 0 and there are the 3 imaginary pixels between the first and second displays.

You can also import `WIDTH` and `HEIGHT` from the library and use these to iterate through all of the pixels. For example, to light all of the pixels across all of the matrices, you would do the following:

```
from microdotphat import clear, set_pixel, show, WIDTH, HEIGHT

clear()

for x in range(HEIGHT):
    for y in range(WIDTH):
        set_pixel(x, y, 1)

show()
```

###write_string and scroll

The `write_string` and `scroll` functions provide a really simple way to scroll text across the Micro Dot matrices. We'll look at the `scrolling-text.py` example.

If you wanted to scroll the message "In the old #BILGETANK we'll keep you in the know!", you would do the following:

```
from microdotphat import write_string, scroll, show
import time

write_string(0, "In the old #BILGETANK we'll keep you in the know!      ")

while True:
    scroll()
    show()
    time.sleep(0.05)
```

We import the `write_string`, `scroll` and `show` functions, as well as the `time` library so that we can add a small delay to set the scrolling speed.

Then, we call the `write_string` function, with the `0` parameter being the start position at which we'll write the string (the left-most pixel), and passing in our text with a few spaces padded onto the end.

If we called `show` now, that text would be written to the matrices, but we also want to scroll the text. To do that, we can call the `scroll` and `show` functions in a `while True` loop.

`scroll` shifts through the buffer, but we also have to call `show` in each iteration of the `while` loop to push the changes to the matrices.

`time.sleep(0.05)` adds a small delay between each iteration and hence sets the scroll speed. Decreasing this value (in seconds) would increase the scroll speed and _vice versa_.

##Examples

There are a number of examples in the [examples](examples) folder that illustrate the above concepts.

If you've used the one-line installer and chosen to download the examples, these will be in the `/home/pi/Pimoroni/microdotphat/examples` directory.
