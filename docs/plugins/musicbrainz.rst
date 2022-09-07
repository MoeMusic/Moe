###########
Musicbrainz
###########

The ``musicbrainz`` plugin provides the following functionality:

* Imports metadata from musicbrainz when adding a track or album to the library.
* Optionally updates a musicbrainz collection when items are added or removed from the library.

*************
Configuration
*************
The ``musicbrainz`` plugin is enabled by default.

``username``
    Musicbrainz username.
``password``
    Musicbrainz password.

Collections
-----------
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
