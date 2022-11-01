######
Fields
######

These are the fields Moe keeps track of for tracks, albums, and extras in your library.

.. note::
    Some track fields are actually on a per-album basis, and are just a mapping to the related album field e.g. ``albumartist`` or ``album``. These fields are exposed as track fields for convenience and due to convention.

************
Track Fields
************
* ``album`` - album title
* ``albumartist`` - album artist
* ``artist`` - track artist
* ``artists`` - track artists [#f1]_
* ``disc`` - disc number
* ``genre`` - genre [#f1]_
* ``path`` - filesystem path of the track [#f3]_
* ``title`` - track title
* ``track_num`` - track number

************
Album Fields
************
* ``artist`` - album artist
* ``barcode`` - UPC barcode
* ``catalog_num`` - catalog numbers of the album [#f1]_
* ``country`` - country the album was released in (two character identifier)
* ``date`` - album release date [#f2]_
* ``disc_total`` - number of discs in the album
* ``label`` - album release label
* ``media`` - album release format (e.g. CD, Digital, etc.)
* ``original_date`` - date of the original release of the album [#f2]_
* ``original_year`` - year of the original release of the album [#f3]_
* ``path`` - filesystem path of the album [#f3]_
* ``title`` - album title
* ``track_total`` - number of tracks an album *should* have, not necessarily the number of tracks an album has in Mo
* ``year`` - album release year

************
Extra Fields
************
* ``filesystem`` - path of the extra [#f3]_

.. rubric:: Footnotes

.. [#f1] Supports multiple values.
.. [#f2] Edit and query using YYYY-MM-DD format.
.. [#f3] Read-only (cannot be edited).

*************
Custom Fields
*************
In addition to the above fields, plugins may add any number of custom fields to Moe. These fields don't behave any differently i.e. they can be queried, edited, accessed, etc, the same as any normal field. You can check each plugin's documentation for more information on the custom fields they expose.
