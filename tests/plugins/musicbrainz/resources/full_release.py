"""Musicbrainz release with all the info we normally search for."""
# flake8: noqa

import datetime

from moe.library.album import Album
from moe.library.track import Track

# as returned by `musicbrainzngs.search_releases()`
search = {
    "release-list": [
        {
            "id": "2fcfcaaa-6594-4291-b79f-2d354139e108",
            "ext:score": "100",
            "title": "My Beautiful Dark Twisted Fantasy",
            "status": "Official",
            "packaging": "Jewel Case",
            "text-representation": {"language": "eng", "script": "Latn"},
            "artist-credit": [
                {
                    "name": "Kanye West",
                    "artist": {
                        "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                        "name": "Kanye West",
                        "sort-name": "West, Kanye",
                    },
                }
            ],
            "release-group": {
                "id": "5d6e21e1-deb5-428e-bb42-c2a567f3619b",
                "type": "Album",
                "title": "My Beautiful Dark Twisted Fantasy",
                "primary-type": "Album",
            },
            "date": "2010-11-22",
            "country": "US",
            "release-event-list": [
                {
                    "date": "2010-11-22",
                    "area": {
                        "id": "489ce91b-6658-3307-9877-795b68554c98",
                        "name": "United States",
                        "sort-name": "United States",
                        "iso-3166-1-code-list": ["US"],
                    },
                }
            ],
            "barcode": "602527474465",
            "asin": "B003X2O6KW",
            "label-info-list": [
                {
                    "catalog-number": "B0014695-02",
                    "label": {
                        "id": "4cccc72a-0bd0-433a-905e-dad87871397d",
                        "name": "Roc‐A‐Fella Records",
                    },
                }
            ],
            "medium-list": [
                {
                    "format": "CD",
                    "disc-list": [],
                    "disc-count": 3,
                    "track-list": [],
                    "track-count": 13,
                }
            ],
            "medium-track-count": 13,
            "medium-count": 1,
            "tag-list": [],
            "artist-credit-phrase": "Kanye West",
        }
    ],
    "release-count": 1,
}

# as returned by `musicbrainzngs.get_release_by_id()`
release = {
    "release": {
        "id": "2fcfcaaa-6594-4291-b79f-2d354139e108",
        "title": "My Beautiful Dark Twisted Fantasy",
        "status": "Official",
        "quality": "high",
        "packaging": "Jewel Case",
        "text-representation": {"language": "eng", "script": "Latn"},
        "artist-credit": [
            {
                "artist": {
                    "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                    "type": "Person",
                    "name": "Kanye West",
                    "sort-name": "West, Kanye",
                    "alias-list": [
                        {
                            "sort-name": "K. West",
                            "type": "Search hint",
                            "alias": "K. West",
                        },
                        {"sort-name": "Kanye", "type": "Artist name", "alias": "Kanye"},
                        {
                            "sort-name": "West, Kanye Omari",
                            "type": "Legal name",
                            "alias": "Kanye Omari West",
                        },
                        {
                            "sort-name": "Kayne West",
                            "type": "Search hint",
                            "alias": "Kayne West",
                        },
                        {"sort-name": "Yeezy", "type": "Artist name", "alias": "Yeezy"},
                        {
                            "locale": "ja",
                            "sort-name": "カニエ・ウェスト",
                            "type": "Artist name",
                            "primary": "primary",
                            "alias": "カニエ・ウェスト",
                        },
                    ],
                    "alias-count": 6,
                }
            }
        ],
        "release-group": {
            "id": "5d6e21e1-deb5-428e-bb42-c2a567f3619b",
            "type": "Album",
            "title": "My Beautiful Dark Twisted Fantasy",
            "first-release-date": "2010-11-22",
            "primary-type": "Album",
            "artist-credit": [
                {
                    "artist": {
                        "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                        "type": "Person",
                        "name": "Kanye West",
                        "sort-name": "West, Kanye",
                        "alias-list": [
                            {
                                "sort-name": "K. West",
                                "type": "Search hint",
                                "alias": "K. West",
                            },
                            {
                                "sort-name": "Kanye",
                                "type": "Artist name",
                                "alias": "Kanye",
                            },
                            {
                                "sort-name": "West, Kanye Omari",
                                "type": "Legal name",
                                "alias": "Kanye Omari West",
                            },
                            {
                                "sort-name": "Kayne West",
                                "type": "Search hint",
                                "alias": "Kayne West",
                            },
                            {
                                "sort-name": "Yeezy",
                                "type": "Artist name",
                                "alias": "Yeezy",
                            },
                            {
                                "locale": "ja",
                                "sort-name": "カニエ・ウェスト",
                                "type": "Artist name",
                                "primary": "primary",
                                "alias": "カニエ・ウェスト",
                            },
                        ],
                        "alias-count": 6,
                    }
                }
            ],
            "artist-credit-phrase": "Kanye West",
        },
        "date": "2010-11-22",
        "country": "US",
        "release-event-list": [
            {
                "date": "2010-11-22",
                "area": {
                    "id": "489ce91b-6658-3307-9877-795b68554c98",
                    "name": "United States",
                    "sort-name": "United States",
                    "iso-3166-1-code-list": ["US"],
                },
            }
        ],
        "release-event-count": 1,
        "barcode": "602527474465",
        "asin": "B003X2O6KW",
        "cover-art-archive": {
            "artwork": "true",
            "count": "4",
            "front": "true",
            "back": "true",
        },
        "label-info-list": [
            {
                "catalog-number": "B0014695-02",
                "label": {
                    "id": "4cccc72a-0bd0-433a-905e-dad87871397d",
                    "type": "Original Production",
                    "name": "Roc‐A‐Fella Records",
                    "sort-name": "Roc‐A‐Fella Records",
                },
            }
        ],
        "label-info-count": 1,
        "medium-list": [
            {
                "position": "1",
                "format": "CD",
                "track-list": [
                    {
                        "id": "219e6b01-c962-355c-8a87-5d4ab3fc13bc",
                        "position": "1",
                        "number": "1",
                        "length": "282866",
                        "recording": {
                            "id": "885ccb38-4057-4d1a-8fb0-52804f79d653",
                            "title": "Dark Fantasy",
                            "length": "280786",
                            "disambiguation": "explicit",
                            "artist-credit": [
                                {
                                    "artist": {
                                        "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                        "type": "Person",
                                        "name": "Kanye West",
                                        "sort-name": "West, Kanye",
                                        "alias-list": [
                                            {
                                                "sort-name": "K. West",
                                                "type": "Search hint",
                                                "alias": "K. West",
                                            },
                                            {
                                                "sort-name": "Kanye",
                                                "type": "Artist name",
                                                "alias": "Kanye",
                                            },
                                            {
                                                "sort-name": "West, Kanye Omari",
                                                "type": "Legal name",
                                                "alias": "Kanye Omari West",
                                            },
                                            {
                                                "sort-name": "Kayne West",
                                                "type": "Search hint",
                                                "alias": "Kayne West",
                                            },
                                            {
                                                "sort-name": "Yeezy",
                                                "type": "Artist name",
                                                "alias": "Yeezy",
                                            },
                                            {
                                                "locale": "ja",
                                                "sort-name": "カニエ・ウェスト",
                                                "type": "Artist name",
                                                "primary": "primary",
                                                "alias": "カニエ・ウェスト",
                                            },
                                        ],
                                        "alias-count": 6,
                                    }
                                }
                            ],
                            "artist-relation-list": [
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["cello", "keyboard"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0db03a60-1142-4b25-ab1b-72027d0dc357",
                                            "attribute": "cello",
                                        },
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        },
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "0fc745df-eb53-4035-94e5-3c407f9f3062",
                                    "direction": "backward",
                                    "attribute-list": ["cello"],
                                    "artist": {
                                        "id": "0fc745df-eb53-4035-94e5-3c407f9f3062",
                                        "type": "Person",
                                        "name": "Chris Chorney",
                                        "sort-name": "Chorney, Chris",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0db03a60-1142-4b25-ab1b-72027d0dc357",
                                            "attribute": "cello",
                                        }
                                    ],
                                    "target-credit": "Chris “Hitchcock” Chorney",
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["cello", "piano"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0db03a60-1142-4b25-ab1b-72027d0dc357",
                                            "attribute": "cello",
                                        },
                                        {
                                            "type-id": "b3eac5f9-7859-4416-ac39-7154e2e8d348",
                                            "attribute": "piano",
                                        },
                                    ],
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "90b8de7b-70eb-4b0c-bf4f-a9addd0fd197",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "90b8de7b-70eb-4b0c-bf4f-a9addd0fd197",
                                        "type": "Person",
                                        "name": "Andrew Dawson",
                                        "sort-name": "Dawson, Andrew",
                                        "disambiguation": "US mix engineer",
                                    },
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "fe5a5f52-e6fa-455f-8c37-a17ed80e08d8",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "fe5a5f52-e6fa-455f-8c37-a17ed80e08d8",
                                        "type": "Person",
                                        "name": "Gaylord Holomalia",
                                        "sort-name": "Holomalia, Gaylord",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "8c4196b1-7053-4b16-921a-f22b2898ed44",
                                            "attribute": "assistant",
                                        }
                                    ],
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "5750f133-b4d9-4715-bb85-4ba419ab41cb",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "5750f133-b4d9-4715-bb85-4ba419ab41cb",
                                        "type": "Person",
                                        "name": "Phil Joly",
                                        "sort-name": "Joly, Phil",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "8c4196b1-7053-4b16-921a-f22b2898ed44",
                                            "attribute": "assistant",
                                        }
                                    ],
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "d22e2371-b891-42ae-a355-5e82d2d718e4",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "d22e2371-b891-42ae-a355-5e82d2d718e4",
                                        "type": "Person",
                                        "name": "Christian Mochizuki",
                                        "sort-name": "Mochizuki, Christian",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "8c4196b1-7053-4b16-921a-f22b2898ed44",
                                            "attribute": "assistant",
                                        }
                                    ],
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        }
                                    ],
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        }
                                    ],
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "1cd913a1-5641-4b2a-9624-a0417914e3e7",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "1cd913a1-5641-4b2a-9624-a0417914e3e7",
                                        "type": "Person",
                                        "name": "No I.D.",
                                        "sort-name": "No I.D.",
                                        "disambiguation": "producer",
                                    },
                                    "target-credit": "No ID",
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "29c28ac3-27c5-4822-8eb6-0af89a3a7240",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "29c28ac3-27c5-4822-8eb6-0af89a3a7240",
                                        "type": "Person",
                                        "name": "RZA",
                                        "sort-name": "RZA",
                                        "disambiguation": "US rapper / producer",
                                    },
                                    "target-credit": "The RZA",
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                        "type": "Person",
                                        "name": "Kanye West",
                                        "sort-name": "West, Kanye",
                                    },
                                },
                                {
                                    "type": "recording",
                                    "type-id": "a01ee869-80a8-45ef-9447-c59e91aa7926",
                                    "target": "90b8de7b-70eb-4b0c-bf4f-a9addd0fd197",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "90b8de7b-70eb-4b0c-bf4f-a9addd0fd197",
                                        "type": "Person",
                                        "name": "Andrew Dawson",
                                        "sort-name": "Dawson, Andrew",
                                        "disambiguation": "US mix engineer",
                                    },
                                },
                                {
                                    "type": "recording",
                                    "type-id": "a01ee869-80a8-45ef-9447-c59e91aa7926",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                },
                                {
                                    "type": "recording",
                                    "type-id": "a01ee869-80a8-45ef-9447-c59e91aa7926",
                                    "target": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                        "type": "Person",
                                        "name": "Anthony Kilhoffer",
                                        "sort-name": "Kilhoffer, Anthony",
                                    },
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "1036b808-f58c-4a3e-b461-a2c4492ecf1b",
                                    "direction": "backward",
                                    "attribute-list": ["background vocals"],
                                    "artist": {
                                        "id": "1036b808-f58c-4a3e-b461-a2c4492ecf1b",
                                        "type": "Person",
                                        "name": "Nicki Minaj",
                                        "sort-name": "Minaj, Nicki",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "75052401-7340-4e5b-a71d-ea024a128849",
                                            "attribute": "background vocals",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "80ff1c00-d064-4887-ae07-81c01cbc2fdc",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "80ff1c00-d064-4887-ae07-81c01cbc2fdc",
                                        "type": "Person",
                                        "name": "Amber Rose",
                                        "sort-name": "Rose, Amber",
                                        "disambiguation": "American model, recording artist, actress and socialite",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "c7eb03c1-f8cb-4815-afc8-46df3b253129",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "c7eb03c1-f8cb-4815-afc8-46df3b253129",
                                        "type": "Person",
                                        "name": "Teyana Taylor",
                                        "sort-name": "Taylor, Teyana",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "0f1d5b01-8784-4870-9bd6-fa43178b9441",
                                    "direction": "backward",
                                    "attribute-list": ["background vocals"],
                                    "artist": {
                                        "id": "0f1d5b01-8784-4870-9bd6-fa43178b9441",
                                        "type": "Person",
                                        "name": "Justin Vernon",
                                        "sort-name": "Vernon, Justin",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "75052401-7340-4e5b-a71d-ea024a128849",
                                            "attribute": "background vocals",
                                        }
                                    ],
                                },
                            ],
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "e645d015-7561-3768-b107-128f68d22da0",
                                    "direction": "forward",
                                    "work": {
                                        "id": "e645d015-7561-3768-b107-128f68d22da0",
                                        "title": "Dark Fantasy",
                                        "iswc": "T-910.551.996-8",
                                        "iswc-list": ["T-910.551.996-8"],
                                        "artist-relation-list": [
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "24202038-7b02-4444-96c2-cf2fc7b81308",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "24202038-7b02-4444-96c2-cf2fc7b81308",
                                                    "type": "Person",
                                                    "name": "Jon Anderson",
                                                    "sort-name": "Anderson, Jon",
                                                    "disambiguation": "Yes/Jon & Vangelis",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                                    "type": "Person",
                                                    "name": "Jeff Bhasker",
                                                    "sort-name": "Bhasker, Jeff",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                                    "type": "Person",
                                                    "name": "Mike Dean",
                                                    "sort-name": "Dean, Mike",
                                                    "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "1cd913a1-5641-4b2a-9624-a0417914e3e7",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "1cd913a1-5641-4b2a-9624-a0417914e3e7",
                                                    "type": "Person",
                                                    "name": "No I.D.",
                                                    "sort-name": "No I.D.",
                                                    "disambiguation": "producer",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "a1684a49-feaa-4150-b758-d9412fc59f12",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "a1684a49-feaa-4150-b758-d9412fc59f12",
                                                    "type": "Person",
                                                    "name": "Mike Oldfield",
                                                    "sort-name": "Oldfield, Mike",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "29c28ac3-27c5-4822-8eb6-0af89a3a7240",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "29c28ac3-27c5-4822-8eb6-0af89a3a7240",
                                                    "type": "Person",
                                                    "name": "RZA",
                                                    "sort-name": "RZA",
                                                    "disambiguation": "US rapper / producer",
                                                },
                                                "target-credit": "Robert Diggs",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                                    "type": "Person",
                                                    "name": "Kanye West",
                                                    "sort-name": "West, Kanye",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "64b15912-5f96-45cb-9514-3943d1b0f220",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "64b15912-5f96-45cb-9514-3943d1b0f220",
                                                    "type": "Person",
                                                    "name": "Malik Yusef",
                                                    "sort-name": "Yusef, Malik",
                                                },
                                                "target-credit": "Malik Jones",
                                            },
                                        ],
                                    },
                                }
                            ],
                            "artist-credit-phrase": "Kanye West",
                        },
                        "artist-credit": [
                            {
                                "artist": {
                                    "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                    "type": "Person",
                                    "name": "Kanye West",
                                    "sort-name": "West, Kanye",
                                    "alias-list": [
                                        {
                                            "sort-name": "K. West",
                                            "type": "Search hint",
                                            "alias": "K. West",
                                        },
                                        {
                                            "sort-name": "Kanye",
                                            "type": "Artist name",
                                            "alias": "Kanye",
                                        },
                                        {
                                            "sort-name": "West, Kanye Omari",
                                            "type": "Legal name",
                                            "alias": "Kanye Omari West",
                                        },
                                        {
                                            "sort-name": "Kayne West",
                                            "type": "Search hint",
                                            "alias": "Kayne West",
                                        },
                                        {
                                            "sort-name": "Yeezy",
                                            "type": "Artist name",
                                            "alias": "Yeezy",
                                        },
                                        {
                                            "locale": "ja",
                                            "sort-name": "カニエ・ウェスト",
                                            "type": "Artist name",
                                            "primary": "primary",
                                            "alias": "カニエ・ウェスト",
                                        },
                                    ],
                                    "alias-count": 6,
                                }
                            }
                        ],
                        "artist-credit-phrase": "Kanye West",
                        "track_or_recording_length": "282866",
                    },
                    {
                        "id": "d4cbaf03-b40a-352d-9461-eadbc5986fc0",
                        "position": "2",
                        "number": "2",
                        "length": "359733",
                        "recording": {
                            "id": "b3c6aa0a-6960-4db6-bf27-ed50de88309c",
                            "title": "Gorgeous",
                            "length": "357653",
                            "disambiguation": "explicit",
                            "artist-credit": [
                                {
                                    "artist": {
                                        "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                        "type": "Person",
                                        "name": "Kanye West",
                                        "sort-name": "West, Kanye",
                                        "alias-list": [
                                            {
                                                "sort-name": "K. West",
                                                "type": "Search hint",
                                                "alias": "K. West",
                                            },
                                            {
                                                "sort-name": "Kanye",
                                                "type": "Artist name",
                                                "alias": "Kanye",
                                            },
                                            {
                                                "sort-name": "West, Kanye Omari",
                                                "type": "Legal name",
                                                "alias": "Kanye Omari West",
                                            },
                                            {
                                                "sort-name": "Kayne West",
                                                "type": "Search hint",
                                                "alias": "Kayne West",
                                            },
                                            {
                                                "sort-name": "Yeezy",
                                                "type": "Artist name",
                                                "alias": "Yeezy",
                                            },
                                            {
                                                "locale": "ja",
                                                "sort-name": "カニエ・ウェスト",
                                                "type": "Artist name",
                                                "primary": "primary",
                                                "alias": "カニエ・ウェスト",
                                            },
                                        ],
                                        "alias-count": 6,
                                    }
                                },
                                " feat. ",
                                {
                                    "artist": {
                                        "id": "e0e1db18-f7ba-4dee-95ff-7ae8cf545460",
                                        "type": "Person",
                                        "name": "Kid Cudi",
                                        "sort-name": "Kid Cudi",
                                        "alias-list": [
                                            {
                                                "sort-name": "Kid Kudi",
                                                "alias": "Kid Kudi",
                                            },
                                            {
                                                "sort-name": "S. Mescudi",
                                                "alias": "S. Mescudi",
                                            },
                                            {
                                                "sort-name": "Mescudi, Scott Ramon Seguro",
                                                "type": "Legal name",
                                                "alias": "Scott Ramon Seguro Mescudi",
                                            },
                                            {
                                                "sort-name": "キッド・カディ",
                                                "alias": "キッド・カディ",
                                            },
                                        ],
                                        "alias-count": 4,
                                    }
                                },
                                " & ",
                                {
                                    "artist": {
                                        "id": "4e954b02-fae2-4bd7-9547-e055a6ac0527",
                                        "type": "Person",
                                        "name": "Raekwon",
                                        "sort-name": "Raekwon",
                                        "disambiguation": "Corey Woods",
                                        "alias-list": [
                                            {
                                                "sort-name": "Chef Raekwon",
                                                "alias": "Chef Raekwon",
                                            },
                                            {
                                                "sort-name": "Woods, Corey",
                                                "type": "Legal name",
                                                "alias": "Corey Woods",
                                            },
                                            {
                                                "sort-name": "Lex Diamonds",
                                                "type": "Artist name",
                                                "alias": "Lex Diamonds",
                                            },
                                            {
                                                "sort-name": "RAEK WON",
                                                "alias": "RAEK WON",
                                            },
                                            {
                                                "sort-name": "Reakwon",
                                                "alias": "Reakwon",
                                            },
                                        ],
                                        "alias-count": 5,
                                    }
                                },
                            ],
                            "artist-relation-list": [
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "0fc745df-eb53-4035-94e5-3c407f9f3062",
                                    "direction": "backward",
                                    "attribute-list": ["cello"],
                                    "artist": {
                                        "id": "0fc745df-eb53-4035-94e5-3c407f9f3062",
                                        "type": "Person",
                                        "name": "Chris Chorney",
                                        "sort-name": "Chorney, Chris",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0db03a60-1142-4b25-ab1b-72027d0dc357",
                                            "attribute": "cello",
                                        }
                                    ],
                                    "target-credit": "Chris “Hitchcock” Chorney",
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["guitar", "solo"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "63021302-86cd-4aee-80df-2270d54f4978",
                                            "attribute": "guitar",
                                        },
                                        {
                                            "type-id": "63daa0d3-9b63-4434-acff-4977c07808ca",
                                            "attribute": "solo",
                                        },
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                    "direction": "backward",
                                    "attribute-list": [
                                        "bass guitar",
                                        "guitar",
                                        "organ",
                                    ],
                                    "artist": {
                                        "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                        "type": "Person",
                                        "name": "Ken Lewis",
                                        "sort-name": "Lewis, Ken",
                                        "disambiguation": "recording engineer and mixer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "17f9f065-2312-4a24-8309-6f6dd63e2e33",
                                            "attribute": "bass guitar",
                                        },
                                        {
                                            "type-id": "63021302-86cd-4aee-80df-2270d54f4978",
                                            "attribute": "guitar",
                                        },
                                        {
                                            "type-id": "55a37f4f-39a4-45a7-851d-586569985519",
                                            "attribute": "organ",
                                        },
                                    ],
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "49c19ad1-eca8-4a0d-99b3-645df7c83dc4",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "49c19ad1-eca8-4a0d-99b3-645df7c83dc4",
                                        "type": "Person",
                                        "name": "Pete Bischoff",
                                        "sort-name": "Bischoff, Pete",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "8c4196b1-7053-4b16-921a-f22b2898ed44",
                                            "attribute": "assistant",
                                        }
                                    ],
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "5750f133-b4d9-4715-bb85-4ba419ab41cb",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "5750f133-b4d9-4715-bb85-4ba419ab41cb",
                                        "type": "Person",
                                        "name": "Phil Joly",
                                        "sort-name": "Joly, Phil",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "8c4196b1-7053-4b16-921a-f22b2898ed44",
                                            "attribute": "assistant",
                                        }
                                    ],
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                        "type": "Person",
                                        "name": "Anthony Kilhoffer",
                                        "sort-name": "Kilhoffer, Anthony",
                                    },
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "d22e2371-b891-42ae-a355-5e82d2d718e4",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "d22e2371-b891-42ae-a355-5e82d2d718e4",
                                        "type": "Person",
                                        "name": "Christian Mochizuki",
                                        "sort-name": "Mochizuki, Christian",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "8c4196b1-7053-4b16-921a-f22b2898ed44",
                                            "attribute": "assistant",
                                        }
                                    ],
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "1cd913a1-5641-4b2a-9624-a0417914e3e7",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "1cd913a1-5641-4b2a-9624-a0417914e3e7",
                                        "type": "Person",
                                        "name": "No I.D.",
                                        "sort-name": "No I.D.",
                                        "disambiguation": "producer",
                                    },
                                    "target-credit": "No ID",
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                        "type": "Person",
                                        "name": "Kanye West",
                                        "sort-name": "West, Kanye",
                                    },
                                },
                                {
                                    "type": "programming",
                                    "type-id": "36c50022-44e0-488d-994b-33f11d20301e",
                                    "target": "a5c6f645-c4db-4cd3-9129-a3ebe9bbabea",
                                    "direction": "backward",
                                    "attribute-list": ["drum machine", "keyboard"],
                                    "artist": {
                                        "id": "a5c6f645-c4db-4cd3-9129-a3ebe9bbabea",
                                        "type": "Person",
                                        "name": "Brent Kolatalo",
                                        "sort-name": "Kolatalo, Brent",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ce0eed13-58d8-4744-8ad0-b7d6182a2d0f",
                                            "attribute": "drum machine",
                                        },
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        },
                                    ],
                                },
                                {
                                    "type": "recording",
                                    "type-id": "a01ee869-80a8-45ef-9447-c59e91aa7926",
                                    "target": "90b8de7b-70eb-4b0c-bf4f-a9addd0fd197",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "90b8de7b-70eb-4b0c-bf4f-a9addd0fd197",
                                        "type": "Person",
                                        "name": "Andrew Dawson",
                                        "sort-name": "Dawson, Andrew",
                                        "disambiguation": "US mix engineer",
                                    },
                                },
                                {
                                    "type": "recording",
                                    "type-id": "a01ee869-80a8-45ef-9447-c59e91aa7926",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                },
                                {
                                    "type": "recording",
                                    "type-id": "a01ee869-80a8-45ef-9447-c59e91aa7926",
                                    "target": "2dad5809-0d9b-40cf-85cf-2f8828ffaaf0",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "2dad5809-0d9b-40cf-85cf-2f8828ffaaf0",
                                        "type": "Person",
                                        "name": "Noah Goldstein",
                                        "sort-name": "Goldstein, Noah",
                                    },
                                },
                                {
                                    "type": "recording",
                                    "type-id": "a01ee869-80a8-45ef-9447-c59e91aa7926",
                                    "target": "5750f133-b4d9-4715-bb85-4ba419ab41cb",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "5750f133-b4d9-4715-bb85-4ba419ab41cb",
                                        "type": "Person",
                                        "name": "Phil Joly",
                                        "sort-name": "Joly, Phil",
                                    },
                                },
                                {
                                    "type": "recording",
                                    "type-id": "a01ee869-80a8-45ef-9447-c59e91aa7926",
                                    "target": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                        "type": "Person",
                                        "name": "Anthony Kilhoffer",
                                        "sort-name": "Kilhoffer, Anthony",
                                    },
                                },
                                {
                                    "type": "recording",
                                    "type-id": "a01ee869-80a8-45ef-9447-c59e91aa7926",
                                    "target": "d22e2371-b891-42ae-a355-5e82d2d718e4",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "d22e2371-b891-42ae-a355-5e82d2d718e4",
                                        "type": "Person",
                                        "name": "Christian Mochizuki",
                                        "sort-name": "Mochizuki, Christian",
                                    },
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "e0e1db18-f7ba-4dee-95ff-7ae8cf545460",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "e0e1db18-f7ba-4dee-95ff-7ae8cf545460",
                                        "type": "Person",
                                        "name": "Kid Cudi",
                                        "sort-name": "Kid Cudi",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "b3045913-62ac-433e-9211-ac683cdf6b5c",
                                            "attribute": "guest",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "4e954b02-fae2-4bd7-9547-e055a6ac0527",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "4e954b02-fae2-4bd7-9547-e055a6ac0527",
                                        "type": "Person",
                                        "name": "Raekwon",
                                        "sort-name": "Raekwon",
                                        "disambiguation": "Corey Woods",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "b3045913-62ac-433e-9211-ac683cdf6b5c",
                                            "attribute": "guest",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "a42fdc0b-09bc-4a6d-8ae6-db454bf0803a",
                                    "direction": "backward",
                                    "attribute-list": ["background vocals"],
                                    "artist": {
                                        "id": "a42fdc0b-09bc-4a6d-8ae6-db454bf0803a",
                                        "type": "Person",
                                        "name": "Tony Williams",
                                        "sort-name": "Williams, Tony",
                                        "disambiguation": "soul/R&B singer/writer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "75052401-7340-4e5b-a71d-ea024a128849",
                                            "attribute": "background vocals",
                                        }
                                    ],
                                },
                            ],
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "579b12e3-44d6-37bb-8e2a-64f04d9d949b",
                                    "direction": "forward",
                                    "work": {
                                        "id": "579b12e3-44d6-37bb-8e2a-64f04d9d949b",
                                        "type": "Song",
                                        "title": "Gorgeous",
                                        "language": "eng",
                                        "iswc": "T-915.028.039-0",
                                        "iswc-list": ["T-915.028.039-0"],
                                        "artist-relation-list": [
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "2b6f3780-6fb6-42c2-95bb-5e080772e38c",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "2b6f3780-6fb6-42c2-95bb-5e080772e38c",
                                                    "type": "Person",
                                                    "name": "Gene Clark",
                                                    "sort-name": "Clark, Gene",
                                                    "disambiguation": "US singer-songwriter; founder of The Byrds",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                                    "type": "Person",
                                                    "name": "Mike Dean",
                                                    "sort-name": "Dean, Mike",
                                                    "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "e0e1db18-f7ba-4dee-95ff-7ae8cf545460",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "e0e1db18-f7ba-4dee-95ff-7ae8cf545460",
                                                    "type": "Person",
                                                    "name": "Kid Cudi",
                                                    "sort-name": "Kid Cudi",
                                                },
                                                "target-credit": "Scott Ramon Seguro Mescudi",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "6ec7336b-a56a-4b5d-bcec-575d2b8ed4e1",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "6ec7336b-a56a-4b5d-bcec-575d2b8ed4e1",
                                                    "type": "Person",
                                                    "name": "Roger McGuinn",
                                                    "sort-name": "McGuinn, Roger",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "94dbfe2e-ca48-4e08-a5a8-e1e74136c63d",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "94dbfe2e-ca48-4e08-a5a8-e1e74136c63d",
                                                    "type": "Person",
                                                    "name": "Method Man",
                                                    "sort-name": "Method Man",
                                                    "disambiguation": "of the Wu-Tang Clan",
                                                },
                                                "target-credit": "Clifford Smith",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "1cd913a1-5641-4b2a-9624-a0417914e3e7",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "1cd913a1-5641-4b2a-9624-a0417914e3e7",
                                                    "type": "Person",
                                                    "name": "No I.D.",
                                                    "sort-name": "No I.D.",
                                                    "disambiguation": "producer",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "4e954b02-fae2-4bd7-9547-e055a6ac0527",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "4e954b02-fae2-4bd7-9547-e055a6ac0527",
                                                    "type": "Person",
                                                    "name": "Raekwon",
                                                    "sort-name": "Raekwon",
                                                    "disambiguation": "Corey Woods",
                                                },
                                                "target-credit": "Corey Woods",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                                    "type": "Person",
                                                    "name": "Kanye West",
                                                    "sort-name": "West, Kanye",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "64b15912-5f96-45cb-9514-3943d1b0f220",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "64b15912-5f96-45cb-9514-3943d1b0f220",
                                                    "type": "Person",
                                                    "name": "Malik Yusef",
                                                    "sort-name": "Yusef, Malik",
                                                },
                                                "target-credit": "Malik Jones",
                                            },
                                        ],
                                    },
                                }
                            ],
                            "artist-credit-phrase": "Kanye West feat. Kid Cudi & Raekwon",
                        },
                        "artist-credit": [
                            {
                                "artist": {
                                    "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                                    "type": "Person",
                                    "name": "Kanye West",
                                    "sort-name": "West, Kanye",
                                    "alias-list": [
                                        {
                                            "sort-name": "K. West",
                                            "type": "Search hint",
                                            "alias": "K. West",
                                        },
                                        {
                                            "sort-name": "Kanye",
                                            "type": "Artist name",
                                            "alias": "Kanye",
                                        },
                                        {
                                            "sort-name": "West, Kanye Omari",
                                            "type": "Legal name",
                                            "alias": "Kanye Omari West",
                                        },
                                        {
                                            "sort-name": "Kayne West",
                                            "type": "Search hint",
                                            "alias": "Kayne West",
                                        },
                                        {
                                            "sort-name": "Yeezy",
                                            "type": "Artist name",
                                            "alias": "Yeezy",
                                        },
                                        {
                                            "locale": "ja",
                                            "sort-name": "カニエ・ウェスト",
                                            "type": "Artist name",
                                            "primary": "primary",
                                            "alias": "カニエ・ウェスト",
                                        },
                                    ],
                                    "alias-count": 6,
                                }
                            },
                            " feat. ",
                            {
                                "artist": {
                                    "id": "e0e1db18-f7ba-4dee-95ff-7ae8cf545460",
                                    "type": "Person",
                                    "name": "Kid Cudi",
                                    "sort-name": "Kid Cudi",
                                    "alias-list": [
                                        {"sort-name": "Kid Kudi", "alias": "Kid Kudi"},
                                        {
                                            "sort-name": "S. Mescudi",
                                            "alias": "S. Mescudi",
                                        },
                                        {
                                            "sort-name": "Mescudi, Scott Ramon Seguro",
                                            "type": "Legal name",
                                            "alias": "Scott Ramon Seguro Mescudi",
                                        },
                                        {"sort-name": "キッド・カディ", "alias": "キッド・カディ"},
                                    ],
                                    "alias-count": 4,
                                }
                            },
                            " & ",
                            {
                                "artist": {
                                    "id": "4e954b02-fae2-4bd7-9547-e055a6ac0527",
                                    "type": "Person",
                                    "name": "Raekwon",
                                    "sort-name": "Raekwon",
                                    "disambiguation": "Corey Woods",
                                    "alias-list": [
                                        {
                                            "sort-name": "Chef Raekwon",
                                            "alias": "Chef Raekwon",
                                        },
                                        {
                                            "sort-name": "Woods, Corey",
                                            "type": "Legal name",
                                            "alias": "Corey Woods",
                                        },
                                        {
                                            "sort-name": "Lex Diamonds",
                                            "type": "Artist name",
                                            "alias": "Lex Diamonds",
                                        },
                                        {"sort-name": "RAEK WON", "alias": "RAEK WON"},
                                        {"sort-name": "Reakwon", "alias": "Reakwon"},
                                    ],
                                    "alias-count": 5,
                                }
                            },
                        ],
                        "artist-credit-phrase": "Kanye West feat. Kid Cudi & Raekwon",
                        "track_or_recording_length": "359733",
                    },
                ],
                "track-count": 13,
            }
        ],
        "medium-count": 1,
        "artist-relation-list": [
            {
                "type": "art direction",
                "type-id": "f3b80a09-5ebf-4ad2-9c46-3e6bce971d1b",
                "target": "d1b04ab5-94e9-4130-96f0-e59dfa66555e",
                "direction": "backward",
                "artist": {
                    "id": "d1b04ab5-94e9-4130-96f0-e59dfa66555e",
                    "type": "Person",
                    "name": "Virgil Abloh",
                    "sort-name": "Abloh, Virgil",
                },
            },
            {
                "type": "art direction",
                "type-id": "f3b80a09-5ebf-4ad2-9c46-3e6bce971d1b",
                "target": "164f0d73-1234-4e2c-8743-d77bf2191051",
                "direction": "backward",
                "artist": {
                    "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                    "type": "Person",
                    "name": "Kanye West",
                    "sort-name": "West, Kanye",
                },
            },
            {
                "type": "graphic design",
                "type-id": "cf43b79e-3299-4b0c-9244-59ea06337107",
                "target": "932727fe-954b-43f5-9b8a-8c9c5ed9eac1",
                "direction": "backward",
                "artist": {
                    "id": "932727fe-954b-43f5-9b8a-8c9c5ed9eac1",
                    "type": "Group",
                    "name": "M/M (Paris)",
                    "sort-name": "M/M (Paris)",
                    "disambiguation": "art, design duo",
                },
            },
            {
                "type": "illustration",
                "type-id": "a6029157-d96b-4dc3-9f73-f99f76423d11",
                "target": "42687455-17d1-42bb-9e7b-cb6cb3103865",
                "direction": "backward",
                "artist": {
                    "id": "42687455-17d1-42bb-9e7b-cb6cb3103865",
                    "type": "Person",
                    "name": "George Condo",
                    "sort-name": "Condo, George",
                },
            },
            {
                "type": "illustration",
                "type-id": "a6029157-d96b-4dc3-9f73-f99f76423d11",
                "target": "932727fe-954b-43f5-9b8a-8c9c5ed9eac1",
                "direction": "backward",
                "artist": {
                    "id": "932727fe-954b-43f5-9b8a-8c9c5ed9eac1",
                    "type": "Group",
                    "name": "M/M (Paris)",
                    "sort-name": "M/M (Paris)",
                    "disambiguation": "art, design duo",
                },
            },
            {
                "type": "mastering",
                "type-id": "84453d28-c3e8-4864-9aae-25aa968bcf9e",
                "target": "0540f222-dfed-4b31-8076-bc876b47e750",
                "direction": "backward",
                "artist": {
                    "id": "0540f222-dfed-4b31-8076-bc876b47e750",
                    "type": "Person",
                    "name": "Vlado Meller",
                    "sort-name": "Meller, Vlado",
                },
            },
            {
                "type": "photography",
                "type-id": "0b58dc9b-9c49-4b19-bb58-9c06d41c8fbf",
                "target": "4e5e1678-cfda-422c-a59e-c1da004ef720",
                "direction": "backward",
                "artist": {
                    "id": "4e5e1678-cfda-422c-a59e-c1da004ef720",
                    "type": "Person",
                    "name": "Fabien Montique",
                    "sort-name": "Montique, Fabien",
                },
            },
            {
                "type": "producer",
                "type-id": "8bf377ba-8d71-4ecc-97f2-7bb2d8a2a75f",
                "target": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                "direction": "backward",
                "attribute-list": ["executive"],
                "artist": {
                    "id": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                    "type": "Person",
                    "name": "JAY‐Z",
                    "sort-name": "JAY‐Z",
                    "disambiguation": "US rapper",
                },
                "attributes": [
                    {
                        "type-id": "e0039285-6667-4f94-80d6-aa6520c6d359",
                        "attribute": "executive",
                    }
                ],
                "target-credit": "Shawn Carter",
            },
            {
                "type": "producer",
                "type-id": "8bf377ba-8d71-4ecc-97f2-7bb2d8a2a75f",
                "target": "c3c993b2-ac96-4b3b-92ce-4716fb70d25c",
                "direction": "backward",
                "attribute-list": ["executive"],
                "artist": {
                    "id": "c3c993b2-ac96-4b3b-92ce-4716fb70d25c",
                    "type": "Person",
                    "name": "Kyambo “Hip Hop” Joshua",
                    "sort-name": "Joshua, Kyambo “Hip Hop”",
                },
                "attributes": [
                    {
                        "type-id": "e0039285-6667-4f94-80d6-aa6520c6d359",
                        "attribute": "executive",
                    }
                ],
            },
            {
                "type": "producer",
                "type-id": "8bf377ba-8d71-4ecc-97f2-7bb2d8a2a75f",
                "target": "67467a70-3754-44e0-9c3c-151fd210f4f9",
                "direction": "backward",
                "attribute-list": ["executive"],
                "artist": {
                    "id": "67467a70-3754-44e0-9c3c-151fd210f4f9",
                    "type": "Person",
                    "name": "L.A. Reid",
                    "sort-name": "Reid, L.A.",
                },
                "attributes": [
                    {
                        "type-id": "e0039285-6667-4f94-80d6-aa6520c6d359",
                        "attribute": "executive",
                    }
                ],
                "target-credit": "Antonio M. Reid",
            },
            {
                "type": "producer",
                "type-id": "8bf377ba-8d71-4ecc-97f2-7bb2d8a2a75f",
                "target": "2c954235-3c70-48b9-b3cf-889cb4f41276",
                "direction": "backward",
                "attribute-list": ["executive"],
                "artist": {
                    "id": "2c954235-3c70-48b9-b3cf-889cb4f41276",
                    "type": "Person",
                    "name": "Gee Roberson",
                    "sort-name": "Roberson, Gee",
                },
                "attributes": [
                    {
                        "type-id": "e0039285-6667-4f94-80d6-aa6520c6d359",
                        "attribute": "executive",
                    }
                ],
            },
            {
                "type": "producer",
                "type-id": "8bf377ba-8d71-4ecc-97f2-7bb2d8a2a75f",
                "target": "164f0d73-1234-4e2c-8743-d77bf2191051",
                "direction": "backward",
                "attribute-list": ["executive"],
                "artist": {
                    "id": "164f0d73-1234-4e2c-8743-d77bf2191051",
                    "type": "Person",
                    "name": "Kanye West",
                    "sort-name": "West, Kanye",
                },
                "attributes": [
                    {
                        "type-id": "e0039285-6667-4f94-80d6-aa6520c6d359",
                        "attribute": "executive",
                    }
                ],
            },
        ],
        "artist-credit-phrase": "Kanye West",
    }
}

# Album representation
album = Album(
    artist="Kanye West",
    title="My Beautiful Dark Twisted Fantasy",
    date=datetime.date(2010, 11, 22),
    path=None,  # type: ignore
    mb_album_id="2fcfcaaa-6594-4291-b79f-2d354139e108",
)
track1 = Track(
    album=album,
    track_num=1,
    path=None,  # type: ignore
    artist="Kanye West",
    title="Dark Fantasy",
    mb_track_id="219e6b01-c962-355c-8a87-5d4ab3fc13bc",
    disc=1,
)
track2 = Track(
    album=album,
    track_num=2,
    path=None,  # type: ignore
    artist="Kanye West feat. Kid Cudi & Raekwon",
    title="Gorgeous",
    mb_track_id="d4cbaf03-b40a-352d-9461-eadbc5986fc0",
    disc=1,
)
