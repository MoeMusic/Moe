#########
List (ls)
#########
Lists music in your library.

*************
Configuration
*************
This plugin is enabled by default.

***********
Commandline
***********
.. code-block:: bash

    moe ls [-h] [-a | -e] query

Options
=======
``-h, --help``
    Display the help message.
``-a, --album``
    Query for matching albums instead of tracks.
``-e, --extra``
    Query for matching extras instead of tracks.

Arguments
=========
``query``
    Query your library for items to list. See the :doc:`query docs <../query>` for more info.
