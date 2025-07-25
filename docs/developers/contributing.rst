:tocdepth: 3

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

        $ tox run-parallel

#. :ref:`Submit a pull request <developers/contributing:Submitting Pull Requests>`

**************************
Creating a dev environment
**************************
#. Fork Moe
#. `Install poetry <https://python-poetry.org/docs/#installation>`_
#. Clone the repository

   .. code:: bash

        $ git clone https://github.com/MoeMusic/Moe.git

#. Install the project and any extra plugin dependencies

   .. code:: bash

        $ cd Moe
        $ poetry install --all-extras

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
The body should include amplifying information on the change both for users looking at the commit from the changelog, as well as developers to understand the change. This is especially important for any breaking changes.

Footer
-------
The footer should include references to any relevant issues, discussions, pull requests, or other information. If resolving an issue, prepend the issue with 'fixes' (`or other supported keywords <https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword>`_). For example:

   .. code:: markdown

      feat(add): cool new command

      This new command allows to you to do this one very cool specific thing.

      Fixes #345
      See #987 for more discussion

.. _migrations:

Migrations
==========
Moe uses `alembic <https://alembic.sqlalchemy.org/en/latest/ops.html>`_ for its database migrations. If your code change requires a database migration, use the following steps:

#. Autogenerate the initial migration script.

   .. code:: bash

       $ cd Moe/moe/moe_alembic
       $ alembic revision --autogenerate -m "<description of the change>"

#. Adjust the auto-generated script as necessary.

   * The script will be under ``Moe/moe/moe_alembic/versions``.

That's it! For more information regarding migrations, reference the `alembic docs <https://alembic.sqlalchemy.org/en/latest/ops.html>`_. Moe will automatically upgrade or downgrade each user's database the next time the program is run.

New Field Checklist
===================
If adding a new field to Moe, the following checklist can help ensure you cover all your bases:

#. Add the database column to the appropriate library class (``Album``, ``Extra``, or ``Track``).

   * If the field represents metadata and does not deal with the filesystem, also add to the appropriate ``Meta`` class (``MetaAlbum`` or ``MetaTrack``).
   * If creating a multi-value field, add the non-plural equivalent property. See ``Track.genres`` and the accompanying single-value field, ``Track.genre`` for an example.
   * Include documentation for the new field in the class docstring(s).
#. Add the new field to the appropriate library item's ``__init__`` method.

   * If the field represents metadata and does not deal with the filesystem, also add to the appropriate ``Meta`` class (``MetaAlbum`` or ``MetaTrack``).
   * Add tests for constructing an item with the new field in the appropriate test file's ``TestInit`` and ``TestMetaInit`` classes.
#. Add to the item's ``fields`` method as necessary.
#. Add code for reading the tag from a track file under ``Track.read_custom_tags``.
#. Add code for writing the tag to a track file under ``write.write_custom_tags``.

   * Add tests under ``test_write.py:TestWriteTags:test_write_tags()``

#. Add a weight for how much the field should factor into matching a track or album to another track or album in ``moe/util/core/match.py:MATCH_<TRACK/ALBUM>_FIELD_WEIGHTS``.
#. Include documentation for your new field in ``docs/fields.rst``
#. Create a :ref:`migration script <migrations>` for your new field.

*******
Testing
*******

Writing Tests
=============
With *very* few exceptions, any new feature or bug fix should include accompanying tests.

What to test
------------
At a minimum, every public function/method should be tested. This includes hook specifications and implementations.

Non-public functions/methods should generally *not* be tested directly in order to maintain flexibility for these functions to be refactored without breaking tests. Instead, test the public interface that uses the non-public function. For example, cli plugins are tested by running ``main`` with the appropriate arguments.

Test structure
--------------
Each module should correspond to a single test module, and each public function and hook implementation gets its own test class. Hook specifications can be combined into a single class.

Style/Conventions
-----------------
* `pytest <https://docs.pytest.org/en/latest/contents.html>`_ is used to write tests and should be used over the standard library `unittest <https://docs.python.org/3/library/unittest.html>`_. The only exception is when it comes to mocking. Use ``unittest.mock`` over ``pytest-mock`` or other alternatives.
* Any tests specific to an operating system should use one of the following markers:

  * ``@pytest.mark.darwin`` - MacOS
  * ``@pytest.mark.linux`` - Linux
  * ``@pytest.mark.win32`` - Windows
* Tests that require ffmpeg should use the ``pytest.mark.ffmpeg`` marker.
* Tests that require internet access should use the ``pytest.mark.network`` marker.

Running Tests
=============
When you've finished writing your tests, you'll want to make sure everything works:

.. code::

    $ tox run -e test

.. note::

   This runs pytest within tox. To pass arguments to pytest, use `--` followed by the pytest args. For example::

     $ tox run -e test -- -m "not ffmpeg"

.. important::

   To exclude certain tests, such as those that require `ffmpeg` to be installed, use the `-m` argument as shown above.

Once that passes, the next step is to check against all python versions Moe supports, as well as run the documentation and `lint <#linting>`_ checks.

.. code::

    $ tox run-parallel

.. important::
   Tox will only be able to use python versions you have installed already. The easiest way to install multiple python versions is to use `pyenv <https://github.com/pyenv/pyenv>`_.

.. tip::
   If you only want to run specific checks, such as the unit tests for a specific python version, or just the lint or documentation tests, you can specify the test "environment" with ``tox run -e [env]``. For example:

   .. code::

      $ tox run -e py313-test

   Which will run all unit tests with python 3.13. For a list of all possible environments you can use, run ``tox -l``.

Linting
-------
.. code::

    $ tox run -e lint

Runs the following checks:

* `ruff <https://docs.astral.sh/ruff/>`_ used for linting and formatting
* `pyright <https://github.com/microsoft/pyright>`_ - used for type checking.
* `commitizen <https://github.com/commitizen-tools/commitizen>`_ - used to ensure proper `commit conventions <#committing>`_.

Building Documentation
----------------------
.. code::

    $ tox run -e docs

Builds and tests the documentation. You can view the newly built documentation under ``Moe/.tox/docs/tmp/html/``.

************************
Submitting Pull Requests
************************
Once your code changes are ready, or if you just want some early feedback, it's time to create a **Pull Request (PR)**.

Here's how the process works:

1.  **Open a Pull Request:** On GitHub, navigate to your forked repository and click the "New pull request" button. Select the branch where you made your changes and compare it to the ``main`` branch of the original ``MoeMusic/Moe`` repository.
2.  **Choose Draft or Ready:**

    * If your work is still in progress, you have questions, or you just want early feedback, open a **Draft Pull Request**. This clearly signals that it's not yet ready for a full review.
    * If you think your changes are complete and all tests are passing, you can open a regular Pull Request, indicating it's ready for review.
    * You can switch between Draft and Ready at any time. If you opened a ready PR but realize more work is needed or tests fail, just convert it back to a draft.
3.  **Review and Feedback:** Once your PR is open (and marked as ready), a project maintainer will review your changes.
4.  **Making Requested Changes:** If changes are requested, update your code locally and push the new commits to your branch using `fixup commits <https://git-scm.com/docs/git-commit#Documentation/git-commit.txt-code--fixupamendrewordltcommitgtcode>`_.
5.  **Request Another Review:** After pushing the changes addressing the feedback, request another review on the PR.
6.  **Merging:** Once the reviewers are happy with your contribution and all checks pass, your Pull Request will be approved and merged into the main Moe project!

Don't hesitate to ask questions in the PR comments if anything is unclear during the review process.
