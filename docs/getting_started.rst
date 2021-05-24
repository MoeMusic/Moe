Getting Started
===============

Installation
------------
Moe *should* work on any platform.

#. `Install poetry <https://python-poetry.org/docs/#installation>`_.
#. Clone the repository

    .. code-block:: bash

        $ git clone https://github.com/jtpavlock/moe.git
#. Install the project

    .. code-block:: bash

       $ cd moe
       $ poetry install
#. Run Moe

    .. code-block:: bash

       $ moe

.. _General Configuration:

General Configuration
---------------------
Moe will automatically create a config file, ``config.toml`` in ``$HOME/.config/moe`` or ``%USERPROFILE\.config\moe`` if you're on Windows. This directory is also where your library database file will reside. There are currently just a few configuration options:

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
