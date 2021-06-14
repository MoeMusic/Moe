####
Move
####
Alters the location of files in your library.

Files will be automatically copied to the location set under ``library_path`` in your :ref:`configuration file <General Configuration>` anytime items in the library are added or edited.

*************
Configuration
*************
``library_path = "~/Music"``
    Tells Moe where to copy your added music to.

    For Windows users, the default path is ``%USERPROFILE%\Music``. Also, you need to set your path by enclosing it in triple-single quotes.

    .. code-block:: toml

       library_path = '''~\Music'''
