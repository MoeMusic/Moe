########
Querying
########
Many plugins use a "query" to search for music in your library.

The query must be in the format ``field:value`` where ``field`` is, by default, a :ref:`track's field <fields:Track Fields>` to match and ``value`` is the field's value (case-insensitive). To match an :ref:`album's field <fields:Album Fields>` or an :ref:`extra's field <fields:Extra Fields>`, prepend the field with ``a:`` or ``e:`` respectively. Internally, this ``field:value`` pair is referred to as a single "term".

By default, tracks will be returned by the query, but you can choose to return albums by using the ``-a, --album`` option, or you can return extras using the ``-e, --extra`` option.

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

.. note::
   When querying for a field that supports multiple values, query for one term per value. For example, to query for tracks with the genres 'hip hop' and 'pop', use:

   .. code-block:: bash

       '"genre:hip hop" genre:pop'

.. tip::
    Fields of different types can be mixed and matched in a query string. For example, the query ``--extras 'album:The College Dropout' e:path:%jpg$`` will return any extras with the 'jpg' file extension belonging to the album titled 'The College Dropout'.

.. tip::
    Normal queries may be faster when compared to regular expression queries. If you are experiencing performance issues with regex queries, see if you can make an equivalent normal query using the ``%`` and ``_`` wildcard characters.
