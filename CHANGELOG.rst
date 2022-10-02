#########
Changelog
#########

This project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

v0.12.1 (2022-10-02)
====================

Bug Fixes
---------
* Moving items that point to the same path (`4d79cd9 <https://github.com/MoeMusic/Moe/commit/4d79cd946f100d280475976a19aa0b950b29642c>`_)
* Import debug statements (`a907dd4 <https://github.com/MoeMusic/Moe/commit/a907dd42ef01d8ab23b47ff0c5462973297c0d26>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.12.0...v0.12.1>`__

v0.12.0 (2022-10-02)
====================

New Features
------------
* New sync plugin to sync music metadata (`6ad78f2 <https://github.com/MoeMusic/Moe/commit/6ad78f2cd97bcd61647905bdd39d5eaf62b69ff6>`_)
* Duplicate prompt ui improvements (`fd24944 <https://github.com/MoeMusic/Moe/commit/fd24944ace7ea8cbf4d0bef3ced869634108ead1>`_)
* Import prompt ui improvements (`2bbff8c <https://github.com/MoeMusic/Moe/commit/2bbff8ca05856565bd231ca5a0976ed0ccd54f19>`_)
* New global config option to explicitly disable plugins (`88d6bab <https://github.com/MoeMusic/Moe/commit/88d6babe6c0d1a23c460723f412062b59e3fc6e2>`_)

Bug Fixes
---------
* Albums were not querying properly if they didn't contain tracks (`094257d <https://github.com/MoeMusic/Moe/commit/094257d35e1e6a938495e6288cb01e969ad7868b>`_)
* Duplicate genres now persist in the database (`6a655b0 <https://github.com/MoeMusic/Moe/commit/6a655b00f73bf392ef843ac0068fb77c013668ef>`_)
* Custom fields now populate when loaded from the database (`911d0f7 <https://github.com/MoeMusic/Moe/commit/911d0f726c355d6d7ddbfbd812db8dce5b931afd>`_)

Build Changes
-------------
* Add rich as a dependency (`626b20c <https://github.com/MoeMusic/Moe/commit/626b20cda8ae798329fcb083b634b952a903e479>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.11.0...v0.12.0>`__

v0.11.0 (2022-09-19)
====================

Some big changes here, notably requiring python3.9 to take get the json1 extension in sqlite. This is what allows us to now support custom fields in plugins. This version introduces an non-backwards-compatible database change, and thus will require a deletion of any current library.

New Features
------------
* Read and write musicbrainz ids (`ef82c67 <https://github.com/MoeMusic/Moe/commit/ef82c672d21d70c59f0454b0b4d6fa22ef4ad0a9>`_)
* New hook to allow plugins to write custom tags to a track (`8ee8fcb <https://github.com/MoeMusic/Moe/commit/8ee8fcbebcab76a2fbf0ee096a0d346e51fe2874>`_)
* New hook to allow plugins to read/set custom track tags (`b5069ba <https://github.com/MoeMusic/Moe/commit/b5069ba2fc2164775a07a8e8a6c562a338da2bc1>`_)
* Custom fields can be set by plugins for all library items (`9606c1d <https://github.com/MoeMusic/Moe/commit/9606c1db0c2ce56fb84491a4d1db8af3bb6f6e20>`_)
* MB: New api call to update an album from musicbrainz (`2a972de <https://github.com/MoeMusic/Moe/commit/2a972def93e20714dde54bcadd0f5addad3c0a1a>`_)
* MB: Added new api call to set a mb collection to a set of releases (`aad7959 <https://github.com/MoeMusic/Moe/commit/aad7959a9edbec4e2d83c4a88d2c5bb83706daaa>`_)
* MB: Ability to auto update a musicbrainz collection (`6e1cec1 <https://github.com/MoeMusic/Moe/commit/6e1cec166ae76def39bd0970200168f55d67cf3e>`_)

Build Changes
-------------
* Move mccabe to dev dependencies (`ef373bc <https://github.com/MoeMusic/Moe/commit/ef373bcadbb0b32bb38a2a27612964c821a3e30f>`_)
* Require python3.9 (`55a8651 <https://github.com/MoeMusic/Moe/commit/55a86519584be1f276a12a61cdfca589b3ea5041>`_)
* Require python3.8 (`68f0640 <https://github.com/MoeMusic/Moe/commit/68f064099097465320f85f8f4107f99542cf19c4>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.10.0...v0.11.0>`__

v0.10.0 (2022-09-05)
====================

New Features
------------
* Add: Guess a track's disc number if not given or presumed wrong (`d71afd9 <https://github.com/MoeMusic/Moe/commit/d71afd9efd5d7cd65efabd383c4fe2da1c54613e>`_)
* Fuzzy match title when matching tracks (`37b9f02 <https://github.com/MoeMusic/Moe/commit/37b9f02b0649e478e525868c064942057fb6f72b>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.9.0...v0.10.0>`_

v0.9.0 (2022-09-02)
===================

Feat
----
- Paths are now configurable.
- Better duplicate resolution.

v0.8.2 (2022-02-03)
===================

Refactor
--------

-  clean query_type code

v0.8.1 (2021-09-21)
===================

Fix
---

-  remove src directory

v0.8.0 (2021-08-28)
===================

Feat
----

-  **config**: extra plugins can be specified in config init
-  add ``plugin_registration`` hook to allow custom plugin registration

Refactor
--------

-  **cli**: move ``edit_new_items`` and ``process_new_items`` hooks
-  switch to using a thread-local session
-  remove core subpackage
-  change to src/moe layout
-  split cli and core files

v0.7.3 (2021-08-14)
===================

Fix
---

-  **add**: abort will now abort importing an item entirely

v0.7.2 (2021-08-14)
===================

Refactor
--------

-  **add**: take advantage of argparse pathlib type

v0.7.1 (2021-08-08)
===================

Refactor
--------

-  **api**: introduce core api
-  **library**: add ``fields`` attribute to library items
-  **query**: "*" query now searches by track ID
-  **library**: take advantage of is_unique in **eq**

v0.7.0 (2021-07-18)
===================

.. _feat-1:

Feat
----

-  **list**: add ability to list item paths

v0.6.1 (2021-07-18)
===================

Fix
---

-  **move**: remove ability to auto-move items on tag changes
-  **move**: remove leftover empty dirs after an album has been moved

v0.6.0 (2021-07-18)
===================

Feat
----

-  **move**: add the ``move`` command

v0.5.0 (2021-07-17)
===================

Feat
----

-  **add**: use ‘artist’ as a backup for ‘albumartist’ if missing

v0.4.2 (2021-07-17)
===================

Fix
---

-  **add**: invalid tracks aren’t added as extras and are logged
   properly

v0.4.1 (2021-07-17)
===================

Refactor
--------

-  more appropriate names for sub-command parsers
-  abstract sqlalchemy orm events into new hook specifications

v0.4.0 (2021-07-15)
===================

Feat
----

-  **move**: add ``asciify_paths`` configuration option

Refactor
--------

-  **move**: move/copying tracks & extras now requires a destination

v0.3.12 (2021-07-12)
====================

Refactor
--------

-  mrmoe -> moe

v0.3.11 (2021-07-11)
====================

Refactor
--------

-  **cli**: only print warnings or worse logs for external libraries

v0.3.10 (2021-07-11)
====================

Fix
---

-  **info**: error accessing empty fields

v0.3.9 (2021-07-11)
===================

Refactor
--------

-  **info**: album info now only prints album attributes

v0.3.8 (2021-07-11)
===================

Refactor
--------

-  **track**: remove ``file_ext`` field
-  **track**: genre is now a concatenated string and genres is a list
-  **track**: don’t expose ``album_path`` as a track field
-  **extra**: album -> album_obj

Fix
---

-  **track**: properly read musibrainz track id from file
-  **write**: write date, disc, and disc_total to track file

v0.3.7 (2021-07-11)
===================

Fix
---

-  **move**: album copies to proper directory on add

v0.3.6 (2021-07-10)
===================

Fix
---

-  **move**: don’t move items until they’ve been added to the dB

v0.3.5 (2021-07-08)
===================

Fix
---

-  write and move properly oeprate on all altered items

v0.3.4 (2021-07-08)
===================

Fix
---

-  **library**: error when adding duplicate genres

v0.3.3 (2021-07-08)
===================

Refactor
--------

-  **add**: abstract questionary dependency from API

v0.3.2 (2021-07-07)
===================

Refactor
--------

-  **api**: define the api

v0.3.1 (2021-07-06)
===================

Fix
---

-  **add**: track file types now transferred when adding a new album via
   prompt

v0.3.0 (2021-07-06)
===================

Feat
----

-  **add**: only print new track title on prompt if it changed

v0.2.1 - v0.2.3 (2021-07-02)
============================

Fix issues installing from PYPI. (Lesson learned to use
`test.pypi.org <https://test.pypi.org>`__ next time.)

v0.2.0 (2021-07-01)
===================

Initial Alpha Release!

Basic features include:

-  add/remove/edit/list music to your library
-  import metadata from Musicbrainz
