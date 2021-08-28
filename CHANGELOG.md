## v0.8.0 (2021-08-28)

### Feat

- **config**: extra plugins can be specified in config init
- add `plugin_registration` hook to allow custom plugin registration

### Refactor

- **cli**: move `edit_new_items` and `process_new_items` hooks
- switch to using a thread-local session
- remove core subpackage
- change to src/moe layout
- split cli and core files

## v0.7.3 (2021-08-14)

### Fix

- **add**: abort will now abort importing an item entirely

## v0.7.2 (2021-08-14)

### Refactor

- **add**: take advantage of argparse pathlib type

## v0.7.1 (2021-08-08)

### Refactor

- **api**: introduce core api
- **library**: add `fields` attribute to library items
- **query**: "*" query now searches by track ID
- **library**: take advantage of is_unique in __eq__

## v0.7.0 (2021-07-18)

### Feat

- **list**: add ability to list item paths

## v0.6.1 (2021-07-18)

### Fix

- **move**: remove ability to auto-move items on tag changes
- **move**: remove leftover empty dirs after an album has been moved

## v0.6.0 (2021-07-18)

### Feat

- **move**: add the `move` command

## v0.5.0 (2021-07-17)

### Feat

- **add**: use 'artist' as a backup for 'albumartist' if missing

## v0.4.2 (2021-07-17)

### Fix

- **add**: invalid tracks aren't added as extras and are logged properly

## v0.4.1 (2021-07-17)

### Refactor

- more appropriate names for sub-command parsers
- abstract sqlalchemy orm events into new hook specifications

## v0.4.0 (2021-07-15)

### Feat

- **move**: add `asciify_paths` configuration option

### Refactor

- **move**: move/copying tracks & extras now requires a destination

## v0.3.12 (2021-07-12)

### Refactor

- mrmoe -> moe

## v0.3.11 (2021-07-11)

### Refactor

- **cli**: only print warnings or worse logs for external libraries

## v0.3.10 (2021-07-11)

### Fix

- **info**: error accessing empty fields

## v0.3.9 (2021-07-11)

### Refactor

- **info**: album info now only prints album attributes

## v0.3.8 (2021-07-11)

### Refactor

- **track**: remove `file_ext` field
- **track**: genre is now a concatenated string and genres is a list
- **track**: don't expose `album_path` as a track field
- **extra**: album -> album_obj

### Fix

- **track**: properly read musibrainz track id from file
- **write**: write date, disc, and disc_total to track file

## v0.3.7 (2021-07-11)

### Fix

- **move**: album copies to proper directory on add

## v0.3.6 (2021-07-10)

### Fix

- **move**: don't move items until they've been added to the dB

## v0.3.5 (2021-07-08)

### Fix

- write and move properly oeprate on all altered items

## v0.3.4 (2021-07-08)

### Fix

- **library**: error when adding duplicate genres

## v0.3.3 (2021-07-08)

### Refactor

- **add**: abstract questionary dependency from API

## v0.3.2 (2021-07-07)

### Refactor

- **api**: define the api

## v0.3.1 (2021-07-06)

### Fix

- **add**: track file types now transferred when adding a new album via prompt

## v0.3.0 (2021-07-06)

### Feat

- **add**: only print new track title on prompt if it changed

## v0.2.1 - v0.2.3 (2021-07-02)

Fix issues installing from PYPI. (Lesson learned to use [test.pypi.org](https://test.pypi.org) next time.)

## v0.2.0 (2021-07-01)

Initial Alpha Release!

Basic features include:

- add/remove/edit/list music to your library
- import metadata from Musicbrainz
