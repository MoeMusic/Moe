###############
Welcome to Moe!
###############
Moe is our resident Music-Organizer-Extraordinaire who's sole purpose is to give you full control over your music library. In other words, it's a commandline-interface for managing your music.

*******************
Development Warning
*******************
Moe is currently in early development, and is still training for his goal to become your all-powerful music library assistant. You are more than welcome to start using Moe, but don't be surprised if you find any bugs or a lack of features. If you do find any bugs, or would like to request a feature, please feel free to `open an issue <https://github.com/jtpavlock/Moe/issues/new/choose>`_.

So what can Moe do right now?
=============================
* Add music to your library, fixing tags with metadata from Musicbrainz.
* Organize, remove, list, and edit your music in the library.
* Supports including extra files with an album e.g. log or playlist files.
* Supports tags with multiple values.

If you want to learn more, check out the `Getting Started <https://mrmoe.readthedocs.io/en/latest/getting_started.html>`_ docs.

********
Why Moe?
********
Moe takes *a lot* of inspiration from `beets <https://github.com/beetbox/beets>`_. If you haven't checked it out, please do so. It's an extremely impressive piece of software and `Adrian <https://github.com/sampsyo>`_ has done a great job developing it over the years. If you're looking for a more mature and/or complete solution *right now* for managing your library, it doesn't get much better than that.

However, there are several shortcomings that spawned the creation of Moe.

* `No support for tags with multiple values <https://github.com/beetbox/beets/issues/505>`_.
* `No native attachment/artifact support <https://github.com/beetbox/beets/pull/591>`_ i.e. the ability to move or query log files, album art, etc. with an album.
* It's quite an intimidating codebase for new developers. Beets is a beast of a project, as when it was first conceived, Adrian didn't have access to all the fancy python libraries we have now. As a result, there is a *ton** of hand-written code and solutions that are arguably better dealt off to an external library e.g. database integration or cross-platform filesystem path handling. Because of it's immense size and complexity, it's fairly difficult for a developer to come in and try to understand everything that's going on. I think this is part of the reason beets has seen trouble gaining new maintainers or willing developers that want to help further it along its path. These days, Adrian has begun to focus on other projects, which means I don't believe we are likely to see any major changes to beets for the foreseeable future.
* Most importantly, this is an area I'm passionate in, and felt it would be a valuable and fun learning experience creating my own app. I'm not a software developer by trade, so I greatly appreciate any feedback or thoughts anyone has as I go along.
