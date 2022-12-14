###############
Writing Plugins
###############
In Moe, almost everything is a plugin. Plugins are designed to interact with other plugins primarily through the various :doc:`hooks <api/hooks>` available.

Creating plugins in Moe is extremely simple. For example, below is a plugin that implements the ``create_path_template_func`` hook to add a ``canon_artist`` function for use in path templates.

.. code:: python

    import moe

    @moe.hookimpl
    def create_path_template_func():
        return [canon_artist]

    def canon_artist(artist):
        if artist == "The Jimi Hendrix Experience":
            return "Jimi Hendrix"
        return artist

Plugins can exist either locally in your configuration directory, or you can opt to share your plugin by publishing it to PyPI.

Local Plugins
=============
You can create a local plugin by adding a module ``<plugin_name>.py`` or package ``<plugin_name>/my_module.py`` in a ``plugins`` directory next to your configuration e.g. ``<configuration directory>/plugins/<my_plugin>``.

.. important::
    The name of your local plugin cannot conflict with any other modules in the current namespace. For example, you can't name your plugin ``random`` because it conflicts with the ``random`` module in the standard library. It may be useful to preface any local plugins with ``moe_`` or any other prefix of your choice if you think there may be a potential conflict.

Published Plugins
=================
If you'd like to make your plugin available on pip, there are a few required steps:

#. Preface your project name with ``moe_`` e.g. ``moe_my_plugin`` when publishing to PyPI.

   .. note::
      It's encouraged that the actual name of your plugin module or package not include the ``moe_`` prefix. The prefix is only necessary for the name of your project on PyPI.

#. Include the `entry_point group <https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-package-metadata>`_ ``moe`` in your ``setup.py`` or ``pyproject.toml``.

   * For example, if using *poetry*, include the following in your ``pyproject.toml``.

     .. code:: toml

        [tool.poetry.plugins."moe"]
        "<plugin_name>" = "<plugin_module or package>"

     .. seealso::
        `relevant poetry docs <https://python-poetry.org/docs/master/pyproject/#plugins>`_

Once you've accomplished the above, your plugin will be automatically loaded by Moe provided the user has installed your package and enabled the plugin in their configuration.

For examples of existing third-party plugins, see the :ref:`plugin docs <plugins/plugins:Third-Party Plugins>`.

.. tip::
   Check out the `plugin_template <https://github.com/MoeMusic/plugin_template>`_ repository to quickly create a plugin to publish to PyPI complete with CI scripts and configuration files consistent with the rest of Moe.

Core vs CLI
===========
Because Moe includes both a library as well as a command-line interface to that library, many of the existing plugins are split into two parts: a *core* module and a *cli* module. If your plugin is attempting to affect both parts of Moe, it should also be split accordingly, but can be contained under a single package. In this case, the name of the package should simply be the name of your plugin. When enabling or disabling plugins, users only need to specify the name of the package, and not the individual sub-modules.

Registering Plugin Sub-Modules
------------------------------
If your plugin is a package consisting of one or more sub-modules, they must each be explicitly registered for them to be included in the plugin system. This is a common occurrence if your plugin has both a ``cli`` and ``core`` sub-module, for instance.

When your plugin is loaded by Moe, it is actually just loading its ``__init__.py``. Therefore, the rest of your sub-modules must be explicitly registered for Moe to see them. For example, the ``add`` plugin has the following in its ``__init__.py``:

.. code:: python

    @moe.hookimpl
    def plugin_registration():
        """Only register the cli sub-plugin if the cli is enabled."""
        config.CONFIG.pm.register(add_core, "add_core")
        if config.CONFIG.pm.has_plugin("cli"):
            config.CONFIG.pm.register(add_cli, "add_cli``)

.. seealso::
   The :meth:`~moe.config.Hooks.plugin_registration` hook.
