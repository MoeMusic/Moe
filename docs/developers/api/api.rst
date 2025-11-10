###
API
###

.. important::
    Moe follows `semantic versioning <https://semver.org/>`_.

There's a couple of things you should understand about Moe's underlying API layout.

#. CLI vs Core
    Moe's codebase is shared by both the command-line interface portion and the underlying core functionality. Because of this, there are technically two different APIs that are split accordingly.
#. Hooks
    The API also consists of *hooks*, which are the primary interface for plugin integration into Moe. Hooks allow you to extend the functionality of plugins and keeps plugins as isolated as possible from each other. If you're developing a plugin, you should be using these hooks the majority of the time, while the core API exists primarily to allow clients or other programs to interact with Moe.

Using the API in other programs
===============================
As illustrated :ref:`in the usage docs <index:Usage>`, Moe's suite of music management functions can be utilized in external programs without requiring a database of music. Obviously, in this case, you can't utilize any functions that require a database ``session``.

The only requirement is to have or create a configuration file and initialize the configuration in your program. For example, your script should include something like the following:

.. code:: python

    from pathlib import Path
    from moe import config

    try:
        config.Config(config_dir=Path.home() / ".config" / "my_script", init_db=False)
    except config.ConfigValidationError as err:
        raise SystemExit(1) from err

A ``config.toml`` file will then be created in the configuration directory specified which you can use to change Moe's behavior, or add your own configuration options.

.. important::
   Ensure to pass the ``init_db=False`` parameter to tell Moe you don't want to use the database.

Any custom configuration options added can be accessed just like any other configuration value. For example, if you added a section to the configuration called ``my_script``, you could access any values via the following:

.. code:: python

    config.CONFIG.settings.my_script.my_setting

Allowing Moe to handle all of the configuration and music managament logic can help greatly simplify your program.

API Definitions
===============

.. toctree::
   :maxdepth: 3

   hooks
   cli
   core
