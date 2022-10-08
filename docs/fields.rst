######
Fields
######

These are the fields Moe keeps track of for tracks, albums, and extras in your library.

.. note::
    Some track fields are actually on a per-album basis, and are just a mapping to the related album field e.g. ``albumartist`` or ``album``. These fields are exposed as track fields for convenience and due to convention.

************
Track Fields
************
.. csv-table::
    :header: "Field", "Description", "Notes"
    :widths: 4, 10, 1
    :width: 100%

    "album", "Album title", ""
    "albumartist", "Album artist", ""
    "artist", "Track artist", ""
    "artists", "Set of track artists.", "1"
    "disc", "Disc number", ""
    "genre", "Genre", "1"
    "path", "Filesystem path of the track", ""
    "title", "Track title", ""
    "track_num", "Track number", ""

************
Album Fields
************
.. csv-table::
    :header: "Field", "Description", "Notes"
    :widths: 4, 10, 1
    :width: 100%

    "artist", "Album artist", ""
    "country", "Country the album was released in (two character identifier).", ""
    "date", "Album release date", "2"
    "disc_total", "Number of discs in the album", ""
    "label", "Album release label.", ""
    "media", "Album release format (e.g. CD, Digital, etc.)", ""
    "original_date", "Date of the original release of the album.", "2"
    "original_year", "Year of the original release of the album.", ""
    "path", "Filesystem path of the album", ""
    "title", "Album title", ""
    "year", "Album release year", ""

************
Extra Fields
************
.. csv-table::
    :header: "Field", "Description", "Notes"
    :widths: 4, 10, 1
    :width: 100%

    "path", "Filesystem path of the extra", ""

*****
Notes
*****
1. Supports multiple values.
2. Edit and query using YYYY-MM-DD format.

*************
Custom Fields
*************
In addition to the above fields, plugins may add any number of custom fields to Moe. These fields don't behave any differently i.e. they can be queried, edited, accessed, etc, the same as any normal field. You can check each plugin's documentation for more information on the custom fields they expose.
