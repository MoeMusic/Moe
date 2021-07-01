"""This is a Python script that is run whenever the alembic migration tool is invoked.

At the very least, it contains instructions to configure and generate a SQLAlchemy
engine, procure a connection from that engine along with a transaction, and then
invoke the migration engine, using the connection as a source of database connectivity.

The env.py script is part of the generated environment so that the way migrations run
is entirely customizable. The exact specifics of how to connect are here, as well as
the specifics of how the migration environment are invoked. The script can be modified
so that multiple engines can be operated upon, custom arguments can be passed into the
migration environment, application-specific libraries and models can be loaded in
and made available.

Alembic includes a set of initialization templates which feature different varieties
of env.py for different use cases.
"""

from logging.config import fileConfig

from alembic import context
from moe.core.config import Config
from moe.core.library.session import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# don't configure logger if Moe is running
if config.attributes.get("configure_logger", True):
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection
    with the context.
    """
    connectable = config.attributes.get("connection", None)
    if not connectable:
        # only create Engine if we don't have a Connection from the outside
        moe_config = Config()
        moe_config.init_db(create_tables=False)
        connectable = moe_config.engine

    # When connectable is already a Connection object, calling
    # connect() gives us a *branched connection*.
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
