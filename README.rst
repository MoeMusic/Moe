###############
Welcome to Moe!
###############
Moe is our resident Music-Organizer-Extraordinaire who's sole purpose is to give you full control over your music library by streamlining the process between downloading/ripping music to your filesystem and listening to it with your favorite music player.

In short, Moe maintains a database of your music library that can be updated with various metadata sources, queried, edited, etc. through either an API or command-line interface. All of these features, and more, are made available by a highly extensible plugin ecosystem.

Usage
=====
Moe comes with a command-line interface which is how most users will take advantage of the library management features. Below is a screenshot of Moe importing an album from the filesystem and adding it to the underlying database all while fixing tags, relocating the files, and anything else you can imagine.

.. image:: _static/import_example.png

Alternatively, because all the core functionality is available via an API, the underlying music management system can be incorporated into any existing program or other user interface.

Finally, although a lot of Moe's functionality exists around the idea of operating on a library database of your music, the database is entirely optional. In this case, Moe provides a convenient set of tools and functionality for handling music in a general sense. For example, below is a standalone python script that takes an album directory and Musicbrainz release ID from the command-line, and then updates the underlying files' tags with any changes from Musicbrainz (utilizing the ``musicbrainz`` plugin).

.. code:: python

    #!/usr/bin/env python3

    import argparse
    import pathlib

    from moe.config import Config, ConfigValidationError
    from moe.library import Album
    from moe.write import write_tags
    import moe_musicbrainz

    def main():
        try:
            config.Config(config_dir=Path.home() / ".config" / "my_script", init_db=False)
        except config.ConfigValidationError as err:
            raise SystemExit(1) from err

        parser = argparse.ArgumentParser(
            description="Update an album with musicbrainz tags."
        )
        parser.add_argument("path", help="dir of the album to update")
        parser.add_argument("mb_id", help="musicbrainz id of the album to fetch")
        args = parser.parse_args()

        album = Album.from_dir(pathlib.Path(args.path))

        album.merge(moe_musicbrainz.get_album_by_id(args.mb_id), overwrite=True)

        for track in album.tracks:
            write_tags(track)


    if __name__ == "__main__":
        main()

This is just a small taste of what Moe is capable of and how it can make your life easier when dealing with music in Python.

If you want to learn more, check out the `Getting Started <https://mrmoe.readthedocs.io/en/latest/getting_started.html>`_ docs.
