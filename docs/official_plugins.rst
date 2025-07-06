:tocdepth: 3

################
Official Plugins
################

Official plugins are supported by the MoeMusic team and are included as optional extras within Moe.

Musicbrainz
===========
This is a plugin for Moe utilizing the musicbrainz metadata source and provides the following features:

* Musicbrainz as an import souce.
* Update musicbrainz collections automatically on import or manually.
* Various API functions.

Installation
************
1. Install via pipx

   .. code-block:: bash

       $ pipx install moe[musicbrainz]

Configuration
*************
Add ``musicbrainz`` to the ``enabled_plugins`` configuration option.

This plugin has the following configuration options:

``username``
    Musicbrainz username.
``password``
    Musicbrainz password.
``search_limit = 5``
    Maximum number of search results to return when searching for candidate albums from MusicBrainz. Must be at least 1. Defaults to 5.

Collections
~~~~~~~~~~~
The following options involve auto updating a specific collection on musicbrainz, and should be specified under a ``musicbrainz.collection`` block as shown:

.. code-block:: toml

    [musicbrainz.collection]
    collection_id = "123"

.. important::

    Utilizing any of the collections functionality requires setting your musicbrainz username and password as described above.

``collection_id``
    Musicbrainz collection to automatically update.

``auto_add = false``
    Whether to automatically add new releases in the library to the collection defined in ``collection_id``.

``auto_remove = false``
    Whether to automatically remove releases from ``collection_id`` when removed from the library.

Custom Fields
*************
This plugin adds the following custom fields:

Track Fields
~~~~~~~~~~~~
* ``mb_track_id`` - musicbrainz track id

Album Fields
~~~~~~~~~~~~
* ``mb_album_id`` - musicbrainz album aka release id

Command-line Interface
**********************
This plugin adds the following commands:

mbcol
~~~~~
Used to sync a musicbrainz collection with musicbrainz releases in the library. The collection synced is the one specified under ``collection_id`` in the user config.

.. code-block:: bash

    moe mbcol [-h] [-a | -e] [--add | --remove] query

By default, the musicbrainz collection will be set to the releases found in the queried items. If tracks or extras are queried, their associated album releases will be synced with the collection.

Positional Arguments
~~~~~~~~~~~~~~~~~~~~
``query``
    Query your library for items to sync your collection with. See the Moe query docs for more info.

Optional Arguments
~~~~~~~~~~~~~~~~~~
``-h, --help``
    Display the help message.
``-a, --album``
    Query for matching albums instead of tracks.
``-e, --extra``
    Query for matching extras instead of tracks.
``--add``
    Add releases to the collection.
``--remove``
    Remove releases from the collection.

API
***
``moe.plugins.musicbrainz``

.. automodule:: moe.plugins.musicbrainz.mb_core
   :members:
   :show-inheritance:

Transcode
=========
This is a plugin for Moe that provides functionality for transcoding music.

Currently only flac -> mp3 [v0, v2, 320] is supported.

Installation
************
1. `Install ffmpeg <https://ffmpeg.org/download.html>`_

   .. important::

      Ensure ``ffmpeg`` is in your OS's path environment variable.

Configuration
*************
Add ``transcode`` to the ``enabled_plugins`` configuration option.

This plugin has the following configuration options:

``transcode_path = {library_path}/transcode``
    The default path for transcoded files.

API
***
``transcode``

.. automodule:: moe.plugins.transcode
   :members:
   :show-inheritance:
