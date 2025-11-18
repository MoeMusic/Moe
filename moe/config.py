"""User configuration of moe.

Each instance of Moe should only create a single `Config` object. This object will
contain all user settings and other related information and is set upon initializing
the configuration for the first time i.e. calling `Config()`. Once initialized, the
config can be accessed through import and should be treated as a constant::

    from moe import config
    print(config.CONFIG.settings.library_path)

Any application requiring use of the database should initiate a single sqlalchemy
'session'. This session should use ``moe_sessionmaker`` to instantiate a session to
connect to the database::

    with moe_sessionmaker.begin() as session:
        # do work

See Also:
    * `The sqlalchemy Session docs
      <https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-basics>`
    * ``moe/cli.py`` for an example on how the CLI handles creating the configuration
      and database connection via the session.
"""

import importlib.metadata
import logging
import os
import re
import sys
from itertools import chain
from pathlib import Path
from types import ModuleType
from typing import Any, NamedTuple, cast

import alembic.command
import alembic.config
import dynaconf
import dynaconf.base
import dynaconf.validator
import pluggy
import sqlalchemy
import sqlalchemy.event
import sqlalchemy.orm
from sqlalchemy.engine.base import Connection

import moe

moe_sessionmaker = sqlalchemy.orm.sessionmaker(autoflush=False)

__all__ = ["CONFIG", "Config", "ConfigValidationError", "ExtraPlugin"]

log = logging.getLogger("moe.config")

DEFAULT_PLUGINS = {
    "add": "moe.add",
    "cli": "moe.cli",
    "duplicate": "moe.duplicate",
    "edit": "moe.edit",
    "import": "moe.moe_import",
    "list": "moe.list",
    "move": "moe.move",
    "read": "moe.read",
    "remove": "moe.remove",
    "write": "moe.write",
}
OFFICIAL_PLUGINS = {
    "musicbrainz": "moe.plugins.musicbrainz",
    "transcode": "moe.plugins.transcode",
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
    def add_config_validator(settings: dynaconf.base.LazySettings) -> None:
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
    def add_hooks(pm: pluggy._manager.PluginManager) -> None:
        """Add hookspecs to be registered to Moe.

        Args:
            pm: PluginManager that registers the hookspec.

        Example:
            .. code:: python

                from moe.add import Hooks
                pm.add_hookspecs(Hooks)
        """

    @staticmethod
    @moe.hookspec
    def plugin_registration() -> None:
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
        """

    @staticmethod
    @moe.hookspec
    def register_sa_event_listeners() -> None:
        """Registers new sqlalchemy event listeners.

        These listeners will automatically apply to all sessions globally if the
        `Session` class is passed as the listener target as shown in the example.

        Important:
            This hook is for Moe internal use only and should not be used by plugins.

        Example:
            .. code:: python

                sqlalchemy.event.listen(
                    Session,
                    "before_flush",
                    _my_func,
                )

            Then you can define ``_my_func`` as such::

                def _my_func(
                    session: sqlalchemy.orm.Session,
                    flush_context: sqlalchemy.orm.UOWTransaction,
                    instances: Any | None,
                ):
                    print("we made it")

        See Also:
            `SQLAlchemy ORM event documentation <https://docs.sqlalchemy.org/en/20/orm/events.html>`_
        """


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings) -> None:
    """Validate move plugin configuration settings."""
    moe_validators = [
        dynaconf.Validator("DEFAULT_PLUGINS", default=DEFAULT_PLUGINS),
        dynaconf.Validator("DISABLE_PLUGINS", default=set()),
        dynaconf.Validator("ENABLE_PLUGINS", default=set()),
        dynaconf.Validator("LIBRARY_PATH", default="~/Music"),
        dynaconf.Validator("ORIGINAL_DATE", default=False),
    ]
    settings.validators.register(*moe_validators)  # type: ignore[reportCallIssue, reportAttributeAccessIssue]


class ExtraPlugin(NamedTuple):
    """Used to specify extra plugins when initializing the config.

    Attributes:
        plugin: This is the class or module of the plugin to register.
        name: Name to register the plugin under.
    """

    plugin: type | ModuleType
    name: str


class Config:
    """Initializes moe configuration settings and database.

    Attributes:
        config_dir (Path): Filesystem path of the configuration directory.
        config_file (Path): Filesystem path of the configuration settings file.
        enabled_plugins (set[str]): Enabled plugins as specified by the configuration.
        engine (sa.engine.base.Engine): Database engine in use.
        pm (pluggy._manager.PluginManager): Plugin manager that handles plugin logic.
        settings (dynaconf.base.LazySettings): User configuration settings.
    """

    def __init__(
        self,
        config_dir: Path | None = None,
        settings_filename: str = "config.toml",
        extra_plugins: list[ExtraPlugin] | None = None,
        engine: sqlalchemy.engine.base.Engine | None = None,
        *,
        init_db: bool = True,
    ) -> None:
        """Initializes the plugin manager and configuration directory.

        Args:
            config_dir: Filesystem path of the configuration directory where the
                settings and database files will reside. The environment variable
                ``MOE_CONFIG_DIR`` has precedence in setting this. If ``None`` given,
                the config directory defaults to ``~/.config/moe``.
            extra_plugins: Any extra plugins that should be enabled in addition to those
                specified in the configuration.
            settings_filename: Name of the configuration settings file.
            engine: sqlalchemy database engine to use. Defaults to a sqlite db located
                in the ``config_dir``.
            init_db: Whether or not to initialize the database.
        """
        global CONFIG  # noqa: PLW0603 best way I've found to make CONFIG easily accessible
        CONFIG = self

        try:
            self.config_dir = Path(os.environ["MOE_CONFIG_DIR"])
        except KeyError:
            self.config_dir = config_dir or Path.home() / ".config" / "moe"

        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = self.config_dir / settings_filename
        self._extra_plugins = extra_plugins or []
        self._read_config()

        self.engine = engine
        if init_db:
            self._init_db()

    def _init_db(self, *, create_tables: bool = True) -> None:
        """Initializes the database.

        Moe uses sqlite by default.

        Args:
            create_tables: Whether or not to create and update the db tables.
                If doing db migrations manually, e.g. in alembic, this should be False.
        """
        log.debug(f"Initializing database. [{create_tables=}]")

        db_path = self.config_dir / "library.db"

        if not self.engine:
            self.engine = sqlalchemy.create_engine("sqlite:///" + str(db_path))

        moe_sessionmaker.configure(bind=self.engine)

        # create and update database tables
        if create_tables:
            config_path = Path(__file__)
            alembic_cfg = alembic.config.Config(
                str(config_path.parents[0] / "moe_alembic" / "alembic.ini")
            )
            alembic_cfg.attributes["configure_logger"] = False
            with self.engine.begin() as connection:
                alembic_cfg.attributes["connection"] = connection
                alembic.command.upgrade(alembic_cfg, "head")

        self.pm.hook.register_sa_event_listeners()

        # create regular expression function for sqlite queries
        @sqlalchemy.event.listens_for(self.engine, "begin")
        def sqlite_engine_connect(conn: Connection) -> None:
            """Use the python re module for sqlite regex functionality.

            Args:
                conn: Raw DB-API connection object
            """
            conn.connection.create_function("regexp", 2, _regexp, deterministic=True)  # type: ignore[reportAttributeAccessIssue]

        def _regexp(pattern: str, col_value: object) -> bool:
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

    def _read_config(self) -> None:
        """Reads the user configuration settings.

        Searches for a configuration file at `config_dir / "config.toml"`.

        Raises:
            ConfigValidationError: Unable to parse the configuration file.
        """
        from moe.library.lib_item import (  # noqa: PLC0415 prevent circular import
            PathType,
        )

        log.debug(f"Reading configuration file. [config_file={self.config_file}]")

        self.config_file.touch(exist_ok=True)

        self.settings = cast(
            "Any",
            dynaconf.Dynaconf(
                envvar_prefix="MOE",  # export envvars with `export MOE_FOO=bar`
                settings_file=str(self.config_file.resolve()),
            ),
        )  # cast to Any until dynaconf implements proper type stubs

        self._setup_plugins()
        self.pm.hook.add_config_validator(settings=self.settings)
        self._validate_settings()

        PathType.library_path = Path(self.settings.library_path)

    def _validate_settings(self) -> None:
        """Validates the given user configuration.

        Raises:
            ConfigValidationError: Error validating the configuration.
        """
        log.debug("Validating configuration settings.")

        try:
            self.settings.validators.validate()
        except dynaconf.validator.ValidationError as err:
            raise ConfigValidationError(err) from err

    def _setup_plugins(self) -> None:
        """Setup pm and hook logic."""
        log.debug("Setting up plugins.")

        self.pm = cast(
            "Any", pluggy.PluginManager("moe")
        )  # avoids pluggy hook type errors

        # register core modules that cannot be disabled by the config
        for plugin_name, module in CORE_PLUGINS.items():
            self.pm.register(importlib.import_module(module), plugin_name)

        # need to validate `config` settings separately so we have access to them
        self.pm.add_hookspecs(Hooks)
        self.pm.hook.add_config_validator(settings=self.settings)
        self._validate_settings()

        self._register_enabled_plugins()

        # register plugin hookspecs for all enabled plugins
        self.pm.hook.add_hooks(pm=self.pm)

        log.debug(f"Registered plugins. [plugins={self.pm.list_name_plugin()}]")

    def _register_enabled_plugins(self) -> None:
        """Registers all enabled plugins in the configuration."""
        self.enabled_plugins = (
            set(self.settings.default_plugins) | set(self.settings.enable_plugins)
        ) - set(self.settings.disable_plugins)

        log.debug(f"Registering enabled plugins. {self.enabled_plugins=}")

        # register default plugins
        for plugin_name, module in chain(
            DEFAULT_PLUGINS.items(), OFFICIAL_PLUGINS.items()
        ):
            if plugin_name in self.enabled_plugins:
                self.pm.register(importlib.import_module(module), plugin_name)

        # register local user plugins
        if Path(self.config_dir / "plugins").exists():
            sys.path.append(str(self.config_dir / "plugins"))
            self._register_local_plugins(
                self.enabled_plugins, self.config_dir / "plugins"
            )

        # register third-party installed plugins
        plugins = importlib.metadata.entry_points().select(group="moe.plugins")
        if plugins:
            for plugin in plugins:
                if plugin.name in self.enabled_plugins:
                    self.pm.register(plugin.load(), plugin.name)

        # register explicitly given extra plugins
        for extra_plugin in self._extra_plugins:
            self.pm.register(extra_plugin.plugin, extra_plugin.name)

        # register individual plugin sub-modules
        self.pm.hook.plugin_registration(pm=self.pm)

        # check if all enabled plugins were loaded
        for plugin in self.enabled_plugins:
            if not self.pm.has_plugin(plugin):
                log.warning(
                    f"Plugin {plugin!r} is enabled in the configuration but could not "
                    "be loaded. Is it installed?"
                )

    def _register_local_plugins(
        self, enabled_plugins: set[str], plugin_dir: Path, pkg_name: str = ""
    ) -> None:
        """Registers all internal plugins in `enabled_plugins`.

        Args:
            enabled_plugins: All enabled plugins as specified by the config.
            plugin_dir: Directory of plugins to register.
            pkg_name: Optional common package name the plugins belong to.
                Include the trailing '.'.
        """
        for plugin_path in plugin_dir.iterdir():
            plugin_name = plugin_path.stem

            if plugin_path.stem in enabled_plugins:
                plugin = importlib.import_module(pkg_name + plugin_name)
                self.pm.register(plugin, plugin_name)
