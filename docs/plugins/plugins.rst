#######
Plugins
#######
Almost everything in Moe is a plugin. To see more details on each individual plugin, visit its page.

*************
Configuration
*************

Global Options
==============
Most configuration options reside in their relevant plugin, however there are the following global options:

``default_plugins = ["add", "edit", "info", "ls", "move", "musicbrainz", "rm", "write"]``
    Overrides the list of default plugins.

.. _library_path config option:

``library_path = "~/Music"``
    Tells Moe where your music library resides.

    For Windows users, ``~`` is your ``%USERPROFILE%`` directory. It's recommended to use a forward slash ``/`` to delineate sub-directories for your library path for consistency with other configuration options, but you may also use a backslash ``\``. If you choose to use backslashes, ensure you enclose your path in single quotes, e.g. ``'~\Music'``, to ensure the backslash ``\`` isn't interpreted as an escape character.

    .. note::
       If you change ``library_path``, Moe will attempt to search for your music in the new location.

Plugin Options
==============
For plugin specific configuration, see the respective plugin's page. Each plugin option should be specified under that plugin's section in the config.

For example, you may want to ensure when Moe moves your music, it only names files using ascii characters. To do this, we'd check out the ``move`` plugin and find it has the ``asciify_paths`` configuration option. To customize this option, we'd write the following in our config file.

.. code-block:: toml

    [move]
    asciify_paths = true

Default Plugins
===============
These are all the plugins that are enabled by default.

.. toctree::
   :maxdepth: 1

   add
   edit
   import
   info
   list
   move
   musicbrainz
   remove
   write
