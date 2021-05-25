Getting Started
===============

Installation
------------
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

General Configuration
---------------------
Moe will automatically create a config file, ``config.toml``, in ``$HOME/.config/moe`` or ``%USERPROFILE\.config\moe`` if you're on Windows. This directory is also where your library database file will reside. There are currently just a few configuration options:

* ``library_path``: Tells Moe where to copy your added music to.

  * Default: ``"~/Music"``

    .. code-block:: text

       library_path = "~/Music"

    If you're on Windows, you need to use a raw string by enclosing your library path in triple-single quotes.

    .. code-block:: text

       library_path = '''~\Music'''
* ``default_plugins``: Override the list of default plugins.

  * Default: ``["add", "info", "ls", "rm"]``

    .. code-block:: text

       default_plugins = ["add", "rm"]

For plugin specific configuration, see the respective plugin's page under :doc:`plugins <plugins/index>`.

Command-Line Interface
----------------------
To run moe:

    .. code-block:: bash

       $ moe

The help text of each command should be enough to get you started. For more info, see :doc:`plugins <plugins/index>`.
