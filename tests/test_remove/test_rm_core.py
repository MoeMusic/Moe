"""Test the core api of the ``remove`` plugin."""

from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.track import Track
from moe.plugins import remove as moe_rm


class TestRemoveItem:
    """Tests `remove_item()`."""

    def test_track(self, tmp_session, mock_track):
        """Tracks are removed from the database with valid query."""
        tmp_session.add(mock_track)
        tmp_session.commit()

        moe_rm.remove_item(mock_track, tmp_session)

        assert not tmp_session.query(Track).scalar()

    def test_album(self, tmp_session, mock_album):
        """Albums are removed from the database with valid query."""
        mock_album = tmp_session.merge(mock_album)
        tmp_session.commit()

        moe_rm.remove_item(mock_album, tmp_session)

        assert not tmp_session.query(Album).scalar()

    def test_extra(self, tmp_session, mock_extra):
        """Extras are removed from the database with valid query."""
        tmp_session.add(mock_extra)
        tmp_session.commit()

        moe_rm.remove_item(mock_extra, tmp_session)

        assert not tmp_session.query(Extra).scalar()
