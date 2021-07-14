####
Move
####
Alters the location of files in your library.

Files will be automatically copied to the location set under ``library_path`` in your :ref:`configuration file <General Configuration>` anytime items in the library are added or edited.

*************
Configuration
*************
This plugin is enabled by default, and provides the following configuration options:

``asciify_paths = false``
    Whether or not to convert all filesystem paths to ascii.

    If ``true`` non-ascii characters will be converted to their ascii equivalents, e.g. ``café.mp3`` will become ``cafe.mp3``.

``library_path = "~/Music"``
    Tells Moe where to copy your added music to.

    For Windows users, the default path is ``%USERPROFILE%\Music``. Also, you need to set your path by enclosing it in triple-single quotes, e.g. ``'''~\Music'''``.
