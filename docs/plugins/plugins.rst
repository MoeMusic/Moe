#######
Plugins
#######
Almost everything in Moe is a plugin. To see more details on each individual plugin, visit its page.

*************
Configuration
*************

Global Options
==============
Most configuration options reside in their relevant plugin, however there is currently one global option:

``default_plugins = ["add", "edit", "info", "ls", "move", "musicbrainz", "rm", "write"]``
    Overrides the list of default plugins.

Plugin Options
==============
For plugin specific configuration, see the respective plugin's page. Each plugin option should be specified under that plugin's section in the config.

For example, it's common to want to specify where Moe should move your music files once it's been added to the library. To do this, we'd check out the ``move`` plugin and find it has the ``library_path`` configuration option. To customize this option, we'd write the following in our config file.

.. code-block:: toml

    [move]
    library_path = "~/Music"

Default Plugins
===============
These are all the plugins that are enabled by default.

.. toctree::
   :maxdepth: 1

   Add <add>
   Edit <edit>
   Info <info>
   List <list>
   Move <move>
   Musicbrainz <musicbrainz>
   Remove <remove>
   Write <write>
