:tocdepth: 2

**********************
Command-Line Interface
**********************
Moe ships with a command-line interface to access and manipulate your music library.

add
===
Adds music to your library.

By default, when adding music to your library, the ``import`` plugin will attempt to import metadata from any enabled sources, and the ``move`` plugin will copy the newly added files per your configuration. If you'd like to disable either behavior, you can disable the plugins either in your configuration file or by setting the ``MOE_DISABLE_PLUGINS`` environment variable.

.. tip::

   If your music already has correct tags, you can save a lot of time when adding it to Moe by disabling the ``import`` plugin.

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

edit
====
Edits music in your library.

.. code-block:: bash

    moe edit [-h] [-a | -e] query FIELD=VALUE [FIELD=VALUE ...]


Positional Arguments
--------------------
``query``
    Query your library for items to edit. See the :doc:`query docs <../query>` for more info.

``FIELD=VALUE``
    ``FIELD`` is any field for the type of query given. For example, if you are querying for albums with ``-a, --album``, ``field`` must be an album field.
    ``VALUE`` is the value to set the field to.

    See the :doc:`fields page<fields>` for all the available fields you can edit. Note that some fields cannot be edited and are annotated as such.

    .. note::
        If the specified field supports multiple values, you can separate those values with a semicolon e.g. ``genre=hip hop;pop``.

Optional Arguments
------------------
``-h, --help``
    Display the help message.
``-a, --album``
    Query for matching albums instead of tracks.
``-e, --extra``
    Query for matching extras instead of tracks.

list
====
Lists music in your library.

.. code-block:: bash

    moe list [-h] [-a | -e] [-p] query

Positional Arguments
--------------------
``query``
    Query your library for items to list. See the :doc:`query docs <../query>` for more info.

Optional Arguments
------------------
``-h, --help``
    Display the help message.
``-a, --album``
    Query for matching albums instead of tracks.
``-e, --extra``
    Query for matching extras instead of tracks.
``-i, --info``
    Output full information on each item.
``-p, --paths``
    List item paths.

move
====
Moves all items in the library according to your configuration file. This can be used to update the items in your library to reflect changes in your configuration.

.. code-block:: bash

    moe move [-h] [-n]

Optional Arguments
------------------
``-h, --help``
    Display the help message.

``-n, --dry-run``
    Show what will be moved without actually moving any files.

read
====
Updates Moe with any changes to your music files.

.. code-block:: bash

    moe read [-h] [-a | -e] [-r] query

Positional Arguments
--------------------
``query``
    Query your library for items to read. See the :doc:`query docs <../query>` for more info.

Optional Arguments
------------------
``-h, --help``
    Display the help message.
``-a, --album``
    Query for matching albums instead of tracks.
``-e, --extra``
    Query for matching extras instead of tracks.
``-r, --remove``
    Remove items that no longer exist on the filesystem.

remove
======
Removes music from your library.

.. code-block:: bash

    moe remove [-h] [-a | -e] [-d] query

Positional Arguments
--------------------
``query``
    Query your library for items to remove. See the :doc:`query docs <../query>` for more info.

Optional Arguments
------------------
``-h, --help``
    Display the help message.
``-a, --album``
    Query for matching albums instead of tracks.
``-e, --extra``
    Query for matching extras instead of tracks.
``-d, --delete``
    Delete the items from the filesystem.
