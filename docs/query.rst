########
Querying
########
Many plugins use a "query" to search for music in your library.

The query must be in the format ``field:value`` where field is a :ref:`track's field <Track Fields>` to match and value is that field's value. Internally, this ``field:value`` pair is referred to as a single "term". The match is case-insensitive.

Album queries, specified with the ``-a, --album`` option, will return albums that contain any tracks matching the given query. Similarly, querying for extras, specified with the ``-e, --extra`` option, will return extras that are attached to albums that contain any tracks matching the given query.

If you would like to specify a value with whitespace or multiple words, enclose the
term in quotes.

.. code-block:: bash

    'title:Hip Hop Hooray'

`SQL LIKE <https://www.w3schools.com/sql/sql_like.asp>`_ query syntax is used for normal queries, which means
the ``_``  and ``%`` characters have special meaning:

* ``%`` - The percent sign represents zero, one, or multiple characters.
* ``_`` - The underscore represents a single character.

To match these special characters as normal, use ``/`` as an escape character.

.. code-block:: bash

    'title:100/%'

The value can also be a regular expression. To enforce this, use two colons
e.g. ``field::value.*``

.. code-block:: bash

    'title::[a-m].*'

As a shortcut to matching all entries, use ``*`` as the term.

.. code-block:: bash

    '*'

Finally, you can also specify any number of terms.
For example, to match all Wu-Tang Clan tracks that start with the letter 'A', use:

.. code-block:: bash

    '"artist:wu-tang clan" title:a%'

.. note::
    When using multiple terms, they are joined together using AND logic, meaning all terms must be true to return a match.

.. tip::
    Normal queries may be faster when compared to regular expression queries. If you are experiencing performance issues with regex queries, see if you can make an equivalent normal query using the LIKE wildcard characters.

****************
Supported Fields
****************

In addition to the :ref:`track fields <Track Fields>`, the following fields are also available to query:

* ``album_path`` Path of an album directory.
* ``extra_path`` Path of an extra.

.. note::
   When querying for a field that supports multiple values, query for one term per value. For example, to query for tracks with the genres 'hip hop' and 'pop', use:

.. code-block:: bash

    '"genre:hip hop" genre:pop'
