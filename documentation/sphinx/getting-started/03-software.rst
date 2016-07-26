Software
--------

Installing
~~~~~~~~~~

The quickest way to get started with Micro Dot pHAT is to use our one-line-installer::

    curl -sS get.pimoroni.com/microdotphat | bash

This will download and install the library, examples and any software required to get them up and running.

First Steps
~~~~~~~~~~~

To start your first Micro Dot pHAT program, you should fire up IDLE and type::

    import microdotphat

To write some text to the internal buffer, just call::

    microdotphat.write_string("Hello World")

And to output it to the display::

    microdotphat.show()

See the :doc:`Library Reference <reference>` for all the methods you'll need to make your first script come to life.

