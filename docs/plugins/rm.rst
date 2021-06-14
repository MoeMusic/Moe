###########
Remove (rm)
###########
Removes music from your library.

*************
Configuration
*************
This plugin is enabled by default.

***********
Commandline
***********
.. code-block:: bash

    moe rm [-h] [-a | -e] query

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
    Query your library for items to remove. See the :doc:`query docs <../query>` for more info.
