"""User configuration of moe.

To avoid namespace confusion when using a variable named config, typical usage of this
module should just import the Config class directly::

    from moe.config import Config
    config = Config()

A configuration shuold only be instantiated once per instance of Moe. Plugins should
pass along that instance through their hooks.
"""

import importlib
import importlib.util
import logging
import os
import re
from contextlib import suppress
from pathlib import Path
from types import ModuleType
from typing import NamedTuple, Optional, Union

import dynaconf
import pluggy
import sqlalchemy
import sqlalchemy.event
import sqlalchemy.orm

import alembic.command
import alembic.config
import moe

session_factory = sqlalchemy.orm.sessionmaker()
MoeSession = sqlalchemy.orm.scoped_session(session_factory)

__all__ = ["Config", "ConfigValidationError", "ExtraPlugin"]

log = logging.getLogger("moe.config")

DEFAULT_PLUGINS = (
    "add",
    "cli",
    "edit",
    "import",
    "info",
    "list",
    "move",
    "musicbrainz",
    "remove",
    "write",
)
CORE_PLUGINS = {
    "config": "moe.config",
    "album": "moe.library.album",
    "extra": "moe.library.extra",
    "track": "moe.library.track",
    "lib_item": "moe.library.lib_item",
}  # {name: module} of plugins that cannot be overwritten by the config


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
            Inside your hook implementation::

                settings.validators.register(
                    dynaconf.Validator("MOVE.ASCIIFY_PATHS", must_exist=True)
                )

        See Also:
            https://www.dynaconf.com/validation/#validation for more info.
        """

    @staticmethod
    @moe.hookspec
    def add_hooks(plugin_manager: pluggy.manager.PluginManager):
        """Add hookspecs to be registered to Moe.

        Args:
            plugin_manager: PluginManager that registers the hookspec.

        Example:
            Inside your hook implementation::

                from moe.plugins.add import Hooks
                plugin_manager.add_hookspecs(Hooks)
        """

    @staticmethod
    @moe.hookspec
    def plugin_registration(config: "Config"):
        """Allows actions after the initial plugin registration.

        In order for a module to implement and register plugin hooks, it must be
        registered as a separate plugin with the ``plugin_manager``. A plugin can be
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
            def plugin_registration(config):
                if config.plugin_manager.has_plugin("cli"):
                    config.plugin_manager.register(edit_cli, "edit_cli")

        This hook can also be used as a way of checking for plugin dependencies by
        inspecting the enabled plugins in the configuration.

        For example, because the ``list`` plugin only exists as a cli plugin, it will
        un-register itself and log a warning if the cli plugin is not enabled::

            @moe.hookimpl
            def plugin_registration(config):
                if not config.plugin_manager.has_plugin("cli"):
                    config.plugin_manager.set_blocked("list")
                    log.warning("You can't list stuff without a cli!")

        See Also:
            `pluggy.PluginManager documentation <https://pluggy.readthedocs.io/en/latest/api_reference.html>`_

        Args:
            config: Moe config.
        """  # noqa: E501

    @staticmethod
    @moe.hookspec
    def register_sa_event_listeners(config: "Config", session: sqlalchemy.orm.Session):
        """Registers new sqlalchemy event listeners.

        Args:
            config: Moe config.
            session: Session to attach the listener to.

        Important:
            This hooks is for Moe internal use only and should not be used by plugins.

        Example:
            In your hook implementation::

                sqlalchemy.event.listen(
                    session,
                    "before_flush",
                    functools.partial(_my_func, config=config),
                )

            Then you can define ``_my_func`` as such::

                def _my_func(
                    session: sqlalchemy.orm.Session,
                    flush_context: sqlalchemy.orm.UOWTransaction,
                    instances: Optional[Any],
                    config: Config,
                ):
                    print("we made it")

        See Also:
            `SQLAlchemy ORM even documentation <https://docs.sqlalchemy.org/en/14/orm/events.html#orm-events>`_
        """  # noqa: E501


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    validators = [
        dynaconf.Validator("DEFAULT_PLUGINS", default=list(DEFAULT_PLUGINS)),
        dynaconf.Validator("LIBRARY_PATH", default="~/Music"),
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
        plugin_manager (pluggy.manager.PluginManager): Manages plugin logic.
        settings (dynaconf.base.LazySettings): User configuration settings.

    Example:
        In your plugin, to access the library_path setting (assuming a Config object
        named config)::

            config.settings.library_path

        See the dynaconf documentation for more info on reading settings variables.
        https://www.dynaconf.com/#reading-settings-variables
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

        self.plugin_manager.hook.register_sa_event_listeners(
            config=self, session=MoeSession()
        )

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
        self.plugin_manager.hook.add_config_validator(settings=self.settings)
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
        """Setup plugin_manager and hook logic.

        Args:
            core_plugins: Optional mapping of core plugin modules to names.
                These plugins cannot be overwritten by the user configuration.
        """
        log.debug("Setting up plugins.")

        self.plugin_manager = pluggy.PluginManager("moe")

        # register core modules that are not considered plugins
        for plugin_name, module in core_plugins.items():
            self.plugin_manager.register(importlib.import_module(module), plugin_name)

        # need to validate `config` specific settings separately so we have access to
        # the 'default_plugins' setting
        self.plugin_manager.add_hookspecs(Hooks)
        self.plugin_manager.hook.add_config_validator(settings=self.settings)
        self._validate_settings()

        config_plugins = self.settings.default_plugins

        # the 'import' plugin maps to the 'moe_import' package
        with suppress(ValueError):
            import_index = config_plugins.index("import")
            config_plugins[import_index] = "moe_import"

        if "cli" in config_plugins:
            self.plugin_manager.register(importlib.import_module("moe.cli"), name="cli")

        # register plugin hookimpls for all enabled plugins
        self._register_internal_plugins(config_plugins)

        # register plugin hookimpls for all extra plugins
        for extra_plugin in self._extra_plugins:
            self.plugin_manager.register(extra_plugin.plugin, extra_plugin.name)

        # register individual plugin sub-modules
        self.plugin_manager.hook.plugin_registration(
            config=self, plugin_manager=self.plugin_manager
        )

        # register plugin hookspecs for all enabled plugins
        self.plugin_manager.hook.add_hooks(plugin_manager=self.plugin_manager)

        log.debug(
            f"Registered plugins. [plugins={self.plugin_manager.list_name_plugin()}]"
        )

    def _register_internal_plugins(self, enabled_plugins):
        """Registers all internal plugins in `enabled_plugins`."""
        plugin_dir = Path(__file__).resolve().parent / "plugins"

        for plugin_path in plugin_dir.iterdir():
            plugin_name = plugin_path.stem

            if plugin_path.stem in enabled_plugins:
                plugin = importlib.import_module("moe.plugins." + plugin_name)
                self.plugin_manager.register(plugin, plugin_name)
