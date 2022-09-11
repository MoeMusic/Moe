"""Tests the musicbrainz plugin."""

import datetime
from unittest.mock import MagicMock, call, patch

import pytest

import tests.plugins.musicbrainz.resources as mb_rsrc
from moe.config import ConfigValidationError
from moe.plugins import musicbrainz as moe_mb
from moe.plugins.musicbrainz.mb_core import MBAuthError


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
    return tmp_config(
        settings="""
    default_plugins = ['musicbrainz']

    [musicbrainz]
    username = "slim shady"
    password = "my name is"
    """
    )


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

        mock_gma.assert_called_once_with(config, mock_album)
        assert candidates == [mock_album]


class TestCollectionsAutoRemove:
    """Test the collection auto remove functionality."""

    def test_auto_remove_true(self, mock_album, mb_config):
        """Remove items from the collection if `auto_remove` is true."""
        mock_album.mb_album_id = "184"
        mb_config.settings.musicbrainz.collection.auto_remove = True

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.plugin_manager.hook.process_removed_items(
                config=mb_config, items=[mock_album]
            )

        mock_rm_releases_call.assert_called_once_with(
            mb_config, {mock_album.mb_album_id}
        )

    def test_all_items(self, album_factory, mb_config):
        """Remove all items from the collection if `auto_remove` is true."""
        album1 = album_factory(mb_album_id="1")
        album2 = album_factory(mb_album_id="2")
        mb_config.settings.musicbrainz.collection.auto_remove = True

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.plugin_manager.hook.process_removed_items(
                config=mb_config, items=[album1, album2]
            )

        mock_rm_releases_call.assert_called_once_with(
            mb_config, {album1.mb_album_id, album2.mb_album_id}
        )

    def test_auto_remove_false(self, mock_album, mb_config):
        """Don't remove any items from the collection if `auto_remove` set to false."""
        mb_config.settings.musicbrainz.collection.auto_remove = False

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.plugin_manager.hook.process_removed_items(
                config=mb_config, items=[mock_album]
            )

        mock_rm_releases_call.assert_not_called()

    def test_no_releases_to_remove(self, mock_album, mb_config):
        """Don't remove any items if there are no releases."""
        mock_album.mb_album_id = None
        mb_config.settings.musicbrainz.collection.auto_remove = True

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.plugin_manager.hook.process_removed_items(
                config=mb_config, items=[mock_album]
            )

        mock_rm_releases_call.assert_not_called()

    def test_invalid_credentials(self, caplog, mock_album, mb_config):
        """Don't raise an error if bad credentials, just log."""
        mb_config.settings.musicbrainz.collection.auto_remove = True
        mock_album.mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"

        with patch.object(
            moe_mb.mb_core,
            "rm_releases_from_collection",
            autospec=True,
            side_effect=MBAuthError,
        ):
            mb_config.plugin_manager.hook.process_removed_items(
                config=mb_config, items=[mock_album]
            )

        assert any(record.levelname == "ERROR" for record in caplog.records)


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
            mb_config, {mock_album.mb_album_id}
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

    def test_invalid_credentials(self, caplog, mock_album, mb_config):
        """Don't raise an error if bad credentials, just log an error."""
        mb_config.settings.musicbrainz.collection.auto_add = True
        mock_album.mb_album_id = "123"

        with patch.object(
            moe_mb.mb_core,
            "add_releases_to_collection",
            autospec=True,
            side_effect=MBAuthError,
        ):
            mb_config.plugin_manager.hook.process_new_items(
                config=mb_config, items=[mock_album]
            )

        assert any(record.levelname == "ERROR" for record in caplog.records)


class TestGetMatchingAlbum:
    """Test `get_matching_album()`."""

    @pytest.mark.network
    def test_network(self, album_factory, mb_config):
        """Make sure we can actually hit the real API.

        Since `get_matching_album` also calls `get_album_by_id`, this test serves as a
        network test for both.
        """
        album = album_factory(
            config=mb_config,
            artist="Kanye West",
            title="My Beautiful Dark Twisted Fantasy",
        )

        mb_album = moe_mb.get_matching_album(mb_config, album)

        # don't test every field since we can't actually guarantee the accuracy of
        # musicbrainz's search results every time
        assert mb_album.artist == album.artist
        assert mb_album.title == album.title

    def test_album_search(self, album_factory, mock_mb_by_id, mb_config):
        """Searching for a release uses the expected parameters."""
        album = album_factory(
            config=mb_config,
            artist="Kanye West",
            title="My Beautiful Dark Twisted Fantasy",
            date=datetime.date(2010, 11, 22),
        )
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
            mb_album = moe_mb.get_matching_album(mb_config, album)

        mock_mb_search.assert_called_once_with(limit=1, **search_criteria)
        assert mb_album == mb_rsrc.full_release.album

    def test_dont_search_if_mbid(self, mock_album):
        """Use ``mb_album_id`` to search by id if it exists."""
        mock_album.mb_album_id = "1"
        mock_config = MagicMock()

        with patch.object(
            moe_mb.mb_core, "get_album_by_id", autospec=True
        ) as mock_mb_by_id:
            moe_mb.get_matching_album(mock_config, mock_album)

        mock_mb_by_id.assert_called_once_with(mock_config, mock_album.mb_album_id)


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

        mb_album = moe_mb.get_album_by_id(MagicMock(), mb_album_id)

        mock_mb_by_id.assert_called_once_with(
            mb_album_id, includes=moe_mb.mb_core.RELEASE_INCLUDES
        )
        assert mb_album == mb_rsrc.full_release.album

    def test_partial_date_year_mon(self, mock_mb_by_id):
        """If given date is missing the day, default to 1."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        mock_mb_by_id.return_value = mb_rsrc.partial_date.partial_date_year_mon

        mb_album = moe_mb.get_album_by_id(MagicMock(), mb_album_id)

        assert mb_album.date == datetime.date(1992, 12, 1)

    def test_partial_date_year(self, mock_mb_by_id):
        """If given date is missing the day and month, default to 1 for each."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        mock_mb_by_id.return_value = mb_rsrc.partial_date.partial_date_year

        mb_album = moe_mb.get_album_by_id(MagicMock(), mb_album_id)

        assert mb_album.date == datetime.date(1992, 1, 1)

    def test_multi_disc_release(self, mock_mb_by_id):
        """We can add a release with multiple discs."""
        mb_album_id = "3af9a6ca-c38a-41a7-a53c-32a97e869e8e"
        mock_mb_by_id.return_value = mb_rsrc.multi_disc.release

        mb_album = moe_mb.get_album_by_id(MagicMock(), mb_album_id)

        assert mb_album.disc_total == 2
        assert any(track.disc == 1 for track in mb_album.tracks)
        assert any(track.disc == 2 for track in mb_album.tracks)


class TestAddReleasesToCollection:
    """Test `add_releases_to_collection` function."""

    def test_add_release_to_collection(self, mb_config):
        """The right calls are made to the api when adding a release to a collection."""
        collection = "123"
        releases = {"122"}

        with patch.object(
            moe_mb.mb_core.musicbrainzngs, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            moe_mb.add_releases_to_collection(mb_config, releases, collection)

        mock_add_releases_call.assert_called_once_with(
            collection=collection, releases=releases
        )

    def test_get_collection_from_config(self, mb_config):
        """Use the collection in the config if not specified."""
        mb_config.settings.musicbrainz.collection.collection_id = "123"
        releases = {"89"}

        with patch.object(
            moe_mb.mb_core.musicbrainzngs, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            moe_mb.add_releases_to_collection(mb_config, releases)

        mock_add_releases_call.assert_called_once_with(
            collection=mb_config.settings.musicbrainz.collection.collection_id,
            releases=releases,
        )

    def test_set_credentials(self, mb_config):
        """Set the user credentials for use."""
        with patch.object(
            moe_mb.mb_core.musicbrainzngs, "add_releases_to_collection", autospec=True
        ):
            with patch.object(
                moe_mb.mb_core.musicbrainzngs, "auth", autospec=True
            ) as mock_auth_call:
                moe_mb.add_releases_to_collection(mb_config, {"432"}, "1")

        mock_auth_call.assert_called_once_with(
            mb_config.settings.musicbrainz.username,
            mb_config.settings.musicbrainz.password,
        )

    @pytest.mark.network
    def test_invalid_credentials(self, mb_config):
        """Raise MBAuthError if invalid user credentials given."""
        collection = "56418762-9bbd-4d67-b6cf-30cd36d93cd1"
        releases = {"11b6532c-0de0-45bb-84fc-7e99514a4cd5"}
        mb_config.settings.musicbrainz.username = "my name is"
        mb_config.settings.musicbrainz.password = "slim shady"

        with pytest.raises(moe_mb.MBAuthError):
            moe_mb.add_releases_to_collection(mb_config, releases, collection)


class TestRmReleasesFromCollection:
    """Test `rm_releases_from_collection` function."""

    def test_remove_release_from_collection(self, mb_config):
        """The right calls are made when removing a release from a collection."""
        collection = "123"
        releases = {"122"}

        with patch.object(
            moe_mb.mb_core.musicbrainzngs,
            "remove_releases_from_collection",
            autospec=True,
        ) as mock_remove_releases_call:
            moe_mb.rm_releases_from_collection(mb_config, releases, collection)

        mock_remove_releases_call.assert_called_once_with(
            collection=collection, releases=releases
        )

    def test_get_collection_from_config(self, mb_config):
        """Use the collection in the config if not specified."""
        mb_config.settings.musicbrainz.collection.collection_id = "123"
        releases = {"123"}

        with patch.object(
            moe_mb.mb_core.musicbrainzngs,
            "remove_releases_from_collection",
            autospec=True,
        ) as mock_remove_releases_call:
            moe_mb.rm_releases_from_collection(mb_config, releases)

        mock_remove_releases_call.assert_called_once_with(
            collection=mb_config.settings.musicbrainz.collection.collection_id,
            releases=releases,
        )

    def test_set_credentials(self, mb_config):
        """Set the user credentials for use."""
        with patch.object(
            moe_mb.mb_core.musicbrainzngs,
            "remove_releases_from_collection",
            autospec=True,
        ):
            with patch.object(
                moe_mb.mb_core.musicbrainzngs, "auth", autospec=True
            ) as mock_auth_call:
                moe_mb.rm_releases_from_collection(mb_config, set("123"), "1")

        mock_auth_call.assert_called_once_with(
            mb_config.settings.musicbrainz.username,
            mb_config.settings.musicbrainz.password,
        )

    @pytest.mark.network
    def test_invalid_credentials(self, mb_config):
        """Raise MBAuthError if invalid user credentials given."""
        collection = "56418762-9bbd-4d67-b6cf-30cd36d93cd1"
        releases = {"11b6532c-0de0-45bb-84fc-7e99514a4cd5"}
        mb_config.settings.musicbrainz.username = "my name is"
        mb_config.settings.musicbrainz.password = "slim shady"

        with pytest.raises(moe_mb.MBAuthError):
            moe_mb.rm_releases_from_collection(mb_config, releases, collection)


class TestSetCollection:
    """Test ``set_collection``."""

    def test_fetch_releases(self, mb_config):
        """We are fetching releases from the collection."""
        mb_config.settings.musicbrainz.collection.collection_id = "123"

        with patch.object(
            moe_mb.mb_core.musicbrainzngs, "get_releases_in_collection", autospec=True
        ) as mock_get_releases_call:
            with patch.object(
                moe_mb.mb_core, "rm_releases_from_collection", autospec=True
            ):
                with patch.object(
                    moe_mb.mb_core, "add_releases_to_collection", autospec=True
                ):
                    moe_mb.set_collection(mb_config, {"1"})

        mock_get_releases_call.assert_called_once_with(
            collection=mb_config.settings.musicbrainz.collection.collection_id,
            limit=100,
            offset=0,
        )

    def test_fetch_releases_over_limit(self, mb_config):
        """We can fetch all the releases if a collection has > 100 (search limit)."""
        collection = "123"

        with patch.object(
            moe_mb.mb_core.musicbrainzngs,
            "get_releases_in_collection",
            autospec=True,
            side_effect=[mb_rsrc.create_collection(100), mb_rsrc.create_collection(71)],
        ) as mock_get_releases_call:
            with patch.object(
                moe_mb.mb_core, "rm_releases_from_collection", autospec=True
            ):
                with patch.object(
                    moe_mb.mb_core, "add_releases_to_collection", autospec=True
                ):
                    moe_mb.set_collection(mb_config, {"1"}, collection)

        expected_calls = [
            call(collection=collection, limit=100, offset=0),
            call(collection=collection, limit=100, offset=100),
        ]
        mock_get_releases_call.assert_has_calls(expected_calls)
        assert mock_get_releases_call.call_count == len(expected_calls)

    def test_add_releases(self, mb_config):
        """Add releases to the collection if they are not present already."""
        collection_id = "123"
        collection = mb_rsrc.create_collection(3)
        releases = {"2", "3"}  # 2 already exists, 3 is new

        with patch.object(
            moe_mb.mb_core.musicbrainzngs,
            "get_releases_in_collection",
            autospec=True,
            return_value=collection,
        ):
            with patch.object(
                moe_mb.mb_core, "rm_releases_from_collection", autospec=True
            ):
                with patch.object(
                    moe_mb.mb_core, "add_releases_to_collection", autospec=True
                ) as mock_add_releases:
                    moe_mb.set_collection(mb_config, releases, collection_id)

        mock_add_releases.assert_called_once_with(mb_config, {"3"}, collection_id)

    def test_rm_releases(self, mb_config):
        """Remove releases from the collection if they are in `releases`."""
        collection_id = "123"
        collection = mb_rsrc.create_collection(3)
        releases = {"1", "2"}  # does not include 0

        with patch.object(
            moe_mb.mb_core.musicbrainzngs,
            "get_releases_in_collection",
            autospec=True,
            return_value=collection,
        ):
            with patch.object(
                moe_mb.mb_core, "rm_releases_from_collection", autospec=True
            ) as mock_rm_releases:
                with patch.object(
                    moe_mb.mb_core, "add_releases_to_collection", autospec=True
                ):
                    moe_mb.set_collection(mb_config, releases, collection_id)

        mock_rm_releases.assert_called_once_with(mb_config, {"0"}, collection_id)

    def test_get_collection_from_config(self, mb_config):
        """Use the collection in the config if not specified."""
        mb_config.settings.musicbrainz.collection.collection_id = "123"

        with patch.object(
            moe_mb.mb_core.musicbrainzngs, "get_releases_in_collection", autospec=True
        ) as mock_set_releases:
            with patch.object(
                moe_mb.mb_core, "rm_releases_from_collection", autospec=True
            ):
                with patch.object(
                    moe_mb.mb_core, "add_releases_to_collection", autospec=True
                ):
                    moe_mb.set_collection(mb_config, {"89"})

        mock_set_releases.assert_called_once_with(
            collection=mb_config.settings.musicbrainz.collection.collection_id,
            limit=100,
            offset=0,
        )

    def test_set_credentials(self, mb_config):
        """Set the user credentials for use."""
        with patch.object(
            moe_mb.mb_core.musicbrainzngs, "get_releases_in_collection", autospec=True
        ):
            with patch.object(
                moe_mb.mb_core, "rm_releases_from_collection", autospec=True
            ):
                with patch.object(
                    moe_mb.mb_core, "add_releases_to_collection", autospec=True
                ):
                    with patch.object(
                        moe_mb.mb_core.musicbrainzngs, "auth", autospec=True
                    ) as mock_auth_call:
                        moe_mb.set_collection(mb_config, {"123"}, "1")

        mock_auth_call.assert_called_once_with(
            mb_config.settings.musicbrainz.username,
            mb_config.settings.musicbrainz.password,
        )

    @pytest.mark.network
    def test_invalid_credentials(self, mock_album, mb_config):
        """Raise MBAuthError if invalid user credentials given."""
        collection = "56418762-9bbd-4d67-b6cf-30cd36d93cd1"
        releases = {"11b6532c-0de0-45bb-84fc-7e99514a4cd5"}
        mb_config.settings.musicbrainz.username = "my name is"
        mb_config.settings.musicbrainz.password = "slim shady"

        with pytest.raises(moe_mb.MBAuthError):
            moe_mb.set_collection(mb_config, releases, collection)


class TestUpdateAlbum:
    """Test ``update_album``."""

    def test_update_album(self, album_factory, mb_config):
        """We can update a given album."""
        old_album = album_factory(title="old", mb_album_id="1", config=mb_config)
        new_album = album_factory(title="new", config=mb_config)

        with patch.object(
            moe_mb.mb_core, "get_album_by_id", autospec=True, return_value=new_album
        ) as mock_album_by_id:
            moe_mb.update_album(mb_config, old_album)

        assert old_album.title == new_album.title
        mock_album_by_id.assert_called_once_with(mb_config, old_album.mb_album_id)

    def test_no_id(self, mock_album):
        """Raise ValueError if not mb album id present."""
        mock_album.mb_album_id = None

        with patch.object(moe_mb.mb_core, "get_album_by_id", autospec=True):
            with pytest.raises(ValueError, match=r"album="):
                moe_mb.update_album(MagicMock(), mock_album)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation.

    Note:
        The hook implementation exists in the `__init__.py` of the plugin.
    """

    def test_musicbrainz_core(self, tmp_config):
        """Enable the musicbrainz core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["musicbrainz"]')

        assert config.plugin_manager.has_plugin("musicbrainz_core")
