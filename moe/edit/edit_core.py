"""Core interface for editing an item."""

import datetime
import logging

from sqlalchemy import Date, Integer

from moe.library import LibItem
from moe.library.lib_item import SetType

__all__ = ["EditError", "edit_item"]

log = logging.getLogger("moe.edit")


class EditError(Exception):
    """Error editing an item in the library."""


def edit_item(item: LibItem, field: str, value: str):  # noqa: C901
    """Sets a LibItem's ``field`` to ``value``.

    Args:
        item: Library item to edit.
        field: Item field to edit.
        value: Value to set the item's field to.

    Raises:
        EditError: ``field`` is not a valid attribute or is not editable.
    """
    log.debug(f"Editing item. [{item=!r}, {field=!r}, {value=!r}]")

    if field == "path":
        raise EditError(f"Non-editable field given. [{field=!r}]")

    try:
        attr = getattr(item.__class__, field)
    except AttributeError as a_err:
        if field in item.custom:
            item.custom[field] = value
            return

        raise EditError(f"Invalid field given. [{field=!r}]") from a_err

    try:
        column_type = attr.property.columns[0].type
    except AttributeError:
        # hybrid_property
        setattr(item, field, value)
        return

    if isinstance(column_type, Integer):
        setattr(item, field, int(value))
    elif isinstance(column_type, SetType):
        setattr(item, field, {value.strip() for value in value.split(";")})
    elif isinstance(column_type, Date):
        try:
            setattr(item, field, datetime.date.fromisoformat(value))
        except ValueError as v_err:
            raise EditError("Date must be in format YYYY-MM-DD") from v_err
    else:
        setattr(item, field, value)

    log.info(f"Item edited. [{item=!r}, {field=!r}, {value=!r}]")
