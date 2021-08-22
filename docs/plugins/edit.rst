####
Edit
####
Edits music in your library.

*************
Configuration
*************
The ``edit`` plugin is enabled by default.

***********
Commandline
***********

.. code-block:: bash

    moe edit [-h] [-a | -e] query FIELD=VALUE [FIELD=VALUE ...]

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
    Query your library for items to edit. See the :doc:`query docs <../query>` for more info.

``FIELD=VALUE``
    ``FIELD`` is any field for the type of query given. For example, if you are querying for albums with ``-a, --album``, ``field`` must be an album field.
    ``VALUE`` is the value to set the field to.

    See the :doc:`fields page<../fields>` for all the available fields you can edit. The only exception is that you cannot edit the ``path`` of an item.

    .. note::
        If the specified field supports multiple values, you can separate those values with a semicolon e.g. ``genre=hip hop;pop``.

    .. note::
        Editing a track's album-related field is equivalent to editing the field directly through the album. For example, the following commands will both edit an album's artist.

        .. code-block:: bash

            moe edit [query] albumartist=2Pac
            moe edit -a [query] artist=2Pac
