####
Read
####
Reads item files and updates them in Moe with any changes.

*************
Configuration
*************
The ``read`` plugin is enabled by default.

***********
Commandline
***********

.. code-block:: bash

    moe read [-h] [-a | -e] [-r] query

Positional Arguments
====================
``query``
    Query your library for items to read. See the :doc:`query docs <../query>` for more info.

Optional Arguments
==================
``-h, --help``
    Display the help message.
``-a, --album``
    Query for matching albums instead of tracks.
``-e, --extra``
    Query for matching extras instead of tracks.
``-r, --remove``
    Remove items that no longer exist on the filesystem.
