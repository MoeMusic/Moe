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
    "artists", "Set of track artists", "1"
    "audio_format", "File audio_format. One of ['aac', 'aiff', 'alac', 'ape',
            'asf', 'dsf', 'flac', 'ogg', 'opus', 'mp3', 'mpc', 'wav', 'wv']", ""
    "disc", "Disc number", ""
    "genre", "Genre", "1"
    "path", "Filesystem path of the track", "3"
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
    "barcode", "UPC barcode", ""
    "catalog_num", "Catalog numbers of the album.", "1"
    "country", "Country the album was released in (two character identifier)", ""
    "date", "Album release date", "2"
    "disc_total", "Number of discs in the album", ""
    "label", "Album release label", ""
    "media", "Album release format (e.g. CD, Digital, etc.)", ""
    "original_date", "Date of the original release of the album", "2"
    "original_year", "Year of the original release of the album", "3"
    "path", "Filesystem path of the album", ""
    "title", "Album title", ""
    "track_total", "Number of tracks an album *should* have, not necessarily the number of tracks an album has in Moe.", ""
    "year", "Album release year", "3"

************
Extra Fields
************
.. csv-table::
    :header: "Field", "Description", "Notes"
    :widths: 4, 10, 1
    :width: 100%

    "path", "Filesystem path of the extra", "3"

*****
Notes
*****
1. Supports multiple values.
2. Edit and query using YYYY-MM-DD format.
3. Read-only (cannot be edited).

*************
Custom Fields
*************
In addition to the above fields, plugins may add any number of custom fields to Moe. These fields don't behave any differently i.e. they can be queried, edited, accessed, etc, the same as any normal field. You can check each plugin's documentation for more information on the custom fields they expose.
