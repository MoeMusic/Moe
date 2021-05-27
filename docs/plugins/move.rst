Move
====
Alters the location of files in the library.

Files will be automatically copied to the location set under ``library_path`` in your :ref:`configuration file <General Configuration>` after they are added to the library.

Configuration
-------------
* ``library_path``: Tells Moe where to copy your added music to.

  * Default: ``"~/Music"`` (``%USERPROFILE%\Music`` on Windows)

    If you're on Windows, you need to set your path by enclosing it in triple-single quotes.

    .. code-block:: toml

       library_path = '''~\Music'''
