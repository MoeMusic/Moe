"""Tests the musicbrainz plugin."""

import datetime
from unittest.mock import patch

import pytest

import tests.plugins.musicbrainz.resources as mb_rsrc
from moe.config import ConfigValidationError
from moe.plugins import musicbrainz as moe_mb


@pytest.fixture
def mock_mb_by_id():
    """Mock the musicbrainzngs api call `get_release_by_id`."""
    with patch.object(
        moe_mb.mb_core.musicbrainzngs, "get_release_by_id", autospec=True
    ) as mock_mb_by_id:
        yield mock_mb_by_id


@pytest.fixture
def mb_config(tmp_config):
    """Creates a configuration with a temporary library path."""
    return tmp_config(settings="default_plugins = ['musicbrainz']")


class TestConfiguration:
    """Test adding options and validation to the configuration."""

    def test_no_mb_settings(self, tmp_config):
        """Ensure we're safe-checking the config variables."""
        tmp_config(settings="default_plugins = ['musicbrainz']")

    def test_valid_config(self, tmp_config):
        """We're good if all the right values are present."""
        tmp_config(
            settings="""
            default_plugins = ['musicbrainz']

            [musicbrainz]
            username = "my_name_is"
            password = "slim_shady"

            [musicbrainz.collection]
            auto_add = true
            auto_remove = true
            collection_id = "123"
            """
        )

    def test_auto_add_no_collection_id(self, tmp_config):
        """If `auto_add` is true, a collection id must be present."""
        with pytest.raises(ConfigValidationError):
            tmp_config(
                settings="""
                default_plugins = ['musicbrainz']

                [musicbrainz.collection]
                auto_add = true
                """
            )

    def test_auto_remove_no_collection_id(self, tmp_config):
        """If `auto_remove` is true, a collection id must be present."""
        with pytest.raises(ConfigValidationError):
            tmp_config(
                settings="""
                default_plugins = ['musicbrainz']

                [musicbrainz.collection]
                auto_remove = true
                """
            )

    def test_login_required_no_password(self, tmp_config):
        """If an option requires a login, username and password must be present."""
        with pytest.raises(ConfigValidationError):
            tmp_config(
                settings="""
                default_plugins = ['musicbrainz']

                [musicbrainz]
                username = "my_name_is"

                [musicbrainz.collection]
                auto_add = true
                collection_id = "123"
                """
            )

    def test_login_required_no_username(self, tmp_config):
        """If an option requires a login, username and password must be present."""
        with pytest.raises(ConfigValidationError):
            tmp_config(
                settings="""
                default_plugins = ['musicbrainz']

                [musicbrainz]
                password = "slim shady"

                [musicbrainz.collection]
                auto_add = true
                collection_id = "123"
                """
            )


class TestImportCandidates:
    """Test the ``import_candidtates`` hook implementation."""

    def test_get_matching_albums(self, mock_album, tmp_config):
        """Get matching albums when searching for candidates to import."""
        config = tmp_config("default_plugins = ['import', 'musicbrainz']")

        with patch.object(
            moe_mb.mb_core, "get_matching_album", autospec=True
        ) as mock_gma:
            mock_gma.return_value = mock_album
            candidates = config.plugin_manager.hook.import_candidates(
                config=config, album=mock_album
            )

        mock_gma.assert_called_once_with(mock_album)
        assert candidates == [mock_album]


class TestCollectionsAutoRemove:
    """Test the collection auto remove functionality in the `post_remove` hook."""

    def test_auto_remove_true(self, mock_album, mb_config):
        """Remove items from the collection if `auto_remove` is true."""
        mock_album.mb_album_id = "184"
        mb_config.settings.musicbrainz.collection.auto_remove = True

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.plugin_manager.hook.post_remove(config=mb_config, item=mock_album)

        mock_rm_releases_call.assert_called_once_with(
            mb_config, None, [mock_album.mb_album_id]
        )

    def test_auto_remove_false(self, mock_album, mb_config):
        """Don't remove any items from the collection if `auto_remove` set to false."""
        mb_config.settings.musicbrainz.collection.auto_remove = False

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.plugin_manager.hook.post_remove(config=mb_config, item=mock_album)

        mock_rm_releases_call.assert_not_called()

    def test_no_releases_to_remove(self, mock_album, mb_config):
        """Don't remove any items if there are no releases."""
        mock_album.mb_album_id = None
        mb_config.settings.musicbrainz.collection.auto_remove = True

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.plugin_manager.hook.post_remove(config=mb_config, item=mock_album)

        mock_rm_releases_call.assert_not_called()

    @pytest.mark.network
    def test_invalid_credentials(self, mock_album, mb_config):
        """Don't raise an error if bad credentials, just log."""
        mb_config.settings.musicbrainz.username = "bad"
        mb_config.settings.musicbrainz.password = "invalid"
        mb_config.settings.musicbrainz.collection.collection_id = (
            "56418762-9bbd-4d67-b6cf-30cd36d93cd1"
        )
        mb_config.settings.musicbrainz.collection.auto_remove = True
        mock_album.mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"

        mb_config.plugin_manager.hook.post_remove(config=mb_config, item=mock_album)


class TestCollectionsAutoAdd:
    """Test the collection auto add functionality in the `process_new_items` hook."""

    def test_auto_add_true(self, mock_album, mb_config):
        """Add an album to the collection if `auto_add` is true."""
        mock_album.mb_album_id = "184"
        mb_config.settings.musicbrainz.collection.auto_add = True

        with patch.object(
            moe_mb.mb_core, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            mb_config.plugin_manager.hook.process_new_items(
                config=mb_config, items=[mock_album]
            )

        mock_add_releases_call.assert_called_once_with(
            mb_config, None, [mock_album.mb_album_id]
        )

    def test_auto_add_false(self, mock_album, mb_config):
        """Don't add any items if `auto_add` set to false."""
        mb_config.settings.musicbrainz.collection.auto_add = False

        with patch.object(
            moe_mb.mb_core, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            mb_config.plugin_manager.hook.process_new_items(
                config=mb_config, items=[mock_album]
            )

        mock_add_releases_call.assert_not_called()

    def test_no_releases_to_add(self, mock_album, mb_config):
        """Don't add any items if there are no releases."""
        mb_config.settings.musicbrainz.collection.auto_add = True
        mock_album.mb_album_id = None

        with patch.object(
            moe_mb.mb_core, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            mb_config.plugin_manager.hook.process_new_items(
                config=mb_config, items=[mock_album]
            )

        mock_add_releases_call.assert_not_called()

    @pytest.mark.network
    def test_invalid_credentials(self, mock_album, mb_config):
        """Don't raise an error if bad credentials, just log."""
        mb_config.settings.musicbrainz.username = "bad"
        mb_config.settings.musicbrainz.password = "invalid"
        mb_config.settings.musicbrainz.collection.collection_id = (
            "56418762-9bbd-4d67-b6cf-30cd36d93cd1"
        )
        mb_config.settings.musicbrainz.collection.auto_add = True
        mock_album.mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"

        mb_config.plugin_manager.hook.process_new_items(
            config=mb_config, items=[mock_album]
        )


class TestGetMatchingAlbum:
    """Test `get_matching_album()`."""

    @pytest.mark.network
    def test_network(self, mock_album):
        """Make sure we can actually hit the real API.

        Since `get_matching_album` also calls `get_album_by_id`, this test serves as a
        network test for both.
        """
        mock_album.artist = "Kanye West"
        mock_album.title = "My Beautiful Dark Twisted Fantasy"

        mb_album = moe_mb.get_matching_album(mock_album)

        # don't test every field since we can't actually guarantee the accuracy of
        # musicbrainz's search results every time
        assert mb_album.artist == mock_album.artist
        assert mb_album.title == mock_album.title

    def test_album_search(self, mock_album, mock_mb_by_id):
        """Searching for a release uses the expected parameters."""
        mock_album.artist = "Kanye West"
        mock_album.title = "My Beautiful Dark Twisted Fantasy"
        mock_album.date = datetime.date(2010, 11, 22)
        search_criteria = {
            "artist": "Kanye West",
            "release": "My Beautiful Dark Twisted Fantasy",
            "date": "2010-11-22",
        }
        mock_mb_by_id.return_value = mb_rsrc.full_release.release

        with patch.object(
            moe_mb.mb_core.musicbrainzngs,
            "search_releases",
            return_value=mb_rsrc.full_release.search,
            autospec=True,
        ) as mock_mb_search:
            mb_album = moe_mb.get_matching_album(mock_album)

        mock_mb_search.assert_called_once_with(limit=1, **search_criteria)
        assert mb_album == mb_rsrc.full_release.album

    def test_dont_search_if_mbid(self, mock_album):
        """Use ``mb_album_id`` to search by id if it exists."""
        mock_album.mb_album_id = "1"

        with patch.object(
            moe_mb.mb_core, "get_album_by_id", autospec=True
        ) as mock_mb_by_id:
            moe_mb.get_matching_album(mock_album)

        mock_mb_by_id.assert_called_once_with(mock_album.mb_album_id)


class TestGetAlbumById:
    """Test `get_album_by_id()`.

    You can use the following code to print the result of a musicbrainz api query.

        def test_print_result(self):
            id = "3af9a6ca-c38a-41a7-a53c-32a97e869e8e"
            includes = ["artist-credits", "recordings"]
            print(musicbrainzngs.get_release_by_id(id, includes))
            assert 0

    Make sure to add any ``includes`` for whatever is needed for the test.
    """

    def test_album_search(self, mock_mb_by_id):
        """Searching for a release returns the expected album."""
        mb_album_id = "2fcfcaaa-6594-4291-b79f-2d354139e108"
        mock_mb_by_id.return_value = mb_rsrc.full_release.release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        mock_mb_by_id.assert_called_once_with(
            mb_album_id, includes=moe_mb.mb_core.RELEASE_INCLUDES
        )
        assert mb_album == mb_rsrc.full_release.album

    def test_partial_date_year_mon(self, mock_mb_by_id):
        """If given date is missing the day, default to 1."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        mock_mb_by_id.return_value = mb_rsrc.partial_date.partial_date_year_mon

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.date == datetime.date(1992, 12, 1)

    def test_partial_date_year(self, mock_mb_by_id):
        """If given date is missing the day and month, default to 1 for each."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        mock_mb_by_id.return_value = mb_rsrc.partial_date.partial_date_year

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.date == datetime.date(1992, 1, 1)

    def test_multi_disc_release(self, mock_mb_by_id):
        """We can add a release with multiple discs."""
        mb_album_id = "3af9a6ca-c38a-41a7-a53c-32a97e869e8e"
        mock_mb_by_id.return_value = mb_rsrc.multi_disc.release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.disc_total == 2
        assert any(track.disc == 1 for track in mb_album.tracks)
        assert any(track.disc == 2 for track in mb_album.tracks)


class TestRmReleasesFromCollection:
    """Test `rm_releases_from_collection` function."""

    def test_remove_release_from_collection(self, mock_album, mb_config):
        """The right calls are made when removing a release from a collection."""
        collection = "123"
        mb_config.settings.musicbrainz.username = "my name is"
        mb_config.settings.musicbrainz.password = "slim shady"

        with patch.object(
            moe_mb.mb_core.musicbrainzngs,
            "remove_releases_from_collection",
            autospec=True,
        ) as mock_remove_releases_call:
            with patch.object(
                moe_mb.mb_core.musicbrainzngs, "auth", autospec=True
            ) as mock_auth_call:
                moe_mb.rm_releases_from_collection(
                    mb_config, collection, [mock_album.mb_album_id]
                )

        mock_remove_releases_call.assert_called_once_with(
            collection=collection, releases=[mock_album.mb_album_id]
        )
        mock_auth_call.assert_called_once_with(
            mb_config.settings.musicbrainz.username,
            mb_config.settings.musicbrainz.password,
        )

    def test_get_collection_from_config(self, mock_album, mb_config):
        """Use the collection in the config if not specified."""
        mb_config.settings.musicbrainz.collection.collection_id = "123"
        mb_config.settings.musicbrainz.username = "my name is"
        mb_config.settings.musicbrainz.password = "slim shady"

        with patch.object(
            moe_mb.mb_core.musicbrainzngs,
            "remove_releases_from_collection",
            autospec=True,
        ) as mock_remove_releases_call:
            with patch.object(
                moe_mb.mb_core.musicbrainzngs, "auth", autospec=True
            ) as mock_auth_call:
                moe_mb.rm_releases_from_collection(
                    mb_config, None, [mock_album.mb_album_id]
                )

        mock_remove_releases_call.assert_called_once_with(
            collection=mb_config.settings.musicbrainz.collection.collection_id,
            releases=[mock_album.mb_album_id],
        )
        mock_auth_call.assert_called_once_with(
            mb_config.settings.musicbrainz.username,
            mb_config.settings.musicbrainz.password,
        )

    @pytest.mark.network
    def test_invalid_credentials(self, mock_album, mb_config):
        """Raise MBAuthError if invalid user credentials given."""
        collection = "56418762-9bbd-4d67-b6cf-30cd36d93cd1"
        mock_album.mb_album_id = "11b6532c-0de0-45bb-84fc-7e99514a4cd5"
        mb_config.settings.musicbrainz.username = "my name is"
        mb_config.settings.musicbrainz.password = "slim shady"

        with pytest.raises(moe_mb.MBAuthError):
            moe_mb.rm_releases_from_collection(
                mb_config, collection, [mock_album.mb_album_id]
            )


class TestAddReleasesToCollection:
    """Test `add_releases_to_collection` function."""

    def test_add_release_to_collection(self, mock_album, mb_config):
        """The right calls are made to the api when adding a release to a collection."""
        collection = "123"
        mock_album.mb_album_id = "89"
        mb_config.settings.musicbrainz.username = "my name is"
        mb_config.settings.musicbrainz.password = "slim shady"

        with patch.object(
            moe_mb.mb_core.musicbrainzngs, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            with patch.object(
                moe_mb.mb_core.musicbrainzngs, "auth", autospec=True
            ) as mock_auth_call:
                moe_mb.add_releases_to_collection(
                    mb_config, collection, [mock_album.mb_album_id]
                )

        mock_add_releases_call.assert_called_once_with(
            collection=collection, releases=[mock_album.mb_album_id]
        )
        mock_auth_call.assert_called_once_with(
            mb_config.settings.musicbrainz.username,
            mb_config.settings.musicbrainz.password,
        )

    def test_get_collection_from_config(self, mock_album, mb_config):
        """Use the collection in the config if not specified."""
        mb_config.settings.musicbrainz.collection.collection_id = "123"
        mb_config.settings.musicbrainz.username = "my name is"
        mb_config.settings.musicbrainz.password = "slim shady"

        with patch.object(
            moe_mb.mb_core.musicbrainzngs, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            with patch.object(
                moe_mb.mb_core.musicbrainzngs, "auth", autospec=True
            ) as mock_auth_call:
                moe_mb.add_releases_to_collection(
                    mb_config, None, [mock_album.mb_album_id]
                )

        mock_add_releases_call.assert_called_once_with(
            collection=mb_config.settings.musicbrainz.collection.collection_id,
            releases=[mock_album.mb_album_id],
        )
        mock_auth_call.assert_called_once_with(
            mb_config.settings.musicbrainz.username,
            mb_config.settings.musicbrainz.password,
        )

    @pytest.mark.network
    def test_invalid_credentials(self, mock_album, mb_config):
        """Raise MBAuthError if invalid user credentials given."""
        collection = "56418762-9bbd-4d67-b6cf-30cd36d93cd1"
        mock_album.mb_album_id = "11b6532c-0de0-45bb-84fc-7e99514a4cd5"
        mb_config.settings.musicbrainz.username = "my name is"
        mb_config.settings.musicbrainz.password = "slim shady"

        with pytest.raises(moe_mb.MBAuthError):
            moe_mb.add_releases_to_collection(
                mb_config, collection, [mock_album.mb_album_id]
            )


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation.

    Note:
        The hook implementation exists in the `__init__.py` of the plugin.
    """

    def test_musicbrainz_core(self, tmp_config):
        """Enable the musicbrainz core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["musicbrainz"]')

        assert config.plugin_manager.has_plugin("musicbrainz_core")
