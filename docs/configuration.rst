:tocdepth: 3

#############
Configuration
#############
Moe will automatically create a config file, ``config.toml``, in ``$HOME/.config/moe`` or ``%USERPROFILE%\.config\moe`` if you're on Windows. This directory is also where your library database file will reside.

.. note::
    The configuration directory can be overwritten by setting the environment variable ``MOE_CONFIG_DIR``.

Throughout this documentation, all configuration options will be displayed in the following format:

``option = default_value``

If there is any functionality you'd like to customize that doesn't have a configuration option, please feel free to open a `feature request <https://github.com/MoeMusic/Moe/issues/new?assignees=&labels=&template=feature_request.md>`_ asking for it!

Global Options
==============
Most configuration options reside in their relevant plugin, however there are the following global options:

``default_plugins = ["add", "cli", "duplicate", "edit", "import", "list", "move", "remove", "write"]``
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

Import
------
``max_candidates = 5``
    Maximum number of candidate albums to display in the import prompt.

    When running ``moe add``, this setting controls how many potential matches are shown when importing albums. Increasing this value allows you to see more options when multiple matches are found from metadata providers like MusicBrainz and Discogs.

    .. code-block:: toml

        [import]
        max_candidates = 10  # Show up to 10 candidate albums

    .. note::
        This setting only affects the number of candidates displayed in the interactive prompt. To increase the number of candidates fetched from metadata providers, you may also need to adjust the search limits for individual plugins like ``musicbrainz.search_limit``.

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

Advanced Path Template Configuration
************************************
There are two options for even more customization of your path templates: functions, and programmatically overriding the template entirely. Both of these options require :ref:`extending_your_config_with_plugins`.

Custom Path Template Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Plugins can create custom path template functions to be called within the path templates. These functions are useful for altering the results of directory or file names, but cannot be used to specify custom sub-directories (for that, see :ref:`overriding_path_templates_programmatically`).

The function called in the default ``extra_path`` template, ``e_unique``, is an example of a custom path template function. The following custom template functions are included in the move plugin:

.. autofunction:: moe.move.move_core.e_unique

To create your own path template functions, implement the :meth:`~moe.move.move_core.Hooks.create_path_template_func` hook in your plugin.

.. _overriding_path_templates_programmatically:

Overriding Path Templates Programmatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The path templates themselves can also be set programmatically via a plugin rather than from your configuration file. Using python to set your path templates allows you to specify different path templates entirely based on criteria such as storing all classical albums in a separate directory. Currently, both the album and extra path templates can be set by plugins using the :meth:`~moe.move.move_core.Hooks.override_album_path_config` and the  :meth:`~moe.move.move_core.Hooks.override_extra_path_config` hooks.

Overriding Config Values
========================
All configuration parameters can be overridden through environment variables. To override global configuration parameters use an environment variable named ``MOE_{PARAM}``:

.. code-block:: bash

    $ MOE_DISABLE_PLUGINS="['musicbrainz']" moe

For plugin specific configuration parameters, use ``MOE_{PLUGIN}__{PARAM}``:

.. code-block:: bash

    $ MOE_MOVE__ASCIIFY_PATHS=true moe

.. _extending_your_config_with_plugins:

Extending Your Configuration With Plugins
=========================================
If you aren't afraid of writing a little bit of Python, the best way to extend your configuration and truly mold Moe to your exact liking is through local plugins. Writing plugins is extremely easy, and can allow you to customize Moe beyond the limitations of the configuration file.

Check out the :doc:`writing plugins docs <developers/writing_plugins>` to get started on writing your own plugins.

If you have any questions, please don't hesitate `to ask
on github <https://github.com/MoeMusic/Moe/discussions/categories/q-a>`_!
