###############
Getting Started
###############

************
Installation
************
1a. The latest release of Moe is available on `PyPI <https://pypi.org/project/moe>`_

.. code-block:: bash

    $ pip install moe

1b. Or, if you want to be on the bleeding edge and can't wait for the latest release, you can install from github.

.. code-block:: bash

    $ pip install git+https://github.com/MoeMusic/Moe@master

2. Ensure everything is working properly.

.. code-block:: bash

    $ moe --version

*********************
Understanding Plugins
*********************
Before using Moe, you should understand that most of Moe's features are provided by various *plugins*, that each contribute a different way of interacting with the music in your library. For example, the ``edit`` plugin lets you edit your music, while the ``add`` plugin lets you add music to your library. Each of these plugins come with their own set of commands and configuration options.

*************
Configuration
*************
Moe will automatically create a config file, ``config.toml``, in ``$HOME/.config/moe`` or ``%USERPROFILE%\.config\moe`` if you're on Windows. This directory is also where your library database file will reside.

.. note::
    The configuration directory can be overwritten by setting the environment variable ``MOE_config.CONFIG_DIR``.

Throughout this documentation, all configuration options will be displayed in the following format:

``option = default_value``

Overriding Config Values
========================
All configuration parameters can be overridden through environment variables. To override the configuration parameter ``{param}``, use an environment variable named ``MOE_{PARAM}``.

For example, to override the ``asciify_paths`` variable, you can run Moe with:

.. code-block:: bash

    $ MOE_MOVE.ASCIIFY_PATHS="true" moe

.. note::
   Notice since the ``asciify_paths`` option is specific to the ``move`` plugin, we use ``move.library_path`` to access it.

Global Options
==============
Most configuration options reside in their relevant plugin, however there are the following global options:

``default_plugins = ["add", "edit", "info", "ls", "move", "musicbrainz", "rm", "write"]``
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
For plugin specific configuration, see the respective plugin's page. Each plugin option should be specified under that plugin's section in the config.

For example, you may want to ensure when Moe moves your music, it only names files using ascii characters. To do this, we'd check out the ``move`` plugin and find it has the ``asciify_paths`` configuration option. To customize this option, we'd write the following in our config file.

.. code-block:: toml

    [move]
    asciify_paths = true

**********************
Command-Line Interface
**********************
Once you're confident you've configured everything to your liking, you're ready to run Moe.

.. code-block:: bash

    $ moe

The help text of each command should be enough to get you started. For more info, see :doc:`plugins <plugins/plugins>`.
