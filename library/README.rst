|Micro Dot pHAT| https://shop.pimoroni.com/products/microdot-phat

Micro Dot pHAT is an unashamedly old school LED matrix display board,
with up to 30x7 pixels, using the Lite-On LTP-305 matrices. Perfect for
building a retro scrolling message display or a tiny 30 band spectrum
analyser.

Installing
----------

Full install (recommended):
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We've created an easy installation script that will install all
pre-requisites and get your Micro Dot pHAT up and running with minimal
efforts. To run it, fire up Terminal which you'll find in Menu ->
Accessories -> Terminal on your Raspberry Pi desktop, as illustrated
below:

.. figure:: http://get.pimoroni.com/resources/github-repo-terminal.png
   :alt: Finding the terminal

In the new terminal window type the command exactly as it appears below
(check for typos) and follow the on-screen instructions:

.. code:: bash

    curl https://get.pimoroni.com/microdotphat | bash

Alternatively, on Raspbian, you can download the ``pimoroni-dashboard``
and install your product by browsing to the relevant entry:

.. code:: bash

    sudo apt-get install pimoroni

(you will find the Dashboard under 'Accessories' too, in the Pi menu -
or just run ``pimoroni-dashboard`` at the command line)

If you choose to download examples you'll find them in
``/home/pi/Pimoroni/microdotphat/``.

Manual install:
~~~~~~~~~~~~~~~

Library install for Python 3:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

on Raspbian:

.. code:: bash

    sudo apt-get install python3-microdotphat

other environments:

.. code:: bash

    sudo pip3 install microdotphat

Library install for Python 2:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

on Raspbian:

.. code:: bash

    sudo apt-get install python-microdotphat

other environments:

.. code:: bash

    sudo pip2 install microdotphat

Development:
~~~~~~~~~~~~

If you want to contribute, or like living on the edge of your seat by
having the latest code, you should clone this repository, ``cd`` to the
library directory, and run:

.. code:: bash

    sudo python3 setup.py install

(or ``sudo python setup.py install`` whichever your primary Python
environment may be)

In all cases you will have to enable the i2c bus.

Documentation & Support
-----------------------

-  Guides and tutorials - https://learn.pimoroni.com/microdot-phat
-  Function reference - http://docs.pimoroni.com/microdotphat/
-  GPIO Pinout - https://pinout.xyz/pinout/micro\_dot\_phat
-  Get help - http://forums.pimoroni.com/c/support

Unofficial / Third-party libraries
----------------------------------

-  Java library by Jim Darby - https://github.com/hackerjimbo/PiJava

.. |Micro Dot pHAT| image:: https://raw.githubusercontent.com/pimoroni/microdot-phat/master/microdot-phat-logo.png
