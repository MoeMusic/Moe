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
Below is a list of known third-party plugins for Moe. If you'd like to add your plugin to this list, please submit a pull request.

* `musicbrainz <https://moe-musicbrainz.readthedocs.io/en/latest/>`_ - Musicbrainz integration.
* `transcode <https://moe-transcode.readthedocs.io/en/latest/>`_ - API functions for transcoding music in your library.
