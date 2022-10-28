############
Contributing
############

Thank you for considering contributing to Moe. The following information is catered to contributing via code, but other forms of contributions are more than welcome!

If you have any questions at all about the below process or contributing in general, please don't hesitate to ask. The best way to do so is by opening a `github discussion <https://github.com/MoeMusic/Moe/discussions/categories/q-a>`_.

********
Overview
********
In short, to contribute code to Moe, you should follow these steps:

#. :ref:`Create a development environment <developers/contributing:Creating a dev environment>`
#. :ref:`Write some code <developers/contributing:Writing Code>`
#. :ref:`Test your code <developers/contributing:Testing>`

   .. code:: bash

        $ pytest -m "not network"
        $ sphinx-build  -q -b html docs ~/src/Moe/docs/_build/html/

#. :ref:`Lint your code <developers/contributing:Linting>`

   .. code:: bash

        $ pre-commit run -a

#. Submit a pull request

**************************
Creating a dev environment
**************************
#. Fork Moe
#. `Install poetry <https://python-poetry.org/docs/#installation>`_
#. Clone the repository

   .. code:: bash

        $ git clone https://github.com/MoeMusic/Moe.git

#. Install the project

   .. code:: bash

        $ cd Moe
        $ poetry install

#. Run Moe

   .. code:: bash

        $ poetry shell
        $ moe

   .. note::
        ``poetry shell`` will enter a virtual environment to interact with the project. To exit, just type ``exit`` in the shell. If you'd like to run ``moe`` or other commands without entering the virtual environment, prepend any commands with ``poetry run``.

************
Writing Code
************

Committing
==========
There are strict commit guidelines to follow in order to keep a clean and useful git history, as well as to automatically generate our changelog. Commits should be atomic i.e. they can exist on their own and only consist of a single feature, bug fix, etc.

Moe follows `conventional commits <https://www.conventionalcommits.org/en/v1.0.0/#summary>`_. In short, all of your commits should look like the following:

.. code::

    <type>[optional scope]: <description>

    [optional body]

    [optional footer(s)]

Type
----
The type should be one of the following:

* ``build``: Changes that affect the build system or external dependencies.
* ``ci``: Changes to our CI configuration files and scripts.
* ``deprecate``: Deprecations of API elements.
* ``docs``: Documentation only changes.
* ``feat``: A new feature.
* ``fix``: A bug fix.
* ``perf``: A code change that improves performance.
* ``refactor``: A code change that neither fixes a bug nor adds a feature.
* ``style``: Changes that do not affect the meaning of the code (white-space, formatting, etc).
* ``test``: Adding missing tests or correcting existing tests.

.. note::
   If the commit introduces a breaking change, then the type and scope should be followed with an exclamation mark e.g. ``feat(add)!: new breaking change``.

Scope
-----
The scope is optional, but generally should just be the name of a plugin if the change is specific to a single plugin.

Description
-----------
The description should be present tense, not capitalized, and have no punctuation at the end. This is what will be displayed in the changelog.

Body
-----
The body should include amplifying information on the change both for users looking at the commit from the changelog, as well as developers to understand the change. Including a body is always encourage, but only mandatory if the commit introduces a breaking change.

Footer
-------
The footer should include references to any relevant issues or other information. If resolving an issue, prepend the issue with 'fixes' (`or other supported keywords <https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword>`_) e.g. ``Fixes #1234``.

Migrations
==========
Moe uses `alembic <https://alembic.sqlalchemy.org/en/latest/ops.html>`_ for its database migrations. If your code change requires a database migration, use the following steps:

#. Autogenerate the initial migration script.

   .. code:: bash

       $ alembic revision --autogenerate -m "<description of the change>"

   .. important::

      You must be in the ``Moe/alembic`` directory for this command to work.

#. Adjust the auto-generated script as necessary.

   * The script will be under ``Moe/alembic/versions``.

That's it! For more information regarding migrations, reference the `alembic docs <https://alembic.sqlalchemy.org/en/latest/ops.html>`_. Moe will automatically upgrade or downgrade each user's database the next time the program is run.

New Field Checklist
===================
If adding a new field to Moe, the following checklist can help ensure you cover all your bases:

#. Add the database column to the appropriate library class (``Album``, ``Extra``, or ``Track``).
   * If the field represents metadata and does not deal with the filesystem, also add to the appropriate ``Meta`` class (``MetaAlbum`` or ``MetaTrack``).
   * If a multi-value field, add the non-plural equivalent property. See ``Track.genres`` and the accompanying single-value field, ``Track.genre`` for an example.
   * Include documentation for the new field in the class docstring(s).

#. Add to the item's ``fields`` method as necessary.
#. Add code for reading the tag from a track file under ``Track.read_custom_tags``.

   * Add tests under ``test_track.py:TestFromFile:test_read_tags()``

#. Add code for writing the tag to a track file under ``write.write_custom_tags``.

   * Add tests under ``test_write.py:TestWriteTags:test_write_tags()``

#. Read/load from the field from musicbrainz as necessary.

   * See ``mb_core.py:_create_album()``
   * Is it possible a musicbrainz release may not contain this field? Use safe dict access if necessary.
   * Add to the ``album`` function in ``tests/plugins/musicbrainz/full_release.py`` to test parsing the new field from a musicbrainz release.

#. Add a weight for how much the field should factor into matching a track or album to another track or album in ``moe/util/core/match.py:MATCH_<TRACK/ALBUM>_FIELD_WEIGHTS``.
#. Include documentation for your new field in ``docs/fields.rst``
#. Create a migration script for your new field.

*******
Testing
*******

Writing Tests
=============
With *very* few exceptions, any new feature or bug fix should include accompanying tests.

What to test
------------
At a minimum, every public function/method should be tested. This includes hook specifications and implementations.

.. note::

    If there are no public functions in your code change, then test the public interface into the module. For example, cli plugins are tested by running ``main`` with the appropriate arguments.

Test structure
--------------
Each module should correspond to a single test module, and each public function and hook implementation gets its own test class. Hook specifications can be combined into a single class.

Style/Conventions
-----------------
* `pytest <https://docs.pytest.org/en/latest/contents.html>`_ is used to write tests and should be used over the standard library `unittest <https://docs.python.org/3/library/unittest.html>`_. The only exception is when it comes to mocking. Use ``unittest.mock`` over ``pytest-mock`` or other alternatives.
* Any tests that require internet connection i.e. make a network call should be marked with the ``network`` marker.

  .. code:: python

   @pytest.mark.network
   def test_external_api():
       make_network_call()
* Any tests specific to an operating system should use one of the following markers:

  * ``@pytest.mark.darwin`` - MacOS
  * ``@pytest.mark.linux`` - Linux
  * ``@pytest.mark.win32`` - Windows

*******
Linting
*******
`pre-commit <https://pre-commit.com/>`_ is used to test the various linters set up. If you'd like to automatically run the linters on each commit, you can 'install' ``pre-commit``:

.. code::

    $ pre-commit install

Otherwise, to manually run all the checks:

.. code::

    $ pre-commit run -a

``pre-commit`` will run the following checks:

* `black <https://github.com/psf/black>`_ - used to keep a consistent code format.
* `flake8 <https://github.com/PyCQA/flake8>`_ - used to check for various stylistic rules. See ``setup.cfg`` for an overview on the various rules encompassed by this check.
* `isort <https://github.com/PyCQA/isort>`_ - used for sorting imports in modules.
* `pyright <https://github.com/microsoft/pyright>`_ - used for type checking.
