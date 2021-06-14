####
Info
####
Prints info about the music in your library. This includes any tags and other relevant information.

*************
Configuration
*************
This plugin is enabled by default.

***********
Commandline
***********
.. code-block:: bash

    moe info [-h] [-a] query

Currently, only a basic set of tags are supported, so you probably won't see all the tags of your music.

Options
=======
``-h, --help``
    Display the help message.
``-a, --album``
    Query albums instead of tracks.

Arguments
=========
``query``
    Query your library for items to print info for. See the :doc:`query docs <../query>` for more info.
