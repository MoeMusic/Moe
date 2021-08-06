####
Info
####
Prints information about the music in your library via the ``info`` command. This includes any tags and other relevant information.

*************
Configuration
*************
The ``info`` plugin is enabled by default.

***********
Commandline
***********
.. code-block:: bash

    moe info [-h] [-a | -e] query

Currently, only a basic set of tags are supported, so you probably won't see all the tags of your music.

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
    Query your library for items to print info for. See the :doc:`query docs <../query>` for more info.
