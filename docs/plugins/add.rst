###
Add
###
Adds music to your library.

.. note::
    In order to add a track to your library, Moe requires each track to contain, at a minimum, a track number, an albumartist (or artist), and a date (or year).

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

