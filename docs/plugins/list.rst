####
List
####
Lists music in your library.

*************
Configuration
*************
The ``list`` plugin is enabled by default.

***********
Commandline
***********
.. code-block:: bash

    moe list [-h] [-a | -e] [-p] query

Options
=======
``-h, --help``
    Display the help message.
``-a, --album``
    Query for matching albums instead of tracks.
``-e, --extra``
    Query for matching extras instead of tracks.
``-p, --paths``
    List item paths.

Arguments
=========
``query``
    Query your library for items to list. See the :doc:`query docs <../query>` for more info.
