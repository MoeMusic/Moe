###################
Third-Party Plugins
###################
Moe's functionality can be greatly extended by the use of plugins. Third-party plugins are just plugins that have been published to PyPI and are available for anyone to add to their own setup.

If you'd like to create and publish your own plugin, see the :doc:`writing plugins docs <developers/writing_plugins>`.

Installation
============
To enable any third-party plugin, simply install the plugin per its specific install docs, and then enable it in the ``enable_plugins`` configuration option.

.. note::
   If you installed Moe with pipx, you'll want to "inject" whatever plugin you're installing into Moe with ``pipx inject moe [plugin]``.

Known Plugins
=============
There are currently no known installable, third-party plugins for moe. If you'd like to add your plugin to this list, please submit a pull request.
