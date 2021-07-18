####
Move
####
Alters the location of files in your library.

The `move` plugin provides the following features:
 * ``move`` command to "consolidate" or move items in the library to reflect changes in your configuration or tags.
 * Any items added to the library will be copied to the location set by ``library_path`` in your configuration file.

This plugin is enabled by default.

*************
Configuration
*************
This plugin provides the following configuration options:

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
