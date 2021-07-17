############
Contributing
############

**************************
Creating a dev environment
**************************
#. `Install poetry <https://python-poetry.org/docs/#installation>`_
#. Clone the repository

   .. code:: bash

        $ git clone https://github.com/jtpavlock/moe.git

#. Install the project

   .. code:: bash

        $ cd Moe
        $ poetry install -E docs

#. Run Moe

   .. code:: bash

        $ poetry shell
        $ moe

   .. note::
        ``poetry shell`` will enter a virtual environment to interact with the project. To exit, just type ``exit`` in the shell. If you'd like to run ``moe`` or other commands without entering the virtual environment, prepend any commands with ``poetry run``.
