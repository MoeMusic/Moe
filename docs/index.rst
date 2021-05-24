.. moe documentation master file, created by
   sphinx-quickstart on Sun May 23 14:55:57 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Moe!
===============================

Moe is our resident Music-Organizer-Extraordinaire who's sole purpose is to give you full control over your music library. In other words, it's a commandline-interface for managing your music akin to `beets <https://beets.readthedocs.io/en/stable/index.html>`_

Development Warning
-------------------
Moe is in *very* early stage development, and is still training for his goal to become your all-powerful music library assistant. You are more than welcome to poke around the codebase or `strike up a conversation <https://github.com/jtpavlock/moe/discussions>`_ about design ideas, or anything else really. If you do find any bugs though, I'd definitely appreciate you opening up a `ticket <https://github.com/jtpavlock/moe/issues/new?assignees=&labels=&template=bug-report.md>`_.

Why Moe?
--------
Moe's direct superior is clearly beets. If you haven't checked it out, please do so. It's an extremely impressive piece of software and `Adrian <https://github.com/sampsyo>`_ has done a great job developing it over the years. If you're looking for a complete solution *right now* for managing your library, it doesn't get much better than that.

However, there are several shortcomings that spawned the creation of Moe.

* `No support for tags with multiple values <https://github.com/beetbox/beets/issues/505>`_.
* `No native attachment/artifact support <https://github.com/beetbox/beets/pull/591>`_ i.e. the ability to move or query log files, album art, etc. with an album.
* It's quite an intimidating codebase for new developers. Beets is a beast of a project, as when it was first conceived, Adrian didn't have access to all the fancy python libraries we have now. As a result, there is a *ton* of hand-written code and solutions that are arguably better dealt off to an external library e.g. database integration or cross-platform filesystem path handling. Because of it's immense size and complexity, it's fairly difficult for a developer to come in and try to understand everything that's going on. I think this is part of the reason beets has seen trouble gaining new maintainers or willing developers that want to help further it along its path. These days, Adrian has begun to focus on other projects, which means I don't believe we are likely to see any major changes to beets for the foreseeable future.
* And most importantly, this is an area I'm passionate in, and felt it would be a valuable and fun learning experience creating my own app. I'm not a software developer by trade, so I greatly appreciate any feedback or thoughts anyone has as I go along.

I realize Moe probably won't match the feature-set of beets for a very long time, but every project has to start somewhere.

So what can Moe do right now?
-----------------------------
* Add music to your library.

  * Also copies the music to a set library path and organizes it by artist/album.
* Remove music from your library.
* List any music in your library.
* Print out tags of your music.

Like I said, *very* early in development. If you're still here and want to test out Moe in his current state, check out the :doc:`Getting Started <getting_started>` page.


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   getting_started
   plugins/index
   query
   developers



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
