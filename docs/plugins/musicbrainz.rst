###########
Musicbrainz
###########

The ``musicbrainz`` plugin provides the following functionality:

* Imports metadata from musicbrainz when adding a track or album to the library.
* Sync releases in your library with a musicbrainz collection.

  * Optionally updates the collection when items are added or removed from the library.
  * Commandline option to manually set, add to, or remove releases from the collection.

*************
Configuration
*************
The ``musicbrainz`` plugin is enabled by default.

``username``
    Musicbrainz username.
``password``
    Musicbrainz password.

Collections
===========
The following options involve auto updating a specific collection on musicbrainz, and should be specified under a ``musicbrainz.collection`` block as shown:

.. code-block:: toml

    [musicbrainz.collection]
    collection_id = "123"

.. important::

    Utilizing any of the collections functionality requires setting your musicbrainz username and password as described above.

``collection_id``
    Musicbrainz collection to automatically update.

``auto_add = False``
    Whether to automatically add new releases in the library to the collection defined in ``collection_id``.

``auto_remove = False``
    Whether to automatically remove releases from ``collection_id`` when removed from the library.

***********
Commandline
***********
The musicbrainz plugin adds a single command, ``mbcol``, used to sync a musicbrainz collection with musicbrainz releases in the library. The collection synced is the one specified under ``collection_id`` in the user config.

.. code-block:: bash

    moe mbcol [-h] [-a | -e] [--add | --remove] query

By default, the musicbrainz collection will be set to the releases found in the queried items. If tracks or extras are queried, their associated album releases will be synced with the collection.

Options
=======
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

Arguments
=========
``query``
    Query your library for items to sync your collection with. See the :doc:`query docs <../query>` for more info.

*************
Custom Fields
*************

Track Fields
============
.. csv-table::
    :header: "Field", "Description", "Notes"
    :widths: 4, 10, 6
    :width: 100%

    "mb_track_id", "Musicbrainz track id", ""

Album Fields
============
.. csv-table::
    :header: "Field", "Description", "Notes"
    :widths: 4, 10, 6
    :width: 100%

    "mb_album_id", "Musicbrainz album aka release id", ""
