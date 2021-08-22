###
API
###

There's a couple of things you should understand about Moe's underlying API layout.

1. CLI vs Core
    Moe's codebase is currently shared by both the comandline interface portion, and the underlying core functionality. Because of this, there are technically two different APIs that are split accordingly.
2. Hooks
    The API also consists of *hooks*, which are the primary interface for plugin integration into Moe. If you're developing a plugin, you should only be using the API hooks the majority of the time. There are exceptions to this, but using hooks help keep plugins as isolated as possible from each other. If you're developing a client, you should use interact with the actual API directly. For example, the commandline interface of Moe uses the underlying API and not the hooks.

.. warning::
    While Moe is in version ``0.X.Y``, the api should be considered unstable.

.. toctree::
   :maxdepth: 4

   hooks
   cli
   core
