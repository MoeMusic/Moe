#########
Changelog
#########

This project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

v1.5.1 (2022-11-06)
===================

Bug Fixes
---------
* Ensure tracks created from files contain required tags (`bf215ed <https://github.com/MoeMusic/Moe/commit/bf215ed674bff2d1c7d1024d391dc57995f39055>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v1.5.0...v1.5.1>`__

v1.5.0 (2022-11-05)
===================

New Features
------------
* Add new `lib_path` argument to `fmt_item_path` (`5ed5dc4 <https://github.com/MoeMusic/Moe/commit/5ed5dc458860d24a7e8a13d9876b02515394aecf>`_)
* Add sample rate and bit depth as track properties (`f9c3384 <https://github.com/MoeMusic/Moe/commit/f9c3384fb7cf20f0dad221ae1f5a38210660d547>`_)

Bug Fixes
---------
* [none] catalog number from musicbrainz now properly set (`25d73e1 <https://github.com/MoeMusic/Moe/commit/25d73e1cf5a6d8ce38e8769631ed4b2089f83182>`_)
* Albumartist overwriting track artist (`6bbf445 <https://github.com/MoeMusic/Moe/commit/6bbf4454b1df1f2d40279980a7dcc348c767684c>`_)

Build Changes
-------------
* Support python 3.11 (`de6ebd2 <https://github.com/MoeMusic/Moe/commit/de6ebd27f8211ec90d16940609776698ae66ea85>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v1.4.0...v1.5.0>`__

v1.4.0 (2022-11-03)
===================

New Features
------------
* Show catalog number after label during import (`84f8067 <https://github.com/MoeMusic/Moe/commit/84f8067bfde837657a1d120853841e77b6cd5845>`_)

Bug Fixes
---------
* Musicbrainz error if release does not have a date or format (`d0fe109 <https://github.com/MoeMusic/Moe/commit/d0fe1096c6a5d522b44e19821defa33302baab01>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v1.3.2...v1.4.0>`__

v1.3.2 (2022-11-01)
===================

Bug Fixes
---------
* Track `audio_format` is now a property and not a field (`c2aeda7 <https://github.com/MoeMusic/Moe/commit/c2aeda7fee2639576b79a83614e062dae018fc2a>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v1.3.1...v1.3.2>`__

v1.3.1 (2022-11-01)
===================

Bug Fixes
---------
* Use fork of mediafile (`53d8333 <https://github.com/MoeMusic/Moe/commit/53d8333907a2095957202d456df6ccf8cf342b76>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v1.3.0...v1.3.1>`__

v1.3.0 (2022-11-01)
===================

New Features
------------
* New MetaAlbum and MetaTrack classes (`e496e7c <https://github.com/MoeMusic/Moe/commit/e496e7c779bf8fe32711cd3f58b84efda61e4784>`_)
* New track field - audio_format (`07fce9f <https://github.com/MoeMusic/Moe/commit/07fce9f7dd28a2b6674f63fe2180490ffa83d236>`_)
* New album field - catalog_nums (`01c7170 <https://github.com/MoeMusic/Moe/commit/01c71707eb80f249c9709b820b40b2f6938b8c34>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v1.2.0...v1.3.0>`__

v1.2.0 (2022-10-12)
===================

New Features
------------
* CLI prompts now allow arrow keys to navigate choices (`78344f9 <https://github.com/MoeMusic/Moe/commit/78344f900a68926e91fc676aa18b034cbd1b5b51>`_)
* New album field - track_total (`eb947b9 <https://github.com/MoeMusic/Moe/commit/eb947b9fb94d26c12e579deb8e802f41233a9474>`_)
* Improve musicbrainz search accuracy (`891b995 <https://github.com/MoeMusic/Moe/commit/891b995e78f6701db411f28d32dd023002b31e49>`_)

Bug Fixes
---------
* Tags now written to tracks if album fields changed (`48f7076 <https://github.com/MoeMusic/Moe/commit/48f707608e5320e6d860641bf3553134d7380bde>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v1.1.0...v1.2.0>`__

v1.1.0 (2022-10-12)
===================

New Features
------------
* New read plugin for updating items in moe with any file changes (`adbbdd4 <https://github.com/MoeMusic/Moe/commit/adbbdd49c015953edee7d8225bf3de852748cef8>`_)
* New album field - barcode (`72d07d3 <https://github.com/MoeMusic/Moe/commit/72d07d354cc636d215ae970f9d708d2e3617cdfc>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v1.0.0...v1.1.0>`__

v1.0.0 (2022-10-09)
===================
First stable release! From this point on, the API is considered stable and breaking changes will result in a new major version per semantic versioning.

Breaking Changes
----------------
* Update docs for stable release (`07fec3e <https://github.com/MoeMusic/Moe/commit/07fec3e215490d1c4fbc83430404b1b0a5d5cdf7>`_)

Bug Fixes
---------
* Import wrong dataclass (`ee6959a <https://github.com/MoeMusic/Moe/commit/ee6959a905496a15b70561ddcebbf413a53257e1>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.16.0...v1.0.0>`__

v0.16.0 (2022-10-09)
====================

New Features
------------
* Support for external third-party plugins (`b0c736c <https://github.com/MoeMusic/Moe/commit/b0c736cb93077848a9208e70d869e10e1775d0d3>`_)
* Users can now create custom plugins in their configuration dir (`84347f6 <https://github.com/MoeMusic/Moe/commit/84347f61bb6ac95bd8671ec94c0b4e27550cfb5d>`_)
* Add command can now handle adding extras (`ab83e63 <https://github.com/MoeMusic/Moe/commit/ab83e633ef439bb8d5ea316f4bb18ed5e31426b8>`_)
* Candidate prompt to select an album to import (`c5ff9a5 <https://github.com/MoeMusic/Moe/commit/c5ff9a5d330adef1ae0450d8b2a6f7e22a5b65d5>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.15.3...v0.16.0>`__

v0.15.3 (2022-10-08)
====================

Bug Fixes
---------
* Musicbrainz error if a release has no label (`6991a41 <https://github.com/MoeMusic/Moe/commit/6991a41b6f0e6192be4c4a042613d0f4eaf8c3f3>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.15.2...v0.15.3>`__

v0.15.2 (2022-10-08)
====================

Bug Fixes
---------
* Musicbrainz error if release does not have a country specified (`1c0f844 <https://github.com/MoeMusic/Moe/commit/1c0f844ddb595ba04ac0a947a7e02d33d48f1121>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.15.1...v0.15.2>`__

v0.15.1 (2022-10-08)
====================

Bug Fixes
---------
* Sync_item not called with keyword arguments (`7c4b65a <https://github.com/MoeMusic/Moe/commit/7c4b65a854abe62aab3f1c13f0829dd6d01f9f95>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.15.0...v0.15.1>`__

v0.15.0 (2022-10-08)
====================

New Features
------------
* New config option ``original_date`` (`3894fa7 <https://github.com/MoeMusic/Moe/commit/3894fa716e45150531c4dfe7473aa7f701ec542c>`_)
* New field - original_date (`416d202 <https://github.com/MoeMusic/Moe/commit/416d20282debdfd2cc1bc2f2fb97246522724b41>`_)
* Add media, label, country, and year to import header (`ce9cc9a <https://github.com/MoeMusic/Moe/commit/ce9cc9a42efdbae7b55bcb12c5328c7b373f68cb>`_)
* New album field - label (`80e8348 <https://github.com/MoeMusic/Moe/commit/80e8348972591b337d9c67cb1fc0d432a44eb949>`_)
* New album field - country (`5a51d71 <https://github.com/MoeMusic/Moe/commit/5a51d716ba731f03a4d07d8f70707bebd8cd3ea9>`_)
* New album field - media (`256a3a6 <https://github.com/MoeMusic/Moe/commit/256a3a673182b917c3a2c09773b205ee6204c42a>`_)
* New track field - artists (`7701d9e <https://github.com/MoeMusic/Moe/commit/7701d9e8ec18e9dd26c788ce5570b5a8d62d4218>`_)
* New path template function to get a unique extra filename (`8a0c3a3 <https://github.com/MoeMusic/Moe/commit/8a0c3a3fd615b5defde64ecb348e914ff2c29306>`_)
* Allow plugins to create custom path template functions (`195ea9c <https://github.com/MoeMusic/Moe/commit/195ea9c4f32950dd81ce8ec2704421e3bb03a949>`_)
* Add `mbcol` cli argument to sync music to a musicbrainz collection (`4f00136 <https://github.com/MoeMusic/Moe/commit/4f001362487795ed76efaf5e27065ec16a9f918f>`_)
* List cli output is now sorted (`fbb11d0 <https://github.com/MoeMusic/Moe/commit/fbb11d0826b265e871f6676690ddf053760fba76>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.14.0...v0.15.0>`__

v0.14.0 (2022-10-02)
====================

New Features
------------
* Add: New import option to skip a single item (`3d3027c <https://github.com/MoeMusic/Moe/commit/3d3027c5ab37d78a24bffbf014cce4dc19d4c435>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.13.0...v0.14.0>`__

v0.13.0 (2022-10-02)
====================

New Features
------------
* Adjusted track match values to be more lenient (`9b90803 <https://github.com/MoeMusic/Moe/commit/9b90803b50acd09ede30d3318967bc686bffed4b>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.12.2...v0.13.0>`__

v0.12.2 (2022-10-02)
====================

Bug Fixes
---------
* Relative path error if album and file use non-relative hardlinks (`8574e38 <https://github.com/MoeMusic/Moe/commit/8574e382a54e77b3c221f851c3fa910b3a45afbf>`_)

`Full diff <https://github.com/MoeMusic/Moe/compare/v0.12.1...v0.12.2>`__

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
