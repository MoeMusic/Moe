######
Fields
######

These are the fields Moe keeps track of for tracks, albums, and extras in your library.

.. note::
    Some track fields are actually on a per-album basis, and are just a mapping to the related album field e.g. ``albumartist`` or ``album``. These fields are exposed as track fields for convenience and due to convention.

.. _Track Fields:

.. csv-table:: Track Fields
    :header: "Field", "Description", "Notes"
    :widths: 20, 50, 50

    "album", "Album title", ""
    "albumartist", "Album artist", ""
    "artist", "Track artist", ""
    "date", "Album release date", "YYYY-MM-DD format"
    "disc", "Disc number", ""
    "disc_total", "Number of discs in the album", ""
    "genre", "Genre", "Supports multiple values"
    "mb_album_id", "Musicbrainz album release ID", ""
    "mb_track_id", "Musicbrainz release track ID", ""
    "path", "Filesystem path of the track", ""
    "title", "Track title", ""
    "track_num", "Track number", ""
    "year", "Album release year", ""

.. csv-table:: Album Fields
    :header: "Field", "Description", "Notes"
    :widths: 20, 50, 50

    "artist", "Album artist", ""
    "date", "Album release date", "YYYY-MM-DD format"
    "disc_total", "Number of discs in the album", ""
    "mb_album_id", "Musicbrainz album release ID", ""
    "path", "Filesystem path of the album", ""
    "title", "Album title", ""
    "year", "Album release year", ""

.. csv-table:: Extra Fields
    :header: "Field", "Description", "Notes"
    :widths: 20, 50, 50

    "path", "Filesystem path of the extra", ""