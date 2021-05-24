## v0.2.0 (2021-05-24)

### Feat

- **track**: add file extension field to Track
- **move**: add move plugin
- **config**: use dynaconf to manage configuration
- **query**: add wildcard '*' query
- **add**: add ability to add albums to the library
- **add**: adding multiple tracks no longer exits on first failure
- **add**: add now accepts multiple path arguments
- **add**: add ability to add directories (albums)
- **track**: support reading genre from tags
- **track**: add genre support to Track
- **library**: unique definitions for tracks and albums
- **config**: basic yaml config file loading
- **rm**: rm now removes both albums and tracks
- **info**: info plugin now handles albums and tracks
- **ls**: handle listing of albums
- **query**: add ability to query match albums instead of tracks
- **query**: add ability to query tracks matching album-specific fields
- **track**: read basic attributes from tracks
- *****: exit with non-zero code if sub-command failed
- **info**: add info command
- **rm**: add rm command
- **alembic**: use alembic for database migrations
- **track**: add title to track
- **ls**: add ls and basic querying
- **list**: Add list command
- **add**: add logging to add plugin
- **cli**: add root logger and cli logging args
- **add**: basic functionality to add a track's path to the database
- **add**: add command skeleton
- **plugin**: add super basic plugin structure with pluggy
- **cli**: initial cli commit

### Refactor

- **move**: add basic logging to move plugin
- **move**: remove unused custom exception
- **library**: remove add_to_db
- **add**: simplify parse_args
- **add**: add add_to_db to Album
- **config**: refactory config
- hookspecs are now loaded via a hook
- **add**: remove unnecessary exception
- various refactoring
- **add**: add post-add hook
- **config**: pluginmanager now resides in config
- **add**: refactor adding an album
- **library**: refactor track and album to use natural primary keys
- **add**: remove ability to add multiple tracks and fix logging
- **add**: better logging for adding directories
- **track**: better error handling for missing required track tags
- **track**: rename genre title to name
- **track**: albums now added to db if not existing on track creation
- **query**: refactor query parsing. multiple word queries now require quotes
- **library**: Refactor library and add abiltiy to handle db duplicates
- **query**: implement case insensitive regex queries a the regexp fun level
- **track**: change how path checking works to always check
- **config**: refactor config to separate logic
- **config**: simplify config
- *****: refactor core for associtaion proxy attrs and repr track and albums as dicts
- **library**: album-related fields are now exposed via associationproxies
- **item**: rename item to musicitem
- **album**: add an album object to tracks
- **query**: change warnings to errors when unable to complete a query
- **alembic**: clarify config in env
- **config**: remove sqlite try except regexp
- **library**: remove unused pathtype comparison code
- **query**: ValueError if invalid query value given
- **query**: separate query logic
- **info**: refactor info for easier testing
- **add**: better error handling if added file doesn't exist
- **track**: track now requires the given path to exist
- **config**: expose engine in config instead of db_path
- **migration**: first migration script - add title to tracks
- **config**: change lib to core and move config inside
- **add**: Add type annotations to add plugin
- **config**: Refactor config for better dependency injection
- **config**: adds config module
- **cli**: generalize plugin loading
- **cli**: refactor cli hook into cli module
- **project**: rename project fili -> moe
- **cli**: separate arg parsing into own function

### Fix

- **info**: remove registry attribute
- **add**: ignore non-media files when adding albums
- **track**: check for None arguments when creating a Track
- **album**: Fix to_dict() various bug
- **query**: association proxy queries now work for case-insensitive matches
- **cli**: main was not passing in args correctly
- **add**: store paths as absolute instead of relative
