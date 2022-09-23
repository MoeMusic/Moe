"""Core api for removing items from the library."""

import logging

import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.orm.session import Session

from moe.config import MoeSession
from moe.library import Extra, LibItem, Track

__all__ = ["remove_item"]

log = logging.getLogger("moe.remove")


def remove_item(item: LibItem):
    """Removes an item from the library."""
    log.debug(f"Removing item from the library. [{item=!r}]")
    session = MoeSession()

    insp = sqlalchemy.inspect(item)
    if insp.persistent:
        session.delete(item)
    elif insp.pending:
        session.expunge(item)
        if isinstance(item, (Track, Extra)):
            item.album_obj = None  # type: ignore

    try:
        session.flush()
    except sqlalchemy.exc.InvalidRequestError:
        # session is currently flushing - delete in separate session to ensure it
        # occurs before any inserts or updates in the original session
        if insp.persistent:
            session.expunge(item)
            new_session = Session(session.connection())
            new_session.delete(item)
            new_session.flush()

    log.info(f"Removed item from the library. [{item=!r}]")
