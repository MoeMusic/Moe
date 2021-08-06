####
Move
####
Alters the location of files in your library.

The ``move`` plugin provides the following features:

* Any items added to your library will be copied to the location set by ``library_path`` in your configuration file.
* Any items moved or copied will have their paths set to a default format. This default format cannot currently be configured, and is as follows:

  * Albums: ``{library_path}/{albumartist} ({album_year})/``
  * Tracks: ``{album_path}/{track_number} - {track_title}.{file_ext}``

    If the album contains more than one disc, tracks will be formatted as:

    ``{album_path}/Disc {disc#}/{track_number} - {track_title}.{file_ext}``
  * Extras: ``{album_path}/{original_file_name}``

*************
Configuration
*************
The ``move`` plugin is enabled by default and provides the following configuration options:

``asciify_paths = false``
    Whether or not to convert all filesystem paths to ascii.

    If ``true``, non-ascii characters will be converted to their ascii equivalents, e.g. ``café.mp3`` will become ``cafe.mp3``.

``library_path = "~/Music"``
    Tells Moe where to copy your added music to.

    For Windows users, the default path is ``%USERPROFILE%\Music``. Also, you need to set your path by enclosing it in triple-single quotes, e.g. ``'''~\Music'''``.

***********
Commandline
***********
The ``move`` command will move all items in the library according to your configuration file. This is useful if you make changes to the configuration file, and you'd like to move the items in your library to reflect the new changes.

.. code-block:: bash

    moe move [-h] [-n]

Options
-------
``-h, --help``
    Display the help message.

``-n, --dry-run``
    Show what will be moved without actually moving any files.
