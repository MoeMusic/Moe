:tocdepth: 3

#############
Configuration
#############
Moe will automatically create a config file, ``config.toml``, in ``$HOME/.config/moe`` or ``%USERPROFILE%\.config\moe`` if you're on Windows. This directory is also where your library database file will reside.

.. note::
    The configuration directory can be overwritten by setting the environment variable ``MOE_CONFIG.CONFIG_DIR``.

Throughout this documentation, all configuration options will be displayed in the following format:

``option = default_value``

If there is any functionality you'd like to customize that doesn't have a configuration option, please feel free to open a `feature request <https://github.com/MoeMusic/Moe/issues/new?assignees=&labels=&template=feature_request.md>`_ asking for it!

Global Options
==============
Most configuration options reside in their relevant plugin, however there are the following global options:

``default_plugins = ["add", "edit", "info", "ls", "move", "rm", "write"]``
    Overrides the list of default plugins.

``disable_plugins = []``
    List of any plugins to explicitly disable. This takes priority over ``enable_plugins``.

``enable_plugins = []``
    List of any plugins to explicitly enable.

.. _library_path config option:

``library_path = "~/Music"``
    Tells Moe where your music library resides.

    For Windows users, ``~`` is your ``%USERPROFILE%`` directory. It's recommended to use a forward slash ``/`` to delineate sub-directories for your library path for consistency with other configuration options, but you may also use a backslash ``\``. If you choose to use backslashes, ensure you enclose your path in single quotes, e.g. ``'~\Music'``, to ensure the backslash ``\`` isn't interpreted as an escape character.

    .. note::
       If you change ``library_path``, Moe will attempt to search for your music in the new location.

``original_date = false``
    Whether or not to always set an album's ``date`` to its ``original_date`` if present.

    .. note::
       This change will also propagate onto the respective ``year`` fields.

Plugin Options
==============
Each plugin option should be specified under that plugin's section in the config. For example, to customize the ``asciify_paths`` option under the ``move`` plugin, we'd write the following in our config file.

.. code-block:: toml

    [move]
    asciify_paths = true

Move
----
``asciify_paths = false``
    Whether or not to convert all filesystem paths to ascii.

    If ``true``, non-ascii characters will be converted to their ascii equivalents, e.g. ``café.mp3`` will become ``cafe.mp3``.

Path Configuration Options
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. note::
    Any items added to your library will be automatically copied to their respective path configurations.

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

.. tip::
    - For any path formatting changes, run ``moe move -n`` for a dry-run to avoid any unexpected results.
    - For a more detailed look at all the field options and types, take a look at the :ref:`library api <Library API>`. ``album``, ``track``, and ``extra`` in the path formats are ``Album``, ``Track``, and ``Extra`` objects respectively and thus you can reference any of their available attributes.

Custom Path Template Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Moe allows plugins to create custom path template functions that can be called within the path templates. The function called in the default ``extra_path`` template, ``e_unique``, is an example of a custom path template function. The following custom template functions are included in the move plugin:

.. autofunction:: moe.move.move_core.e_unique

Overriding Config Values
========================
All configuration parameters can be overridden through environment variables. To override the configuration parameter ``{param}``, use an environment variable named ``MOE_{PARAM}``.

For example, to override the ``asciify_paths`` variable, you can run Moe with:

.. code-block:: bash

    $ MOE_MOVE.ASCIIFY_PATHS="true" moe

.. note::
   Notice since the ``asciify_paths`` option is specific to the ``move`` plugin, we use ``move.asciify_paths`` to access it.

Extending Your Configuration With Plugins
=========================================
If you aren't afraid of writing a little bit of Python, the best way to extend your configuration and truly mold Moe to your exact liking is through local plugins. Writing plugins is extremely easy, and can allow you to customize Moe beyond the limitations of the configuration file.

Check out the :doc:`writing plugins docs <developers/writing_plugins>` to get started on writing your own plugins.

If you have any questions, please don't hesitate `to ask
on github <https://github.com/MoeMusic/Moe/discussions/categories/q-a>`_!
