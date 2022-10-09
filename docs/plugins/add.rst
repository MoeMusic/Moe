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

    moe add [-h] [-a ALBUM_QUERY] path [path ...]

Positional Arguments
--------------------
``path``
    The filesystem path of the track or album to add to the library. If ``path`` is a directory, Moe assumes that directory contains a single album.

Optional Arguments
------------------
``-h, --help``
    Display the help message.
``-a ALBUM_QUERY, --album_query ALBUM_QUERY``
    Album to add an extra or track to (required if adding an extra).
