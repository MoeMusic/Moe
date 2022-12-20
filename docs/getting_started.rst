###############
Getting Started
###############

************
Installation
************
Moe requires python 3.9 or greater.

#. The latest release of Moe is available on `PyPI <https://pypi.org/project/moe>`_

   .. code-block:: bash

       $ pip install moe

#. Ensure everything is working properly.

   .. code-block:: bash

       $ moe --version

*********************
Understanding Plugins
*********************
Before using Moe, you should understand that most of Moe's features are provided by various *plugins* that each contribute a different way of interacting with the music in your library. For example, the ``edit`` plugin lets you edit your music, while the ``add`` plugin lets you add music to your library. Each of these plugins come with their own set of commands and configuration options.

There also exist external or third-party plugins that extend the functionality of Moe even further. See :doc:`the third-party plugins docs <third_party_plugins>` for more information.

*********
Now what?
*********
The first step is configuring Moe to your liking. To do this, check out the :doc:`configuration docs <configuration>`.

.. note::

   Moe doesn't ship with any metadata source connections by default. If you'd like to import metadata from online sources such as Musicbrainz, you'll have to install a third-party plugin.

Once you're satisfied with everything, you can start using Moe! For normal users, check out the :doc:`command-line interface docs <cli>` to interact with and start adding music to your music library. If you're a developer, check out the relevant :doc:`developer docs <developers/developers>`.
