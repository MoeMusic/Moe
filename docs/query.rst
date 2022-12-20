########
Querying
########
Many plugins use a "query" to search for music in your library.

The query must be in the format ``field:value`` where ``field`` is, by default, a :ref:`track's field <fields:Track Fields>` to match and ``value`` is the field's value (case-insensitive). To match an :ref:`album's field <fields:Album Fields>` or an :ref:`extra's field <fields:Extra Fields>`, prepend the field with ``a:`` or ``e:`` respectively. Internally, this ``field:value`` pair is referred to as a single "term".

.. note::

    Some fields such as a track's ``audio_format`` cannot be queried and are noted as such in :ref:`the field docs <fields:Fields>`.

By default, tracks will be returned by the query, but you can choose to return albums by using the ``-a, --album`` option, or you can return extras using the ``-e, --extra`` option.

Normal Queries
==============
If you would like to specify a value with whitespace or multiple words, enclose the
term in quotes.

.. code-block:: bash

    'title:Hip Hop Hooray'

.. important::

   If specifying a query with spaces on the command-line, you'll need two sets of quotes since the first set simply delineates the argument from others and doesn't retain the spaces in the term. For example, if executing the above query using the ``ls`` command, you should write the following:

   .. code-block:: bash

       moe ls "'title:Hip Hop Hooray'"

   For powershell users, it's necessary to use ``"`` as the outer quotes.

.. note::
   When querying for a field that supports multiple values, query for one term per value. For example, to query for tracks with the genres 'hip hop' and 'pop', use:

   .. code-block:: bash

       "'genre:hip hop' genre:pop"

Numeric Range Queries
=====================
Queries on numeric fields can specify an acceptable range. To do this, specify the range by using two dots ``..`` in the beginning, middle, or end of the value. Dots in the beginning let you specifiy a minimum e.g. ``1..``, dots and the end let you specify a maximum e.g. ``..10``, and dots in the middle let you specify a range e.g. ``1..10``.

For instance, the following will query for any albums released between 2010 and 2020:

.. code-block::

    "a:year:2010..2020"

Whereas this query will find any albums released prior to 2020:

.. code-block::

    "a:year:..2020"

And finally, this query will find any albums released after 2010:

.. code-block::

    "a:year:2010.."

.. note::

   Query ranges are *inclusive* i.e. items matching the minimum or maximum value will also be included.

SQL Like Queries
================
`SQL LIKE <https://www.w3schools.com/sql/sql_like.asp>`_ query syntax is used for normal queries, which means
the ``_``  and ``%`` characters have special meaning:

* ``%`` - The percent sign represents zero, one, or multiple characters.
* ``_`` - The underscore represents a single character.

To match these special characters as normal, use ``/`` as an escape character.

.. code-block:: bash

    'title:100/%'

Regular Expression Queries
==========================
The value can also be a regular expression. To enforce this, use two colons
e.g. ``field::value.*``

.. code-block:: bash

    'title::[a-m].*'

As a shortcut to matching all entries, use ``*`` as the term.

.. code-block:: bash

    '*'

.. tip::
    Normal queries may be faster when compared to regular expression queries. If you are experiencing performance issues with regex queries, see if you can make an equivalent normal query using the ``%`` and ``_`` wildcard characters.

Multiple Query Terms
====================
You can also specify any number of terms.
For example, to match all Wu-Tang Clan tracks that start with the letter 'A', use:

.. code-block:: bash

    "'artist:wu-tang clan' title:a%"

.. note::
    When using multiple terms, they are joined together using AND logic, meaning all terms must be true to return a match.

.. tip::
    Fields of different types can be mixed and matched in a query string. For example, the query ``--extras 'album:The College Dropout' e:path:%jpg$`` will return any extras with the 'jpg' file extension belonging to the album titled 'The College Dropout'.
