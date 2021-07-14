###############
Getting Started
###############

************
Installation
************
See the :ref:`Installation Guide <Installation Guide>` to install Moe.

****************
Required Reading
****************
Before using Moe, you should understand that Moe mostly consists of *plugins* or self-contained features, that each provide a different way of interacting with music in your library.
For example, the ``edit`` plugin lets you edit your music, while the ``add`` plugin lets you add music to your library. Each of these plugins comes with it's own commands and configuration options that let you define how Moe manages your music. Each configuration option has sensible defaults which means you *could* just run Moe out of the box, but I'd recommend taking a look at the following.

.. _General Configuration:

*************
Configuration
*************
Moe will automatically create a config file, ``config.toml``, in ``$HOME/.config/moe`` or ``%USERPROFILE%\.config\moe`` if you're on Windows. This directory is also where your library database file will reside.

.. note::
    The configuration directory can be overwritten by setting the environment variable ``MOE_CONFIG_DIR``.

All configuration options will presented in the following format

    ``option = default_value``

Global Options
==============
Most configuration options reside in their relevant plugin, however there is currently one global option:

``default_plugins = ["add", "edit", "info", "ls", "move", "musicbrainz", "rm", "write"]``
    Overrides the list of default plugins.

Plugin Options
==============
For plugin specific configuration, see the respective plugin's page under :doc:`plugins <plugins/plugins>`. Each plugin option should be specified under that plugin's section in the config.

For example, it's common to want to specify where Moe should move your music files once it's been added to the library. To do this, we'd check out the ``move`` plugin and find it has the ``library_path`` configuration option. To customize this option, we'd write the following in our config file.

    .. code-block:: toml

       [move]
       library_path = "~/Music"

Overriding Config Values
========================
All configuration parameters can be overridden through environment variables. To override the configuration parameter ``{param}``, use an environment variable named ``MOE_{PARAM}``.

For example, to override the ``library_path`` variable, you can run Moe with:

    .. code-block:: bash

       $ MOE_MOVE.LIBRARY_PATH="~/Music2" moe

.. note::
   Notice since the ``library_path`` option is specific to the ``move`` plugin, we use ``move.library_path`` to access it.

**********************
Command-Line Interface
**********************
Once you're confident you've configured everything to your liking, you're ready to run Moe.

    .. code-block:: bash

       $ moe

The help text of each command should be enough to get you started. For more info, see :doc:`plugins <plugins/plugins>`.
