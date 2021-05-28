###############
Getting Started
###############

************
Installation
************
Moe *should* work on any platform.

.. important::
    The following will install `Moe` for use in a development environment. `Moe` isn't currently intended for normal use.

#. `Install poetry <https://python-poetry.org/docs/#installation>`_.
#. Clone the repository

    .. code-block:: bash

        $ git clone https://github.com/jtpavlock/moe.git
#. Install the project

    .. code-block:: bash

       $ cd Moe
       $ poetry install
#. Run Moe

    .. code-block:: bash

       $ poetry shell
       $ moe

.. note::
    ``poetry shell`` will enter a virtual environment to interact with the project. To exit, just type ``exit`` in the shell. If you'd like to run ``moe`` or other commands without entering the virtual environment, prepend any commands with ``poetry run``.

    .. code-block:: bash

       $ poetry run moe

.. _General Configuration:

*************
Configuration
*************
Moe will automatically create a config file, ``config.toml``, in ``$HOME/.config/moe`` or ``%USERPROFILE%\.config\moe`` if you're on Windows. This directory is also where your library database file will reside.

Global Options
==============
Most configuration options reside in their relevant plugin, however there is currently one global option:

* ``default_plugins``: Override the list of default plugins.

  * Default: ``["add", "info", "ls", "move, "rm"]``

Plugin Options
==============
For plugin specific configuration, see the respective plugin's page under :doc:`plugins <plugins/plugins>`. Each plugin option should be specified under that plugin's section in the config.

For example, to specify the config option ``library_path`` which is a ``move`` plugin option, we'd write the following in our config:

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
To run moe:

    .. code-block:: bash

       $ moe

The help text of each command should be enough to get you started. For more info, see :doc:`plugins <plugins/plugins>`.
