"""Any non-music item attached to an album such as log files are considered extras."""

import logging
from pathlib import Path, PurePath
from typing import Any, cast

import pluggy
from sqlalchemy import JSON, Column, Integer
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

import moe
from moe import config
from moe.library.album import Album
from moe.library.lib_item import LibItem, PathType, SABase

__all__ = ["Extra"]

log = logging.getLogger("moe.extra")


class Hooks:
    """Extra hook specifications."""

    @staticmethod
    @moe.hookspec
    def create_custom_extra_fields() -> dict[str, Any]:  # type: ignore
        """Creates new custom fields for an Extra.

        Returns:
            Dict of the field names to their default values or ``None`` for no default.

        Example:
            .. code:: python

                return {"my_new_field": "default value", "other_field": None}

            You can then access your new field as if it were a normal field::

                extra.my_new_field = "awesome new value"

        Important:
            Your custom field should follow the same naming rules as any other python
            variable i.e. no spaces, starts with a letter, and consists solely of
            alpha-numeric and underscore characters.
        """  # noqa: DAR202

    @staticmethod
    @moe.hookspec
    def is_unique_extra(extra: "Extra", other: "Extra") -> bool:  # type: ignore
        """Add new conditions to determine whether two extras are unique.

        "Uniqueness" is meant in terms of whether the two extras should be considered
        duplicates in the library. These additional conditions will be applied inside a
        extra's :meth:`is_unique` method.
        """


@moe.hookimpl
def add_hooks(pm: pluggy.manager.PluginManager):
    """Registers `extra` hookspecs to Moe."""
    from moe.library.extra import Hooks

    pm.add_hookspecs(Hooks)


class Extra(LibItem, SABase):
    """An Album can have any number of extra files such as logs, cues, etc.

    Attributes:
        album_obj (Album): Album the extra file belongs to.
        path (pathlib.Path): Filesystem path of the extra file.
    """

    __tablename__ = "extra"

    _id: int = cast(int, Column(Integer, primary_key=True))
    path: Path = cast(Path, Column(PathType, nullable=False, unique=True))
    _custom_fields: dict[str, Any] = cast(
        dict[str, Any],
        Column(
            MutableDict.as_mutable(JSON(none_as_null=True)),
            default="{}",
            nullable=False,
        ),
    )

    _album_id: int = cast(int, Column(Integer, ForeignKey("album._id")))
    album_obj: Album = relationship("Album", back_populates="extras")

    def __init__(self, album: Album, path: Path, **kwargs):
        """Creates an Extra.

        Args:
            album: Album the extra file belongs to.
            path: Filesystem path of the extra file.
            **kwargs: Any other fields to assign to the extra.
        """
        self._custom_fields = self._get_default_custom_fields()
        self._custom_fields_set = set(self._custom_fields)

        album.extras.append(self)
        self.path = path

        for key, value in kwargs.items():
            setattr(self, key, value)

        log.debug(f"Extra created. [extra={self!r}]")

    @property
    def fields(self) -> set[str]:
        """Returns any editable, extra fields."""
        return {"album_obj", "path"}.union(self._custom_fields)

    @property
    def rel_path(self) -> PurePath:
        """Returns the extra's path relative to its album's path."""
        return self.path.relative_to(self.album_obj.path)

    def is_unique(self, other: "Extra") -> bool:
        """Returns whether an extra is unique in the library from ``other``."""
        if self.path == other.path:
            return False

        custom_uniqueness = config.CONFIG.pm.hook.is_unique_extra(
            extra=self, other=other
        )
        if False in custom_uniqueness:
            return False

        return True

    def merge(self, other: "Extra", overwrite: bool = False):
        """Merges another extra into this one.

        Args:
            other: Other extra to be merged with the current extra.
            overwrite: Whether or not to overwrite self if a conflict exists.
        """
        log.debug(
            f"Merging extras. [extra_a={self!r}, extra_b={other!r}, {overwrite=!r}]"
        )

        omit_fields = {"album_obj"}
        for field in self.fields - omit_fields:
            other_value = getattr(other, field)
            self_value = getattr(self, field)
            if other_value and (overwrite or (not overwrite and not self_value)):
                setattr(self, field, other_value)

        log.debug(
            f"Extras merged. [extra_a={self!r}, extra_b={other!r}, {overwrite=!r}]"
        )

    def __eq__(self, other):
        """Compares Extras by their fields."""
        if not isinstance(other, Extra):
            return False

        for field in self.fields:
            if not hasattr(other, field) or (
                getattr(self, field) != getattr(other, field)
            ):
                return False

        return True

    def __lt__(self, other: "Extra") -> bool:
        """Sort based on album then path."""
        if self.album_obj == other.album_obj:
            return self.path < other.path

        return self.album_obj < other.album_obj

    def __repr__(self):
        """Represents an Extra using its path and album."""
        field_reprs = []
        omit_fields = {"album_obj"}
        for field in self.fields - omit_fields:
            if hasattr(self, field):
                field_reprs.append(f"{field}={getattr(self, field)!r}")
        repr_str = "Extra(" + ", ".join(field_reprs) + f", album='{self.album_obj}'"

        custom_field_reprs = []
        for custom_field, value in self._custom_fields.items():
            custom_field_reprs.append(f"{custom_field}={value}")
        if custom_field_reprs:
            repr_str += ", custom_fields=[" + ", ".join(custom_field_reprs) + "]"

        repr_str += ")"
        return repr_str

    def __str__(self):
        """String representation of an Extra."""
        return f"{self.album_obj}: {self.rel_path}"

    def _get_default_custom_fields(self) -> dict[str, Any]:
        """Returns the default custom extra fields."""
        return {
            field: default_val
            for plugin_fields in config.CONFIG.pm.hook.create_custom_extra_fields()
            for field, default_val in plugin_fields.items()
        }
