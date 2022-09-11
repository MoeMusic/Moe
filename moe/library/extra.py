"""Any non-music item attached to an album such as log files are considered extras."""

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Optional, cast

import pluggy
from sqlalchemy import JSON, Column, Integer
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import joinedload, relationship
from sqlalchemy.schema import ForeignKey

import moe
from moe.config import Config, MoeSession
from moe.library import SABase
from moe.library.album import Album
from moe.library.lib_item import LibItem, PathType

# Makes hybrid_property's have the same typing as a normal properties.
# Use until the stubs are improved.
if TYPE_CHECKING:
    typed_hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import hybrid_property as typed_hybrid_property

__all__ = ["Extra"]

log = logging.getLogger("moe.extra")


class Hooks:
    """Extra hook specifications."""

    @staticmethod
    @moe.hookspec
    def create_custom_extra_fields(config: Config) -> list[str]:  # type: ignore
        """Creates new custom fields for an Extra.

        Args:
            config: Moe config.

        Returns:
            A list of any new fields you wish to create.

        Example:
            Inside your hook implementation::

                return "my_new_field"

            You can then access your new field as if it were a normal field::

                extra.my_new_field = "awesome new value"

        Important:
            Your custom field should follow the same naming rules as any other python
            variable i.e. no spaces, starts with a letter, and consists solely of
            alpha-numeric and underscore characters.
        """  # noqa: DAR202


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `extra` hookspecs to Moe."""
    from moe.library.extra import Hooks

    plugin_manager.add_hookspecs(Hooks)


class Extra(LibItem, SABase):
    """An Album can have any number of extra files such as logs, cues, etc.

    Attributes:
        album_obj (Album): Album the extra file belongs to.
        filename (str): Base file name of the extra file.
            Read-only. Set ``path`` instead.
        path (Path): Filesystem path of the extra file.
    """

    __tablename__ = "extras"

    _id: int = cast(int, Column(Integer, primary_key=True))
    path: Path = cast(Path, Column(PathType, nullable=False, unique=True))
    _custom_fields: dict[str, Optional[str]] = cast(
        dict[str, Optional[str]],
        Column(MutableDict.as_mutable(JSON(none_as_null=True))),
    )

    _album_id: int = cast(int, Column(Integer, ForeignKey("album._id")))
    album_obj: Album = relationship("Album", back_populates="extras")

    def __init__(self, config: Config, album: Album, path: Path, **kwargs):
        """Creates an Extra.

        Args:
            config: Moe config.
            album: Album the extra file belongs to.
            path: Filesystem path of the extra file.
            **kwargs: Any other fields to assign to the extra.
        """
        self.config = config
        self.__dict__["_custom_fields"] = {}
        custom_fields = config.plugin_manager.hook.create_custom_extra_fields(
            config=config
        )
        for plugin_fields in custom_fields:
            for plugin_field in plugin_fields:
                self._custom_fields[plugin_field] = None

        album.extras.append(self)
        self.path = path

        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)

        log.debug(f"Extra created. [extra={self!r}]")

    @typed_hybrid_property
    def filename(self) -> str:
        """Gets an Extra's filename."""
        return self.path.name

    def fields(self) -> tuple[str, ...]:
        """Returns the public fields, or non-method attributes, of an Extra."""
        return "filename", "path"

    def get_existing(self) -> Optional["Extra"]:
        """Gets a matching Extra in the library by its unique attributes.

        Returns:
            Duplicate extra or the same extra if it already exists in the library.
        """
        log.debug(f"Searching library for existing extra. [extra={self!r}]")

        session = MoeSession()
        existing_extra = (
            session.query(Extra)
            .filter(Extra.path == self.path)
            .options(joinedload("*"))
            .one_or_none()
        )
        if not existing_extra:
            log.debug("No matching extra found.")
            return None

        log.debug(f"Matching extra found. [match={existing_extra!r}]")
        return existing_extra

    def __eq__(self, other):
        """Compares Extras by their 'uniqueness' in the database."""
        if not isinstance(other, Extra):
            return False

        if self.path == other.path:
            return True

        return False

    def __lt__(self, other: "Extra") -> bool:
        """Sort based on album then path."""
        if self.album_obj == other.album_obj:
            return self.path < other.path

        return self.album_obj < other.album_obj

    def __repr__(self):
        """Represents an Extra using its path and album."""
        repr_fields = ["path"]
        field_reprs = []
        for field in repr_fields:
            if hasattr(self, field):
                field_reprs.append(f"{field}={getattr(self, field)!r}")
        repr_str = "Extra(" + ", ".join(field_reprs) + f", album={self.album_obj.title}"

        custom_field_reprs = []
        for custom_field, value in self._custom_fields.items():
            custom_field_reprs.append(f"{custom_field}={value}")
        if custom_field_reprs:
            repr_str += ", custom_fields=[" + ", ".join(custom_field_reprs) + "]"

        repr_str += ")"
        return repr_str

        return f"Extra(path={self.path}, album={self.album_obj.title})"

    def __str__(self):
        """String representation of an Extra."""
        return f"{self.album_obj}: {self.filename}"
