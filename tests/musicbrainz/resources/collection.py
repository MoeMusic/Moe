"""A collection and its releases from musicbrainz.

As returned by ``musicbrainzngs.get_releases_in_collection``.
"""


def create_collection(num_releases: int):
    """Creates a collection dict for parsing.

    The id of each release will be incremented from 0 to `num_releases - 1`.
    """
    release_list = []
    for release_num in range(num_releases):
        release_list.append(
            {
                "id": f"{str(release_num)}",
                "title": "The College Dropout",
                "status": "Official",
                "quality": "normal",
                "packaging": "Jewel Case",
                "text-representation": {"language": "eng", "script": "Latn"},
                "date": "2004-02-09",
                "country": "XE",
                "release-event-list": [
                    {
                        "date": "2004-02-09",
                        "area": {
                            "id": "89a675c2-3e37-3518-b83c-418bad59a85a",
                            "name": "Europe",
                            "sort-name": "Europe",
                            "iso-3166-1-code-list": ["XE"],
                        },
                    }
                ],
                "release-event-count": 1,
                "barcode": "602498617397",
            }
        )

    return {
        "collection": {
            "id": "56418762-9bbd-4d67-b6cf-30cd36d93cd1",
            "type": "Release collection",
            "entity-type": "release",
            "name": "My Collection",
            "editor": "kanye",
            "release-list": release_list,
            "release-count": num_releases,
        }
    }


# example of a collection as returned by musicbrainz
# note release-list[0]['id'] will be the release id on the actual result
collection = {
    "collection": {
        "id": "56418762-9bbd-4d67-b6cf-30cd36d93cd1",
        "type": "Release collection",
        "entity-type": "release",
        "name": "My Collection",
        "editor": "kanye",
        "release-list": [
            {
                "id": "0",
                "title": "The College Dropout",
                "status": "Official",
                "quality": "normal",
                "packaging": "Jewel Case",
                "text-representation": {"language": "eng", "script": "Latn"},
                "date": "2004-02-09",
                "country": "XE",
                "release-event-list": [
                    {
                        "date": "2004-02-09",
                        "area": {
                            "id": "89a675c2-3e37-3518-b83c-418bad59a85a",
                            "name": "Europe",
                            "sort-name": "Europe",
                            "iso-3166-1-code-list": ["XE"],
                        },
                    }
                ],
                "release-event-count": 1,
                "barcode": "602498617397",
            }
        ],
        "release-count": 1,
    }
}

assert create_collection(1) == collection
