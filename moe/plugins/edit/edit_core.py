"""Core interface for editing an item."""

import datetime
import logging

from moe.library.lib_item import LibItem

__all__ = ["EditError", "edit_item"]

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
        try:
            setattr(item, field, datetime.date.fromisoformat(value))
        except ValueError as v_err:
            raise EditError("Date must be in format YYYY-MM-DD") from v_err
    else:
        raise EditError(f"Editing field of type '{type(attr)}' not supported.")
