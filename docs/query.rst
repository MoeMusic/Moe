Querying
========
Many plugins use a "query" to search for music in your library.

The query must be in the format ``field:value`` where field is a track or album's field to match and value is that field's value. Internally, this ``field:value`` pair is referred to as a single "term". The match is case-insensitive.

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

    'title:100\%'

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

Note that when using multiple terms, they are joined together using AND logic, meaning all terms must be true to return a match.

If doing an album query, you still specify track fields, but it will match albums instead of tracks.

Tip: Normal queries may be faster when compared to regex queries. If you are experiencing performance issues with regex queries, see if you can make an equivalent normal query using the LIKE wildcard characters.
