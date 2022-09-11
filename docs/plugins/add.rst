###
Add
###
Adds music to your library.

*************
Configuration
*************
The ``add`` plugin is enabled by default.

***********
Commandline
***********

.. code-block:: bash

    moe add [-h] path [path ...]

Options
-------
``-h, --help``
    Display the help message.

Arguments
---------
``path``
    The filesystem path of the track or album to add to the library. If ``path`` is a directory, Moe assumes that directory contains a single album.

