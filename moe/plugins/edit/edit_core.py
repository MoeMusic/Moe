"""Core interface for editing an item."""

import datetime
import logging
import re
import sys

from moe.library.lib_item import LibItem

__all__ = ["edit_item", "EditError"]

log = logging.getLogger("moe.edit")


class EditError(Exception):
    """Error editing an item in the library."""


def edit_item(item: LibItem, field: str, value: str):
    """Sets a LibItem's ``field`` to ``value``.

    Args:
        item: Library item to edit.
        field: Item field to edit.
        value: Value to set the item's field to.

    Raises:
        EditError: ``field`` is not a valid attribute or is not editable.
    """
    try:
        attr = getattr(item, field)
    except AttributeError as a_err:
        raise EditError(
            f"'{field}' is not a valid {type(item).__name__.lower()} field."
        ) from a_err

    non_editable_fields = ["path"]
    if field in non_editable_fields:
        raise EditError(f"'{field}' is not an editable field.")

    log.debug(f"Editing '{field}' to '{value}' for '{item}'.")
    if isinstance(attr, str):
        setattr(item, field, value)
    elif isinstance(attr, int):
        setattr(item, field, int(value))
    elif isinstance(attr, datetime.date):
        if (sys.version_info.major, sys.version_info.minor) < (3, 7):
            if not re.match(
                r"^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$", value  # noqa: FS003
            ):
                raise EditError("Date must be in format YYYY-MM-DD")
            date = value.split("-")
            setattr(
                item, field, datetime.date(int(date[0]), int(date[1]), int(date[2]))
            )
        else:
            try:
                setattr(item, field, datetime.date.fromisoformat(value))
            except ValueError as v_err:
                raise EditError("Date must be in format YYYY-MM-DD") from v_err
    else:
        raise EditError(f"Editing field of type '{type(attr)}' not supported.")
