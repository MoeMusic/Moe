:tocdepth: 2

######
Fields
######

These are the fields Moe keeps track of for tracks, albums, and extras in your library.

************
Track Fields
************
* ``artist`` - track artist
* ``artists`` - track artists [#f1]_
* ``audio_format`` - aac, aiff, alac, ape, asf, dsf, flac, ogg, opus, mp3, mpc, wav, or wv [#f3]_ [#f4]_
* ``bit_depth`` - number of bits per sample in the audio encoding [#f3]_ [#f4]_
* ``disc`` - disc number
* ``genre`` - genre [#f1]_
* ``path`` - filesystem path of the track [#f3]_
* ``sample_rate`` - sample rate of the track in Hz [#f3]_ [#f4]_
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
* ``path`` - filesystem path of the extra [#f3]_

.. rubric:: Footnotes

.. [#f1] Supports multiple values.
.. [#f2] Edit and query using YYYY-MM-DD format.
.. [#f3] Read-only (cannot be edited).
.. [#f4] Cannot be queried.

*************
Custom Fields
*************
In addition to the above fields, plugins may add any number of custom fields to Moe. These fields can be edited, queried, etc. the same as normal fields.
