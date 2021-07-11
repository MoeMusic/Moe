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
