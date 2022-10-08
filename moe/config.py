"""User configuration of moe.

Each instance of Moe should only create a single `Config` object. This object will
contain all user settings and other related information and is set upon initializing
the configuration for the first time i.e. calling `Config()`. Once initialized, the
config can be accessed through import and should be treated as a constant::

    from moe import config
    print(config.CONFIG.settings.library_path)
"""

import importlib
import importlib.util
import logging
import os
import re
from pathlib import Path
from types import ModuleType
from typing import NamedTuple, Optional, Union, cast

import dynaconf
import pluggy
import sqlalchemy
import sqlalchemy.event
import sqlalchemy.orm

import alembic.command
import alembic.config
import moe

session_factory = sqlalchemy.orm.sessionmaker(autoflush=False)
MoeSession = sqlalchemy.orm.scoped_session(session_factory)

__all__ = ["CONFIG", "Config", "ConfigValidationError", "ExtraPlugin"]

log = logging.getLogger("moe.config")

DEFAULT_PLUGINS = {
    "add",
    "cli",
    "duplicate",
    "edit",
    "import",
    "info",
    "list",
    "move",
    "musicbrainz",
    "sync",
    "remove",
    "write",
}
CORE_PLUGINS = {
    "config": "moe.config",
    "album": "moe.library.album",
    "extra": "moe.library.extra",
    "track": "moe.library.track",
    "lib_item": "moe.library.lib_item",
}  # {name: module} of plugins that cannot be overwritten by the config

CONFIG = cast("Config", None)


class ConfigValidationError(Exception):
    """Error in the user's configuration."""


class Hooks:
    """Config hook specifications."""

    @staticmethod
    @moe.hookspec
    def add_config_validator(settings: dynaconf.base.LazySettings):
        """Add a settings validator for the configuration file.

        Args:
            settings: Moe's settings.

        Example:
            .. code:: python

                settings.validators.register(
                    dynaconf.Validator("MOVE.ASCIIFY_PATHS", must_exist=True)
                )

        See Also:
            https://www.dynaconf.com/validation/#validation for more info.
        """

    @staticmethod
    @moe.hookspec
    def add_hooks(pm: pluggy.manager.PluginManager):
        """Add hookspecs to be registered to Moe.

        Args:
            pm: PluginManager that registers the hookspec.

        Example:
            .. code:: python

                from moe.plugins.add import Hooks
                pm.add_hookspecs(Hooks)
        """

    @staticmethod
    @moe.hookspec
    def plugin_registration():
        """Allows actions after the initial plugin registration.

        In order for a module to implement and register plugin hooks, it must be
        registered as a separate plugin with the ``pm``. A plugin can be
        either just a module, or a full package.

        If a plugin is a package, only it's ``__init__.py`` will be initially
        registered, meaning only ``__init__.py`` will be able to run hook
        implementations at start-up. This hook is provided so each plugin can register
        it's individual sub-modules as appropriate.

        Important:
            Ensure any sub-modules you register as plugins are registered with the
            original plugin name as the prefix. This helps prevent naming conflicts.

        For example, see how the ``edit`` plugin conditionally enables its cli
        sub-module::

            @moe.hookimpl
            def plugin_registration():
                if config.CONFIG.pm.has_plugin("cli"):
                    config.CONFIG.pm.register(edit_cli, "edit_cli")

        This hook can also be used as a way of checking for plugin dependencies by
        inspecting the enabled plugins in the configuration.

        For example, because the ``list`` plugin only exists as a cli plugin, it will
        un-register itself and log a warning if the cli plugin is not enabled::

            @moe.hookimpl
            def plugin_registration():
                if not config.CONFIG.pm.has_plugin("cli"):
                    config.CONFIG.pm.set_blocked("list")
                    log.warning("You can't list stuff without a cli!")

        See Also:
            `pluggy.PluginManager documentation <https://pluggy.readthedocs.io/en/latest/api_reference.html>`_
        """  # noqa: E501

    @staticmethod
    @moe.hookspec
    def register_sa_event_listeners(session: sqlalchemy.orm.Session):
        """Registers new sqlalchemy event listeners.

        Args:
            session: Session to attach the listener to.

        Important:
            This hooks is for Moe internal use only and should not be used by plugins.

        Example:
            .. code:: python

                sqlalchemy.event.listen(
                    session,
                    "before_flush",
                    _my_func,
                )

            Then you can define ``_my_func`` as such::

                def _my_func(
                    session: sqlalchemy.orm.Session,
                    flush_context: sqlalchemy.orm.UOWTransaction,
                    instances: Optional[Any],
                ):
                    print("we made it")

        See Also:
            `SQLAlchemy ORM even documentation <https://docs.sqlalchemy.org/en/14/orm/events.html#orm-events>`_
        """  # noqa: E501


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    validators = [
        dynaconf.Validator("DEFAULT_PLUGINS", default=DEFAULT_PLUGINS),
        dynaconf.Validator("DISABLE_PLUGINS", default=set()),
        dynaconf.Validator("LIBRARY_PATH", default="~/Music"),
        dynaconf.Validator("ORIGINAL_DATE", default=False),
    ]
    settings.validators.register(*validators)


class ExtraPlugin(NamedTuple):
    """Used to specify extra plugins when initializing the config.

    Attributes:
        plugin: This is the class or module of the plugin to register.
        name: Name to register the plugin under.
    """

    plugin: Union[type, ModuleType]
    name: str


class Config:
    """Initializes moe configuration settings and database.

    Attributes:
        config_dir (Path): Filesystem path of the configuration directory.
        config_file (Path): Filesystem path of the configuration settings file.
        engine (sa.engine.base.Engine): Database engine in use.
        pm (pluggy.manager.PluginManager): Plugin manager that handles plugin logic.
        settings (dynaconf.base.LazySettings): User configuration settings.
    """

    def __init__(
        self,
        config_dir: Path = Path.home() / ".config" / "moe",  # noqa: B008
        settings_filename: str = "config.toml",
        extra_plugins: Optional[list[ExtraPlugin]] = None,
        engine: Optional[sqlalchemy.engine.base.Engine] = None,
        init_db=True,
    ):
        """Initializes the plugin manager and configuration directory.

        Args:
            config_dir: Filesystem path of the configuration directory where the
                settings and database files will reside. The environment variable
                ``MOE_CONFIG_DIR`` has precedence in setting this.
            extra_plugins: Any extra plugins that should be enabled in addition to those
                specified in the configuration.
            settings_filename: Name of the configuration settings file.
            engine: sqlalchemy database engine to use. Defaults to a sqlite db located
                in the ``config_dir``.
            init_db: Whether or not to initialize the database.
        """
        global CONFIG
        CONFIG = self

        try:
            self.config_dir = Path(os.environ["MOE_CONFIG_DIR"])
        except KeyError:
            self.config_dir = config_dir

        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = self.config_dir / settings_filename
        self._extra_plugins = extra_plugins or []
        self._read_config()

        self.engine = engine
        if init_db:
            self._init_db()

    def _init_db(self, create_tables: bool = True):
        """Initializes the database.

        Moe uses sqlite by default.

        Args:
            create_tables: Whether or not to create and update the db tables.
                If doing db migrations manually, e.g. in alembic, this should be False.
        """
        log.debug(f"Initializing database. [{create_tables=!r}]")

        db_path = self.config_dir / "library.db"

        if not self.engine:
            self.engine = sqlalchemy.create_engine("sqlite:///" + str(db_path))

        session_factory.configure(bind=self.engine)

        # create and update database tables
        if create_tables:
            config_path = Path(__file__)
            alembic_cfg = alembic.config.Config(
                str(config_path.parents[1] / "alembic" / "alembic.ini")
            )
            alembic_cfg.attributes["configure_logger"] = False
            with self.engine.begin() as connection:
                alembic_cfg.attributes["connection"] = connection
                alembic.command.upgrade(alembic_cfg, "head")

        self.pm.hook.register_sa_event_listeners(config=self, session=MoeSession())

        # create regular expression function for sqlite queries
        @sqlalchemy.event.listens_for(self.engine, "begin")
        def sqlite_engine_connect(conn):
            conn.connection.create_function("regexp", 2, _regexp, deterministic=True)

        def _regexp(pattern: str, col_value) -> bool:
            """Use the python re module for sqlite regular expression functionality.

            Args:
                pattern: Regular expression pattern.
                col_value: Column value to match against. The match will be against
                    the str of the value.

            Returns:
                Whether or not the match was successful.
            """
            return re.search(pattern, str(col_value), re.IGNORECASE) is not None

        log.debug(f"Initialized database. [engine={self.engine!r}]")

    def _read_config(self):
        """Reads the user configuration settings.

        Searches for a configuration file at `config_dir / "config.toml"`.

        Raises:
            ConfigValidationError: Unable to parse the configuration file.
        """
        from moe.library.lib_item import PathType

        log.debug(f"Reading configuration file. [config_file={self.config_file}]")

        self.config_file.touch(exist_ok=True)

        self.settings = dynaconf.Dynaconf(
            envvar_prefix="MOE",  # export envvars with `export MOE_FOO=bar`
            settings_file=str(self.config_file.resolve()),
        )

        self._setup_plugins()
        self.pm.hook.add_config_validator(settings=self.settings)
        self._validate_settings()

        PathType.library_path = Path(self.settings.library_path)

    def _validate_settings(self):
        """Validates the given user configuration.

        Raises:
            ConfigValidationError: Error validating the configuration.
        """
        log.debug("Validating configuration settings.")

        try:
            self.settings.validators.validate()
        except dynaconf.validator.ValidationError as err:
            raise ConfigValidationError(err) from err

    def _setup_plugins(self, core_plugins: dict[str, str] = CORE_PLUGINS):
        """Setup pm and hook logic.

        Args:
            core_plugins: Optional mapping of core plugin modules to names.
                These plugins cannot be overwritten by the user configuration.
        """
        log.debug("Setting up plugins.")

        self.pm = pluggy.PluginManager("moe")

        # register core modules that are not considered plugins
        for plugin_name, module in core_plugins.items():
            self.pm.register(importlib.import_module(module), plugin_name)

        # need to validate `config` specific settings separately so we have access to
        # the 'default_plugins' setting
        self.pm.add_hookspecs(Hooks)
        self.pm.hook.add_config_validator(settings=self.settings)
        self._validate_settings()

        config_plugins = set(self.settings.default_plugins) - set(
            self.settings.disable_plugins
        )

        # the 'import' plugin maps to the 'moe_import' package
        if "import" in config_plugins:
            config_plugins.remove("import")
            config_plugins.add("moe_import")

        if "cli" in config_plugins:
            self.pm.register(importlib.import_module("moe.cli"), name="cli")

        # register plugin hookimpls for all enabled plugins
        self._register_internal_plugins(config_plugins)

        # register plugin hookimpls for all extra plugins
        for extra_plugin in self._extra_plugins:
            self.pm.register(extra_plugin.plugin, extra_plugin.name)

        # register individual plugin sub-modules
        self.pm.hook.plugin_registration(pm=self.pm)

        # register plugin hookspecs for all enabled plugins
        self.pm.hook.add_hooks(pm=self.pm)

        log.debug(f"Registered plugins. [plugins={self.pm.list_name_plugin()}]")

    def _register_internal_plugins(self, enabled_plugins):
        """Registers all internal plugins in `enabled_plugins`."""
        plugin_dir = Path(__file__).resolve().parent / "plugins"

        for plugin_path in plugin_dir.iterdir():
            plugin_name = plugin_path.stem

            if plugin_path.stem in enabled_plugins:
                plugin = importlib.import_module("moe.plugins." + plugin_name)
                self.pm.register(plugin, plugin_name)
