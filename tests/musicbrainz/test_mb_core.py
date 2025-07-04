"""Tests the musicbrainz plugin."""

import copy
import datetime
from unittest.mock import MagicMock, call, patch

import pytest

import moe.plugins.musicbrainz as moe_mb
import tests.resources.musicbrainz as mb_rsrc
from moe import config
from moe.config import ConfigValidationError
from moe.library import Track
from tests.conftest import album_factory, track_factory


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

    def test_search_limit_default(self, tmp_config):
        """The search_limit option should default to 5."""
        config = tmp_config(settings="default_plugins = ['musicbrainz']")

        assert config.settings.musicbrainz.search_limit == 5  # noqa: PLR2004

    def test_search_limit_custom_value(self, tmp_config):
        """The search_limit option should accept custom values."""
        search_limit = 10
        config = tmp_config(
            settings=f"""
            default_plugins = ['musicbrainz']

            [musicbrainz]
            search_limit = {search_limit}
            """
        )

        assert config.settings.musicbrainz.search_limit == search_limit

    def test_search_limit_invalid_value(self, tmp_config):
        """The search_limit option should raise an error if set to less than 1."""
        with pytest.raises(ConfigValidationError):
            tmp_config(
                settings="""
                default_plugins = ['musicbrainz']

                [musicbrainz]
                search_limit = 0
                """
            )


class TestGetCandidates:
    """Test the ``get_candidates`` hook implementation."""

    @pytest.mark.network
    def test_network(self, mb_config):
        """Make sure we can actually hit the real API.

        Since `get_matching_album` also calls `get_album_by_id`, this test serves as a
        network test for both.
        """
        album = mb_rsrc.full_album()

        candidates = config.CONFIG.pm.hook.get_candidates(album=album)
        mb_album = candidates[0][0].album

        # don't test fields since we can't actually guarantee the accuracy of
        # musicbrainz's search results every time
        assert mb_album

    def test_search_limit_used(self, mb_config):
        """The search_limit config option should be used when searching musicbrainz."""
        album = album_factory(title="Test Album", artist="Test Artist")
        mb_config.settings.musicbrainz.search_limit = 3

        with (
            patch.object(
                moe_mb.mb_core.musicbrainzngs,
                "search_releases",
                autospec=True,
                return_value={"release-list": []},
            ) as mock_search,
            patch.object(moe_mb.mb_core, "get_candidate_by_id", autospec=True),
        ):
            mb_config.pm.hook.get_candidates(album=album)

        assert mock_search.call_count == 1
        assert (
            mock_search.call_args.kwargs["limit"]
            == mb_config.settings.musicbrainz.search_limit
        )


class TestCollectionsAutoRemove:
    """Test the collection auto remove functionality."""

    def test_auto_remove_true(self, mb_config):
        """Remove items from the collection if `auto_remove` is true."""
        album = album_factory(mb_album_id="184")
        mb_config.settings.musicbrainz.collection.auto_remove = True
        mock_session = MagicMock()

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.pm.hook.process_removed_items(session=mock_session, items=[album])

        mock_rm_releases_call.assert_called_once_with({album.custom["mb_album_id"]})

    def test_all_items(self, mb_config):
        """Remove all items from the collection if `auto_remove` is true."""
        album1 = album_factory(mb_album_id="1")
        album2 = album_factory(mb_album_id="2")
        mb_config.settings.musicbrainz.collection.auto_remove = True
        mock_session = MagicMock()

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.pm.hook.process_removed_items(
                session=mock_session, items=[album1, album2]
            )

        mock_rm_releases_call.assert_called_once_with(
            {album1.custom["mb_album_id"], album2.custom["mb_album_id"]}
        )

    def test_auto_remove_false(self, mb_config):
        """Don't remove any items from the collection if `auto_remove` set to false."""
        album = album_factory()
        mb_config.settings.musicbrainz.collection.auto_remove = False
        mock_session = MagicMock()

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.pm.hook.process_removed_items(session=mock_session, items=[album])

        mock_rm_releases_call.assert_not_called()

    def test_no_releases_to_remove(self, mb_config):
        """Don't remove any items if there are no releases."""
        album = album_factory()
        mb_config.settings.musicbrainz.collection.auto_remove = True
        mock_session = MagicMock()

        with patch.object(
            moe_mb.mb_core, "rm_releases_from_collection", autospec=True
        ) as mock_rm_releases_call:
            mb_config.pm.hook.process_removed_items(session=mock_session, items=[album])

        mock_rm_releases_call.assert_not_called()

    def test_invalid_credentials(self, caplog, mb_config):
        """Don't raise an error if bad credentials, just log."""
        mb_config.settings.musicbrainz.collection.auto_remove = True
        album = album_factory(mb_album_id="112dec42-65f2-3bde-8d7d-26deddde10b2")
        mock_session = MagicMock()

        with patch.object(
            moe_mb.mb_core,
            "rm_releases_from_collection",
            autospec=True,
            side_effect=moe_mb.MBAuthError,
        ):
            mb_config.pm.hook.process_removed_items(session=mock_session, items=[album])

        assert any(record.levelname == "ERROR" for record in caplog.records)


class TestCollectionsAutoAdd:
    """Test the collection auto add functionality in the `process_new_items` hook."""

    def test_auto_add_true(self, mb_config):
        """Add an album to the collection if `auto_add` is true."""
        album = album_factory(mb_album_id="184")
        mb_config.settings.musicbrainz.collection.auto_add = True

        with patch.object(
            moe_mb.mb_core, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            mb_config.pm.hook.process_new_items(session=MagicMock(), items=[album])

        mock_add_releases_call.assert_called_once_with({album.custom["mb_album_id"]})

    def test_auto_add_false(self, mb_config):
        """Don't add any items if `auto_add` set to false."""
        album = album_factory()
        mb_config.settings.musicbrainz.collection.auto_add = False

        with patch.object(
            moe_mb.mb_core, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            mb_config.pm.hook.process_new_items(session=MagicMock(), items=[album])

        mock_add_releases_call.assert_not_called()

    def test_no_releases_to_add(self, mb_config):
        """Don't add any items if there are no releases."""
        album = album_factory()
        mb_config.settings.musicbrainz.collection.auto_add = True

        with patch.object(
            moe_mb.mb_core, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            mb_config.pm.hook.process_new_items(session=MagicMock(), items=[album])

        mock_add_releases_call.assert_not_called()

    def test_invalid_credentials(self, caplog, mb_config):
        """Don't raise an error if bad credentials, just log an error."""
        mb_config.settings.musicbrainz.collection.auto_add = True
        album = album_factory(mb_album_id="123")

        with patch.object(
            moe_mb.mb_core,
            "add_releases_to_collection",
            autospec=True,
            side_effect=moe_mb.MBAuthError,
        ):
            mb_config.pm.hook.process_new_items(session=MagicMock(), items=[album])

        assert any(record.levelname == "ERROR" for record in caplog.records)


class TestSyncMetadata:
    """Test the `sync_metadata` hook implementation."""

    def test_sync_album(self, mb_config):
        """Albums are synced with musicbrainz when called."""
        old_album = album_factory(title="unsynced", mb_album_id="1")
        new_album = album_factory(title="synced")

        with patch.object(
            moe_mb.mb_core, "get_album_by_id", return_value=new_album
        ) as mock_id:
            config.CONFIG.pm.hook.sync_metadata(item=old_album)

        mock_id.assert_called_once_with(old_album.custom["mb_album_id"])
        assert old_album.title == "synced"

    def test_sync_track(self, mb_config):
        """Tracks are synced with musicbrainz when called."""
        old_track = track_factory(title="unsynced", mb_track_id="1")
        old_track.album.custom["mb_album_id"] = "2"
        new_track = track_factory(title="synced")

        with patch.object(
            moe_mb.mb_core, "get_track_by_id", return_value=new_track
        ) as mock_id:
            config.CONFIG.pm.hook.sync_metadata(item=old_track)

        mock_id.assert_called_once_with(
            old_track.custom["mb_track_id"], old_track.album.custom["mb_album_id"]
        )
        assert old_track.title == "synced"


class TestGetAlbumById:
    """Test `get_album_by_id()`.

    You can use the following code to print the result of a musicbrainz api query.

        def test_print_result(self):
            import musicbrainzngs
            album_id = "3af9a6ca-c38a-41a7-a53c-32a97e869e8e"
            includes = ["artist-credits", "recordings"]
            print(musicbrainzngs.get_release_by_id(album_id, includes))
            assert 0

    Make sure to add any ``includes`` for whatever is needed for the test.
    """

    def test_album_search(self, mock_mb_by_id, mb_config):
        """Searching for a release returns the expected album."""
        mb_album_id = "2fcfcaaa-6594-4291-b79f-2d354139e108"
        mock_mb_by_id.return_value = mb_rsrc.full_release.release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        mock_mb_by_id.assert_called_once_with(
            mb_album_id, includes=moe_mb.mb_core.RELEASE_INCLUDES
        )
        assert mb_album == mb_rsrc.full_album()
        for track in mb_album.tracks:
            assert track in mb_rsrc.full_album().tracks
        assert len(mb_album.tracks) == len(mb_rsrc.full_album().tracks)

    def test_partial_date_year_mon(self, mock_mb_by_id, mb_config):
        """If given date is missing the day, default to 1."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        release = copy.deepcopy(mb_rsrc.full_release.release)
        release["release"]["date"] = "1992-12"
        mock_mb_by_id.return_value = release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.date == datetime.date(1992, 12, 1)

    def test_partial_date_year(self, mock_mb_by_id, mb_config):
        """If given date is missing the day and month, default to 1 for each."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        release = copy.deepcopy(mb_rsrc.full_release.release)
        release["release"]["date"] = "1992"
        mock_mb_by_id.return_value = release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.date == datetime.date(1992, 1, 1)

    def test_multi_disc_release(self, mock_mb_by_id, mb_config):
        """We can add a release with multiple discs."""
        mb_album_id = "3af9a6ca-c38a-41a7-a53c-32a97e869e8e"
        mock_mb_by_id.return_value = mb_rsrc.multi_disc.release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.disc_total == 2  # noqa: PLR2004
        assert any(track.disc == 1 for track in mb_album.tracks)
        assert any(track.disc == 2 for track in mb_album.tracks)  # noqa: PLR2004

    def test_minimal_release(self, mock_mb_by_id, mb_config):
        """We can properly handle a release with minimal information."""
        mb_album_id = "c6bf7925-2f27-430c-a86d-d4d50e940631"
        mock_mb_by_id.return_value = mb_rsrc.min_release.release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        mock_mb_by_id.assert_called_once_with(
            mb_album_id, includes=moe_mb.mb_core.RELEASE_INCLUDES
        )
        assert mb_album == mb_rsrc.min_album()
        for track in mb_album.tracks:
            assert track in mb_rsrc.min_album().tracks
        assert len(mb_album.tracks) == len(mb_rsrc.min_album().tracks)

    def test_none_catalog_num(self, mock_mb_by_id, mb_config):
        """Set `catalog_nums` to an empty set if listed as [none] in musicbrainz."""
        mb_album_id = "2fcfcaaa-6594-4291-b79f-2d354139e108"
        release = copy.deepcopy(mb_rsrc.full_release.release)
        release["release"]["label-info-list"][0]["catalog-number"] = "[none]"
        release["release"]["label-info-list"] = release["release"]["label-info-list"][
            :1
        ]
        mock_mb_by_id.return_value = release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.catalog_nums == set()

    def test_missing_first_release_date(self, mock_mb_by_id, mb_config):
        """Handle missing first-release-date field gracefully without KeyError."""
        mb_album_id = "fe5f8a8e-4992-4e36-a7b6-b0c4c368a9a5"
        release = copy.deepcopy(mb_rsrc.full_release.release)

        if "first-release-date" in release["release"]["release-group"]:
            del release["release"]["release-group"]["first-release-date"]

        mock_mb_by_id.return_value = release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.original_date is None

    def test_missing_release_group(self, mock_mb_by_id, mb_config):
        """Handle missing release-group field gracefully without KeyError."""
        mb_album_id = "fe5f8a8e-4992-4e36-a7b6-b0c4c368a9a5"
        release = copy.deepcopy(mb_rsrc.full_release.release)

        if "release-group" in release["release"]:
            del release["release"]["release-group"]

        mock_mb_by_id.return_value = release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.original_date is None


class TestGetCandidateByID:
    """Test `get_candidate_by_id()`."""

    def test_album_search(self, mock_mb_by_id, mb_config):
        """Searching for a release returns the expected album."""
        mb_album_id = "2fcfcaaa-6594-4291-b79f-2d354139e108"
        mock_mb_by_id.return_value = mb_rsrc.full_release.release

        candidate = moe_mb.get_candidate_by_id(album_factory(), mb_album_id)

        mock_mb_by_id.assert_called_once_with(
            mb_album_id, includes=moe_mb.mb_core.RELEASE_INCLUDES
        )
        assert candidate.album == mb_rsrc.full_album()

    def test_minimal_release(self, mock_mb_by_id, mb_config):
        """We can properly handle a release with minimal information."""
        mb_album_id = "c6bf7925-2f27-430c-a86d-d4d50e940631"
        mock_mb_by_id.return_value = mb_rsrc.min_release.release

        candidate = moe_mb.get_candidate_by_id(album_factory(), mb_album_id)

        mock_mb_by_id.assert_called_once_with(
            mb_album_id, includes=moe_mb.mb_core.RELEASE_INCLUDES
        )
        assert candidate.album == mb_rsrc.min_album()


class TestGetTrackByID:
    """Test `get_track_by_id`."""

    def test_track_search(self, mock_mb_by_id):
        """We can't search for tracks so we search for albums and match tracks."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        mb_track_id = "219e6b01-c962-355c-8a87-5d4ab3fc13bc"
        mock_mb_by_id.return_value = mb_rsrc.full_release.release

        mb_track = moe_mb.get_track_by_id(mb_track_id, mb_album_id)

        assert mb_track.title == "Dark Fantasy"
        mock_mb_by_id.assert_called_once_with(
            mb_album_id, includes=moe_mb.mb_core.RELEASE_INCLUDES
        )

    def test_track_not_found(self, mock_mb_by_id):
        """Raise ValueError if track or album cannot be found."""
        mock_mb_by_id.return_value = mb_rsrc.full_release.release

        with pytest.raises(ValueError, match="track_id"):
            moe_mb.get_track_by_id("track id", "album id")


class TestCustomFields:
    """Test reading, writing, and setting musicbrainz custom fields."""

    def test_read_write(self, tmp_config):
        """We can read and write the custom fields."""
        tmp_config(settings="default_plugins = ['musicbrainz', 'write']")
        album = album_factory(mb_album_id="album id", exists=True)
        track = track_factory(album=album, mb_track_id="track id", exists=True)

        new_track = Track.from_file(track.path)

        assert new_track.album.custom["mb_album_id"] == "album id"
        assert new_track.custom["mb_track_id"] == "track id"


class TestAddReleasesToCollection:
    """Test `add_releases_to_collection` function."""

    def test_add_release_to_collection(self, mb_config):
        """The right calls are made to the api when adding a release to a collection."""
        collection = "123"
        releases = {"122"}

        with patch.object(
            moe_mb.mb_core.musicbrainzngs, "add_releases_to_collection", autospec=True
        ) as mock_add_releases_call:
            moe_mb.add_releases_to_collection(releases, collection)

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
            moe_mb.add_releases_to_collection(releases)

        mock_add_releases_call.assert_called_once_with(
            collection=mb_config.settings.musicbrainz.collection.collection_id,
            releases=releases,
        )

    def test_set_credentials(self, mb_config):
        """Set the user credentials for use."""
        with (
            patch.object(
                moe_mb.mb_core.musicbrainzngs,
                "add_releases_to_collection",
                autospec=True,
            ),
            patch.object(
                moe_mb.mb_core.musicbrainzngs, "auth", autospec=True
            ) as mock_auth_call,
        ):
            moe_mb.add_releases_to_collection({"432"}, "1")

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
            moe_mb.add_releases_to_collection(releases, collection)


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
            moe_mb.rm_releases_from_collection(releases, collection)

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
            moe_mb.rm_releases_from_collection(releases)

        mock_remove_releases_call.assert_called_once_with(
            collection=mb_config.settings.musicbrainz.collection.collection_id,
            releases=releases,
        )

    def test_set_credentials(self, mb_config):
        """Set the user credentials for use."""
        with (
            patch.object(
                moe_mb.mb_core.musicbrainzngs,
                "remove_releases_from_collection",
                autospec=True,
            ),
            patch.object(
                moe_mb.mb_core.musicbrainzngs, "auth", autospec=True
            ) as mock_auth_call,
        ):
            moe_mb.rm_releases_from_collection(set("123"), "1")

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
            moe_mb.rm_releases_from_collection(releases, collection)


class TestSetCollection:
    """Test ``set_collection``."""

    def test_fetch_releases(self, mb_config):
        """We are fetching releases from the collection."""
        mb_config.settings.musicbrainz.collection.collection_id = "123"

        with (
            patch.object(
                moe_mb.mb_core.musicbrainzngs,
                "get_releases_in_collection",
                autospec=True,
            ) as mock_get_releases_call,
            patch.object(moe_mb.mb_core, "rm_releases_from_collection", autospec=True),
            patch.object(moe_mb.mb_core, "add_releases_to_collection", autospec=True),
        ):
            moe_mb.set_collection({"1"})

        mock_get_releases_call.assert_called_once_with(
            collection=mb_config.settings.musicbrainz.collection.collection_id,
            limit=100,
            offset=0,
        )

    def test_fetch_releases_over_limit(self, mb_config):
        """We can fetch all the releases if a collection has > 100 (search limit)."""
        collection = "123"

        with (
            patch.object(
                moe_mb.mb_core.musicbrainzngs,
                "get_releases_in_collection",
                autospec=True,
                side_effect=[
                    mb_rsrc.create_collection(100),
                    mb_rsrc.create_collection(71),
                ],
            ) as mock_get_releases_call,
            patch.object(moe_mb.mb_core, "rm_releases_from_collection", autospec=True),
            patch.object(moe_mb.mb_core, "add_releases_to_collection", autospec=True),
        ):
            moe_mb.set_collection({"1"}, collection)

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

        with (
            patch.object(
                moe_mb.mb_core.musicbrainzngs,
                "get_releases_in_collection",
                autospec=True,
                return_value=collection,
            ),
            patch.object(moe_mb.mb_core, "rm_releases_from_collection", autospec=True),
            patch.object(
                moe_mb.mb_core, "add_releases_to_collection", autospec=True
            ) as mock_add_releases,
        ):
            moe_mb.set_collection(releases, collection_id)

        mock_add_releases.assert_called_once_with({"3"}, collection_id)

    def test_rm_releases(self, mb_config):
        """Remove releases from the collection if they are in `releases`."""
        collection_id = "123"
        collection = mb_rsrc.create_collection(3)
        releases = {"1", "2"}  # does not include 0

        with (
            patch.object(
                moe_mb.mb_core.musicbrainzngs,
                "get_releases_in_collection",
                autospec=True,
                return_value=collection,
            ),
            patch.object(
                moe_mb.mb_core, "rm_releases_from_collection", autospec=True
            ) as mock_rm_releases,
            patch.object(moe_mb.mb_core, "add_releases_to_collection", autospec=True),
        ):
            moe_mb.set_collection(releases, collection_id)

        mock_rm_releases.assert_called_once_with({"0"}, collection_id)

    def test_get_collection_from_config(self, mb_config):
        """Use the collection in the config if not specified."""
        mb_config.settings.musicbrainz.collection.collection_id = "123"

        with (
            patch.object(
                moe_mb.mb_core.musicbrainzngs,
                "get_releases_in_collection",
                autospec=True,
            ) as mock_set_releases,
            patch.object(moe_mb.mb_core, "rm_releases_from_collection", autospec=True),
            patch.object(moe_mb.mb_core, "add_releases_to_collection", autospec=True),
        ):
            moe_mb.set_collection({"89"})

        mock_set_releases.assert_called_once_with(
            collection=mb_config.settings.musicbrainz.collection.collection_id,
            limit=100,
            offset=0,
        )

    def test_set_credentials(self, mb_config):
        """Set the user credentials for use."""
        with (
            patch.object(
                moe_mb.mb_core.musicbrainzngs,
                "get_releases_in_collection",
                autospec=True,
            ),
            patch.object(moe_mb.mb_core, "rm_releases_from_collection", autospec=True),
            patch.object(moe_mb.mb_core, "add_releases_to_collection", autospec=True),
            patch.object(
                moe_mb.mb_core.musicbrainzngs, "auth", autospec=True
            ) as mock_auth_call,
        ):
            moe_mb.set_collection({"123"}, "1")

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
            moe_mb.set_collection(releases, collection)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation.

    Note:
        The hook implementation exists in the `__init__.py` of the plugin.
    """

    def test_musicbrainz_core(self, tmp_config):
        """Enable the musicbrainz core plugin if specified in the config."""
        tmp_config(settings='default_plugins = ["musicbrainz"]')

        assert config.CONFIG.pm.has_plugin("musicbrainz_core")
