####
Edit
####
Edits music in your library.

*************
Configuration
*************
This plugin is enabled by default.

***********
Commandline
***********

.. code-block:: bash

    moe edit [-h] [-a] query FIELD=VALUE [FIELD=VALUE ...]

Options
=======
``-h, --help``
    Display the help message.
``-a, --album``
    Query albums instead of tracks.

Arguments
=========
``query``
    Query your library for items to edit. See the :doc:`query docs <../query>` for more info.

``FIELD=VALUE``
    Set a track's field or an album's field if an album query is specified with the ``-a, --album`` option. If the specified field supports multiple values, you can separate those values with a semicolon e.g. ``genre=hip hop;pop``.

    The following is a list of all the available fields you can edit.

    *Track fields*

    * ``album``
    * ``albumartist``
    * ``artist``
    * ``genre`` [*]_
    * ``title``
    * ``track_num``
    * ``year``

    *Album fields*

    * ``artist``
    * ``title``
    * ``year``

    .. [*] Supports multiple values.

.. note::
    Editing a track's album-related field is equivalent to editing the field directly through the album. For example, the following commands will both edit an album's artist.

    .. code-block:: bash

        moe edit [query] albumartist=2Pac
        moe edit -a [query] artist=2Pac
