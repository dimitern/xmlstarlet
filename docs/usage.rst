=====
Usage
=====

To use XMLStarlet CFFI in a project::

    import xmlstarlet


Each command takes the same string arguments as the C version of `xmlstarlet`, and returns an
integer exit code (0 means success). Here's how you can use the `edit` command, for example::

   assert xmlstarlet.edit(
        "-S",
        "-N",
        "_=urn:local:html",
        "--var",
        "foo",
        "translate(//_:a[1]/text(), ' \n', '')",
        "-s",
        "/_:html",
        "-t",
        "attr",
        "-n",
        "text",
        "-v",
        "X",
        "-u",
        "$prev",
        "-x",
        "$foo",
        "./test.xml",
        "./test2.xml",
    ) == 0
