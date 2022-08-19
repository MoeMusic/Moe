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
``library_path = "~/Music"``
    Tells Moe where your music library resides.

    For Windows users, the default path is ``%USERPROFILE%\Music``. Also, you need to set your path by enclosing it in triple-single quotes, e.g. ``'''~\Music'''``.

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
