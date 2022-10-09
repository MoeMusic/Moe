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

.. toctree::
   :maxdepth: 4

   hooks
   cli
   core
