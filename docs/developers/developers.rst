##########
Developers
##########

**************************
Creating a dev environment
**************************
#. `Install poetry <https://python-poetry.org/docs/#installation>`_.
#. Clone the repository

    .. code-block:: bash

        $ git clone https://github.com/jtpavlock/moe.git
#. Install the project

    .. code-block:: bash

       $ cd Moe
       $ poetry install
#. Run Moe

    .. code-block:: bash

       $ poetry shell
       $ moe

.. note::
    ``poetry shell`` will enter a virtual environment to interact with the project. To exit, just type ``exit`` in the shell. If you'd like to run ``moe`` or other commands without entering the virtual environment, prepend any commands with ``poetry run``.

    .. code-block:: bash

       $ poetry run moe


***
API
***

.. warning::
    While Moe is in version ``0.X.Y``, the api should be considered unstable.

.. toctree::
    :maxdepth: 4
    :caption: Contents:

    api/moe.rst
