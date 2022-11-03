.. _Move Plugin:

####
Move
####
Alters the location of files in your library.

.. note::
    Any items added to your library will be automatically copied to their respective path configurations.

*************
Configuration
*************
The ``move`` plugin is enabled by default and provides the following configuration options:

``asciify_paths = false``
    Whether or not to convert all filesystem paths to ascii.

    If ``true``, non-ascii characters will be converted to their ascii equivalents, e.g. ``café.mp3`` will become ``cafe.mp3``.

Path Configuration Options
==========================
``album_path = "{album.artist}/{album.title} ({album.year})"``
    Album filesystem path format relative to the global configuration option, :ref:`library_path <library_path config option>`.

``track_path = "{f'Disc {track.disc:02}' if album.disc_total > 1 else ''}/{track.track_num:02} - {track.title}{track.path.suffix}"``
    Track filesystem path format relative to ``album_path``.

    .. note::
        - The ``if`` statement inside the path simply means that if there is more than one disc in the album, the tracks will be put into separate directories for their respective disc.
        - Include ``track.path.suffix`` at the end if you wish to retain the file extension of the track file.

``extra_path = "{e_unique(extra)}"``
    Extra filesystem path format relative to ``album_path``.

Paths are formatted using python `f-strings <https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals>`_ which, as demonstrated by the default track path, allow all the advanced formatting and expression evaluation that come with them. You can access any of the :ref:`respective item's fields <fields:Fields>` in these strings using ``{[album/track/extra].field}`` notation as shown.

.. important::
    Windows users should use a forward slash ``/`` when delineating sub-directories in path formats as the back slash ``\`` is used as an escape character.

.. note::
    Forward slashes ``/`` cannot be used inside a nested f-string variable e.g. ``{f'Disc {track.disc}/{track.disc}}`` is not allowed. You may instead be able to achieve the behavior you're after by implementing a custom path template function as described below.

Custom Path Template Functions
==============================
Moe allows plugins to create custom path template functions that can be called within the path templates. The function called in the default ``extra_path`` template, ``e_unique``, is an example of a custom path template function. The following custom template functions are included in the move plugin:

.. autofunction:: moe.plugins.move.move_core.e_unique

.. tip::
    - For any path formatting changes, run ``moe move -n`` for a dry-run to avoid any unexpected results.
    - For a more detailed look at all the field options and types, take a look at the :ref:`library api <Library API>`. ``album``, ``track``, and ``extra`` in the path formats are ``Album``, ``Track``, and ``Extra`` objects respectively and thus you can reference any of their available attributes.

***********
Commandline
***********
The ``move`` command will move all items in the library according to your configuration file. This can be used to update the items in your library to reflect changes in your configuration.

.. code-block:: bash

    moe move [-h] [-n]

Optional Arguments
==================
``-h, --help``
    Display the help message.

``-n, --dry-run``
    Show what will be moved without actually moving any files.
