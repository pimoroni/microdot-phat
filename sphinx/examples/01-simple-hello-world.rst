Simple Hello World
==================

A message up to 6 characters in length and with no scrolling is the simplest way
to use Micro Dot pHAT. This doesn't have to be static, it could be the time for example,
or some other piece of information.

To display one character per matrix, you need to tern off the ``kerning`` option of ``write_string``::

    from microdotphat import write_string, show, set_clear_on_exit

    set_clear_on_exit(False)
    write_string("Ahoy!!", kerning=False)
    show()

This example will display the word "Ahoy!!" on your Micro Dot pHAT and then exit,
leaving the text displayed.

