####
Sync
####
Syncs music metadata from connected sources.

*************
Configuration
*************
The ``sync`` plugin is enabled by default.

***********
Commandline
***********
.. code-block:: bash

    moe sync [-h] [-a | -e] [-p] query

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
    Query your library for items to sync. See the :doc:`query docs <../query>` for more info.
