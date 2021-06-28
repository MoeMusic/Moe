"""Musicbrainz release with all the info we normally search for."""
# flake8: noqa

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
                    {
                        "id": "907f2c88-4a97-318a-a199-263b77d90b57",
                        "position": "3",
                        "number": "3",
                        "length": "294173",
                        "recording": {
                            "id": "f42e84ef-f23e-4b8c-b3a1-8f407be68ea5",
                            "title": "Power",
                            "length": "292093",
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
                                    "type": "engineer",
                                    "type-id": "5dcc52af-7064-4051-8d62-7d80f4c3c907",
                                    "target": "a5c6f645-c4db-4cd3-9129-a3ebe9bbabea",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "a5c6f645-c4db-4cd3-9129-a3ebe9bbabea",
                                        "type": "Person",
                                        "name": "Brent Kolatalo",
                                        "sort-name": "Kolatalo, Brent",
                                    },
                                },
                                {
                                    "type": "engineer",
                                    "type-id": "5dcc52af-7064-4051-8d62-7d80f4c3c907",
                                    "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                        "type": "Person",
                                        "name": "Ken Lewis",
                                        "sort-name": "Lewis, Ken",
                                        "disambiguation": "recording engineer and mixer",
                                    },
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "94f632a0-2214-4fc2-8c60-8151f4989a12",
                                    "direction": "backward",
                                    "attribute-list": ["handclaps"],
                                    "artist": {
                                        "id": "94f632a0-2214-4fc2-8c60-8151f4989a12",
                                        "type": "Person",
                                        "name": "Ian Allen",
                                        "sort-name": "Allen, Ian",
                                        "disambiguation": "Negativland",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "b8d84cec-ef49-47ec-b754-c1e48146e255",
                                            "attribute": "handclaps",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["keyboard"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        }
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
                                    "target": "0815491f-0cac-4099-a117-18d42d6cd25c",
                                    "direction": "backward",
                                    "attribute-list": ["handclaps"],
                                    "artist": {
                                        "id": "0815491f-0cac-4099-a117-18d42d6cd25c",
                                        "type": "Person",
                                        "name": "Wilson Christopher",
                                        "sort-name": "Christopher, Wilson",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "b8d84cec-ef49-47ec-b754-c1e48146e255",
                                            "attribute": "handclaps",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["bass", "guitar", "keyboard"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "6505f98c-f698-4406-8bf4-8ca43d05c36f",
                                            "attribute": "bass",
                                        },
                                        {
                                            "type-id": "63021302-86cd-4aee-80df-2270d54f4978",
                                            "attribute": "guitar",
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
                                    "target": "3b9b9504-b604-4c97-950b-a39fa6396787",
                                    "direction": "backward",
                                    "attribute-list": ["handclaps"],
                                    "artist": {
                                        "id": "3b9b9504-b604-4c97-950b-a39fa6396787",
                                        "type": "Person",
                                        "name": "Uri Djemal",
                                        "sort-name": "Djemal, Uri",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "b8d84cec-ef49-47ec-b754-c1e48146e255",
                                            "attribute": "handclaps",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "0a8cfc83-0060-481d-a8af-7255ff5b195d",
                                    "direction": "backward",
                                    "attribute-list": ["handclaps"],
                                    "artist": {
                                        "id": "0a8cfc83-0060-481d-a8af-7255ff5b195d",
                                        "type": "Person",
                                        "name": "Chris Soper",
                                        "sort-name": "Soper, Chris",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "b8d84cec-ef49-47ec-b754-c1e48146e255",
                                            "attribute": "handclaps",
                                        }
                                    ],
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "190ae10e-44c9-47c2-9d05-09520fcfba41",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "190ae10e-44c9-47c2-9d05-09520fcfba41",
                                        "type": "Person",
                                        "name": "Erik Madrid",
                                        "sort-name": "Madrid, Erik",
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
                                    "target": "54c1f74e-2cd7-481d-9d31-7808fc2dbf05",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "54c1f74e-2cd7-481d-9d31-7808fc2dbf05",
                                        "type": "Person",
                                        "name": "Manny Marroquin",
                                        "sort-name": "Marroquin, Manny",
                                    },
                                },
                                {
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "d6982f2c-4cb1-4ec7-b341-12b1aa08c1c1",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "d6982f2c-4cb1-4ec7-b341-12b1aa08c1c1",
                                        "type": "Person",
                                        "name": "Christian Plata",
                                        "sort-name": "Plata, Christian",
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
                                    "target": "90b8de7b-70eb-4b0c-bf4f-a9addd0fd197",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "90b8de7b-70eb-4b0c-bf4f-a9addd0fd197",
                                        "type": "Person",
                                        "name": "Andrew Dawson",
                                        "sort-name": "Dawson, Andrew",
                                        "disambiguation": "US mix engineer",
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
                                    "target": "21f45372-d089-4766-9343-9dafc079f83d",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "21f45372-d089-4766-9343-9dafc079f83d",
                                        "type": "Person",
                                        "name": "Symbolyc One",
                                        "sort-name": "Symbolyc One",
                                    },
                                    "target-credit": "S1",
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
                                    "target": "808c1fbb-ccfb-4b15-a541-72bec155e696",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "808c1fbb-ccfb-4b15-a541-72bec155e696",
                                        "type": "Person",
                                        "name": "Dwele",
                                        "sort-name": "Dwele",
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
                                    "target": "9fa19223-ec32-4da2-b1a2-79ea8afeb17a",
                                    "direction": "backward",
                                    "attribute-list": ["other vocals"],
                                    "artist": {
                                        "id": "9fa19223-ec32-4da2-b1a2-79ea8afeb17a",
                                        "type": "Person",
                                        "name": "Alvin Fields",
                                        "sort-name": "Fields, Alvin",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "c359be96-620a-435c-bd25-2eb0ce81a22e",
                                            "attribute": "other vocals",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                    "direction": "backward",
                                    "attribute-list": ["other vocals"],
                                    "artist": {
                                        "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                        "type": "Person",
                                        "name": "Ken Lewis",
                                        "sort-name": "Lewis, Ken",
                                        "disambiguation": "recording engineer and mixer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "c359be96-620a-435c-bd25-2eb0ce81a22e",
                                            "attribute": "other vocals",
                                        }
                                    ],
                                },
                            ],
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "57eff194-93a2-324b-92b1-2cb1570e55bf",
                                    "direction": "forward",
                                    "work": {
                                        "id": "57eff194-93a2-324b-92b1-2cb1570e55bf",
                                        "title": "Power",
                                        "iswc": "T-906.142.685-5",
                                        "iswc-list": ["T-906.142.685-5"],
                                        "artist-relation-list": [
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "4ed7e5da-c622-41e4-a849-062979b5698f",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "4ed7e5da-c622-41e4-a849-062979b5698f",
                                                    "type": "Person",
                                                    "name": "Boris Bergman",
                                                    "sort-name": "Bergman, Boris",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "753deb54-5a00-4552-bab4-c63a98eec171",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "753deb54-5a00-4552-bab4-c63a98eec171",
                                                    "type": "Person",
                                                    "name": "François Bernheim",
                                                    "sort-name": "Bernheim, François",
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
                                                "target": "08bd2f0f-4459-4192-9b48-7c5e6062fdf3",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "08bd2f0f-4459-4192-9b48-7c5e6062fdf3",
                                                    "type": "Person",
                                                    "name": "Andwele Gardner",
                                                    "sort-name": "Gardner, Andwele",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "e3902857-ae51-4752-967c-0bc722625aa9",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "e3902857-ae51-4752-967c-0bc722625aa9",
                                                    "type": "Person",
                                                    "name": "Jean-Pierre Lang",
                                                    "sort-name": "Lang, Jean-Pierre",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                                    "type": "Person",
                                                    "name": "Ken Lewis",
                                                    "sort-name": "Lewis, Ken",
                                                    "disambiguation": "recording engineer and mixer",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "21f45372-d089-4766-9343-9dafc079f83d",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "21f45372-d089-4766-9343-9dafc079f83d",
                                                    "type": "Person",
                                                    "name": "Symbolyc One",
                                                    "sort-name": "Symbolyc One",
                                                },
                                                "target-credit": "Larry D. Griffin Jr.",
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
                                        ],
                                        "work-relation-list": [
                                            {
                                                "type": "other version",
                                                "type-id": "7440b539-19ab-4243-8c03-4f5942ca2218",
                                                "target": "59557898-6e85-4292-a815-c878691bf4aa",
                                                "direction": "forward",
                                                "attribute-list": ["parody"],
                                                "work": {
                                                    "id": "59557898-6e85-4292-a815-c878691bf4aa",
                                                    "type": "Song",
                                                    "title": "Ponies",
                                                },
                                                "attributes": [
                                                    {
                                                        "type-id": "d73de9d3-934b-419c-8c83-2e48a5773b14",
                                                        "attribute": "parody",
                                                    }
                                                ],
                                            }
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
                        "track_or_recording_length": "294173",
                    },
                    {
                        "id": "1d93f379-4891-30b1-83d3-a6e97b339917",
                        "position": "4",
                        "number": "4",
                        "length": "64346",
                        "recording": {
                            "id": "48299852-b44c-46a3-b635-1a34f2fe61e5",
                            "title": "All of the Lights (interlude)",
                            "length": "62253",
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
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "529b9c3e-1fcd-3cfb-973e-dee048e775ea",
                                    "direction": "forward",
                                    "work": {
                                        "id": "529b9c3e-1fcd-3cfb-973e-dee048e775ea",
                                        "title": "All of the Lights (interlude)",
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
                        "track_or_recording_length": "64346",
                    },
                    {
                        "id": "b207c458-a93f-3251-8edf-a150688ad9c2",
                        "position": "5",
                        "number": "5",
                        "length": "301853",
                        "recording": {
                            "id": "a4c4457b-577e-4fac-b820-713bb91dbb6c",
                            "title": "All of the Lights",
                            "length": "299786",
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
                                    "type": "conductor",
                                    "type-id": "234670ce-5f22-4fd0-921b-ef1662695c5d",
                                    "target": "7481f4a7-2a2a-4fa7-8a53-128e247e493d",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "7481f4a7-2a2a-4fa7-8a53-128e247e493d",
                                        "type": "Person",
                                        "name": "Rosie Danvers",
                                        "sort-name": "Danvers, Rosie",
                                    },
                                },
                                {
                                    "type": "engineer",
                                    "type-id": "5dcc52af-7064-4051-8d62-7d80f4c3c907",
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
                                    "type": "engineer",
                                    "type-id": "5dcc52af-7064-4051-8d62-7d80f4c3c907",
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
                                    "type": "engineer",
                                    "type-id": "5dcc52af-7064-4051-8d62-7d80f4c3c907",
                                    "target": "a5c6f645-c4db-4cd3-9129-a3ebe9bbabea",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "a5c6f645-c4db-4cd3-9129-a3ebe9bbabea",
                                        "type": "Person",
                                        "name": "Brent Kolatalo",
                                        "sort-name": "Kolatalo, Brent",
                                    },
                                },
                                {
                                    "type": "engineer",
                                    "type-id": "5dcc52af-7064-4051-8d62-7d80f4c3c907",
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
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "8af4f66f-31ea-45ab-92bb-e6cbfaaf87d9",
                                    "direction": "backward",
                                    "attribute-list": ["French horn"],
                                    "artist": {
                                        "id": "8af4f66f-31ea-45ab-92bb-e6cbfaaf87d9",
                                        "type": "Person",
                                        "name": "Tim Anderson",
                                        "sort-name": "Anderson, Tim",
                                        "disambiguation": "horn player",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "f9abcd44-52d6-4424-b3a0-67f003bbbf3d",
                                            "attribute": "French horn",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "35fa8888-f0cc-4c4c-bfbf-a99def95f74e",
                                    "direction": "backward",
                                    "attribute-list": ["French horn"],
                                    "artist": {
                                        "id": "35fa8888-f0cc-4c4c-bfbf-a99def95f74e",
                                        "type": "Person",
                                        "name": "Richard Ashton",
                                        "sort-name": "Ashton, Richard",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "f9abcd44-52d6-4424-b3a0-67f003bbbf3d",
                                            "attribute": "French horn",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["keyboard"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        }
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
                                    "target": "7481f4a7-2a2a-4fa7-8a53-128e247e493d",
                                    "direction": "backward",
                                    "attribute-list": ["cello"],
                                    "artist": {
                                        "id": "7481f4a7-2a2a-4fa7-8a53-128e247e493d",
                                        "type": "Person",
                                        "name": "Rosie Danvers",
                                        "sort-name": "Danvers, Rosie",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0db03a60-1142-4b25-ab1b-72027d0dc357",
                                            "attribute": "cello",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["keyboard"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "e54e8707-837c-4aa4-a7be-deb95938de5f",
                                    "direction": "backward",
                                    "attribute-list": ["trumpet"],
                                    "artist": {
                                        "id": "e54e8707-837c-4aa4-a7be-deb95938de5f",
                                        "type": "Person",
                                        "name": "Simon Finch",
                                        "sort-name": "Finch, Simon",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "1c8f9780-2f16-4891-b66d-bb7aa0820dbd",
                                            "attribute": "trumpet",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "1c6693fe-3fa0-4b45-8b5f-ee68978c6bc5",
                                    "direction": "backward",
                                    "attribute-list": ["brass", "woodwind"],
                                    "artist": {
                                        "id": "1c6693fe-3fa0-4b45-8b5f-ee68978c6bc5",
                                        "type": "Person",
                                        "name": "Danny Flam",
                                        "sort-name": "Flam, Danny",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "82157c40-112f-4e4a-a3c0-5388ebb12931",
                                            "attribute": "brass",
                                        },
                                        {
                                            "type-id": "35df3318-7a89-4601-bccc-4cd27ba062f7",
                                            "attribute": "woodwind",
                                        },
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "8707aba3-625c-4a6b-a10c-834651a7788b",
                                    "direction": "backward",
                                    "attribute-list": ["trombone"],
                                    "artist": {
                                        "id": "8707aba3-625c-4a6b-a10c-834651a7788b",
                                        "type": "Person",
                                        "name": "Mark Frost",
                                        "sort-name": "Frost, Mark",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "f6100277-c7b8-4c8d-aa26-d8cd014b6761",
                                            "attribute": "trombone",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "960130c1-6d3e-47a5-b9d7-811a5c43a262",
                                    "direction": "backward",
                                    "attribute-list": ["trumpet"],
                                    "artist": {
                                        "id": "960130c1-6d3e-47a5-b9d7-811a5c43a262",
                                        "type": "Person",
                                        "name": "Andy Gathercole",
                                        "sort-name": "Gathercole, Andy",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "1c8f9780-2f16-4891-b66d-bb7aa0820dbd",
                                            "attribute": "trumpet",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "aa2bca02-d5f5-4490-86b6-d9bfb7140a33",
                                    "direction": "backward",
                                    "attribute-list": ["brass", "woodwind"],
                                    "artist": {
                                        "id": "aa2bca02-d5f5-4490-86b6-d9bfb7140a33",
                                        "type": "Person",
                                        "name": "Tony Gorruso",
                                        "sort-name": "Gorruso, Tony",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "82157c40-112f-4e4a-a3c0-5388ebb12931",
                                            "attribute": "brass",
                                        },
                                        {
                                            "type-id": "35df3318-7a89-4601-bccc-4cd27ba062f7",
                                            "attribute": "woodwind",
                                        },
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "b83bc61f-8451-4a5d-8b8e-7e9ed295e822",
                                    "direction": "backward",
                                    "attribute-list": ["piano"],
                                    "artist": {
                                        "id": "b83bc61f-8451-4a5d-8b8e-7e9ed295e822",
                                        "type": "Person",
                                        "name": "Elton John",
                                        "sort-name": "John, Elton",
                                        "disambiguation": "English singer, songwriter, pianist, and composer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "b3eac5f9-7859-4416-ac39-7154e2e8d348",
                                            "attribute": "piano",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "af728b40-baa9-4a6b-a6e9-d4cda9bccd43",
                                    "direction": "backward",
                                    "attribute-list": ["trombone"],
                                    "artist": {
                                        "id": "af728b40-baa9-4a6b-a6e9-d4cda9bccd43",
                                        "type": "Person",
                                        "name": "Philip Judge",
                                        "sort-name": "Judge, Philip",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "f6100277-c7b8-4c8d-aa26-d8cd014b6761",
                                            "attribute": "trombone",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "066741c8-b6fe-41d3-960c-10bc284e147e",
                                    "direction": "backward",
                                    "attribute-list": ["violin family"],
                                    "artist": {
                                        "id": "066741c8-b6fe-41d3-960c-10bc284e147e",
                                        "type": "Person",
                                        "name": "Sato Kotono",
                                        "sort-name": "Kotono, Sato",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "39354e17-ab05-4aa5-b503-3092a6b4622c",
                                            "attribute": "violin family",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                    "direction": "backward",
                                    "attribute-list": ["brass", "woodwind"],
                                    "artist": {
                                        "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                        "type": "Person",
                                        "name": "Ken Lewis",
                                        "sort-name": "Lewis, Ken",
                                        "disambiguation": "recording engineer and mixer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "82157c40-112f-4e4a-a3c0-5388ebb12931",
                                            "attribute": "brass",
                                        },
                                        {
                                            "type-id": "35df3318-7a89-4601-bccc-4cd27ba062f7",
                                            "attribute": "woodwind",
                                        },
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "70f935ed-952c-4283-8898-708b16766fa6",
                                    "direction": "backward",
                                    "attribute-list": ["trumpet"],
                                    "artist": {
                                        "id": "70f935ed-952c-4283-8898-708b16766fa6",
                                        "type": "Person",
                                        "name": "Mike Lovatt",
                                        "sort-name": "Lovatt, Mike",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "1c8f9780-2f16-4891-b66d-bb7aa0820dbd",
                                            "attribute": "trumpet",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "669122dd-c354-40ef-acfc-0718f867b0ab",
                                    "direction": "backward",
                                    "attribute-list": ["viola"],
                                    "artist": {
                                        "id": "669122dd-c354-40ef-acfc-0718f867b0ab",
                                        "type": "Person",
                                        "name": "Rachel Robson",
                                        "sort-name": "Robson, Rachel",
                                        "disambiguation": "violist",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "377e007a-33fe-4825-9bef-136cf5cf581a",
                                            "attribute": "viola",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "cad3d64e-e18d-455a-95ee-ae0ea3795087",
                                    "direction": "backward",
                                    "attribute-list": ["French horn"],
                                    "artist": {
                                        "id": "cad3d64e-e18d-455a-95ee-ae0ea3795087",
                                        "type": "Person",
                                        "name": "Tom Rumsby",
                                        "sort-name": "Rumsby, Tom",
                                        "disambiguation": "horn player",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "f9abcd44-52d6-4424-b3a0-67f003bbbf3d",
                                            "attribute": "French horn",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "a772d4df-70dd-4044-86c4-9c7b10319edf",
                                    "direction": "backward",
                                    "attribute-list": ["violin family"],
                                    "artist": {
                                        "id": "a772d4df-70dd-4044-86c4-9c7b10319edf",
                                        "type": "Person",
                                        "name": "Jenny Sacha",
                                        "sort-name": "Sacha, Jenny",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "39354e17-ab05-4aa5-b503-3092a6b4622c",
                                            "attribute": "violin family",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "cfb31d3d-5a6b-4fc8-9c77-a1c440e0eeb6",
                                    "direction": "backward",
                                    "attribute-list": ["flute"],
                                    "artist": {
                                        "id": "cfb31d3d-5a6b-4fc8-9c77-a1c440e0eeb6",
                                        "type": "Person",
                                        "name": "Chloe Vincent",
                                        "sort-name": "Vincent, Chloe",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "540280f1-d6cf-46bf-968b-695e99e216d7",
                                            "attribute": "flute",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument arranger",
                                    "type-id": "4820daa1-98d6-4f8b-aa4b-6895c5b79b27",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["cello"],
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
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument arranger",
                                    "type-id": "4820daa1-98d6-4f8b-aa4b-6895c5b79b27",
                                    "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                    "direction": "backward",
                                    "attribute-list": ["horn"],
                                    "artist": {
                                        "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                        "type": "Person",
                                        "name": "Ken Lewis",
                                        "sort-name": "Lewis, Ken",
                                        "disambiguation": "recording engineer and mixer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "e798a2bd-a578-4c28-8eea-6eca2d8b2c5d",
                                            "attribute": "horn",
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
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["co"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ac6f6b4c-a4ec-4483-a04e-9f425a914573",
                                            "attribute": "co",
                                        }
                                    ],
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "1585dc61-099b-4efb-9baf-22321fc853d2",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "1585dc61-099b-4efb-9baf-22321fc853d2",
                                        "type": "Person",
                                        "name": "Tommy Danvers",
                                        "sort-name": "Danvers, Tommy",
                                    },
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
                                    "target": "8dd4dd69-729d-49d2-92cc-001139f49892",
                                    "direction": "backward",
                                    "attribute-list": ["lead vocals"],
                                    "artist": {
                                        "id": "8dd4dd69-729d-49d2-92cc-001139f49892",
                                        "type": "Person",
                                        "name": "Marcos Tovar",
                                        "sort-name": "Tovar, Marcos",
                                        "disambiguation": "engineer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "8e2a3255-87c2-4809-a174-98cb3704f1a5",
                                            "attribute": "lead vocals",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "9fff2f8a-21e6-47de-a2b8-7f449929d43f",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "9fff2f8a-21e6-47de-a2b8-7f449929d43f",
                                        "type": "Person",
                                        "name": "Drake",
                                        "sort-name": "Drake",
                                        "disambiguation": "Canadian actor/rapper",
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
                                    "target": "1c46e82f-4764-4d82-a33b-5d5aee5e2881",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "1c46e82f-4764-4d82-a33b-5d5aee5e2881",
                                        "type": "Person",
                                        "name": "Fergie",
                                        "sort-name": "Fergie",
                                        "disambiguation": "member of The Black Eyed Peas",
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
                                    "target": "9fa19223-ec32-4da2-b1a2-79ea8afeb17a",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "9fa19223-ec32-4da2-b1a2-79ea8afeb17a",
                                        "type": "Person",
                                        "name": "Alvin Fields",
                                        "sort-name": "Fields, Alvin",
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
                                    "target": "eb7fd13f-5239-4751-bc1f-665f0f1f9dd7",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "eb7fd13f-5239-4751-bc1f-665f0f1f9dd7",
                                        "type": "Person",
                                        "name": "Elly Jackson",
                                        "sort-name": "Jackson, Elly",
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
                                    "target": "b83bc61f-8451-4a5d-8b8e-7e9ed295e822",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "b83bc61f-8451-4a5d-8b8e-7e9ed295e822",
                                        "type": "Person",
                                        "name": "Elton John",
                                        "sort-name": "John, Elton",
                                        "disambiguation": "English singer, songwriter, pianist, and composer",
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
                                    "target": "8ef1df30-ae4f-4dbd-9351-1a32b208a01e",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "8ef1df30-ae4f-4dbd-9351-1a32b208a01e",
                                        "type": "Person",
                                        "name": "Alicia Keys",
                                        "sort-name": "Keys, Alicia",
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
                                    "target": "e0e1db18-f7ba-4dee-95ff-7ae8cf545460",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "e0e1db18-f7ba-4dee-95ff-7ae8cf545460",
                                        "type": "Person",
                                        "name": "Kid Cudi",
                                        "sort-name": "Kid Cudi",
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
                                    "target": "75a72702-a5ef-4513-bca5-c5b944903546",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "75a72702-a5ef-4513-bca5-c5b944903546",
                                        "type": "Person",
                                        "name": "John Legend",
                                        "sort-name": "Legend, John",
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
                                    "target": "4bbc8087-548d-4484-abd2-5b1f4c1a7940",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "4bbc8087-548d-4484-abd2-5b1f4c1a7940",
                                        "type": "Person",
                                        "name": "Ryan Leslie",
                                        "sort-name": "Leslie, Ryan",
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
                                    "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                        "type": "Person",
                                        "name": "Ken Lewis",
                                        "sort-name": "Lewis, Ken",
                                        "disambiguation": "recording engineer and mixer",
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
                                    "target": "73e5e69d-3554-40d8-8516-00cb38737a1c",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "73e5e69d-3554-40d8-8516-00cb38737a1c",
                                        "type": "Person",
                                        "name": "Rihanna",
                                        "sort-name": "Rihanna",
                                        "disambiguation": "Barbadian R&B/pop singer",
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
                                    "target": "66a4b9d2-d5a6-40b8-93d5-0bdd1dbb4b43",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "66a4b9d2-d5a6-40b8-93d5-0bdd1dbb4b43",
                                        "type": "Person",
                                        "name": "The‐Dream",
                                        "sort-name": "The‐Dream",
                                        "disambiguation": "US singer, songwriter & RnB producer Terius Youngdell Nash",
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
                                    "target": "a42fdc0b-09bc-4a6d-8ae6-db454bf0803a",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "a42fdc0b-09bc-4a6d-8ae6-db454bf0803a",
                                        "type": "Person",
                                        "name": "Tony Williams",
                                        "sort-name": "Williams, Tony",
                                        "disambiguation": "soul/R&B singer/writer",
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
                                    "target": "b2d7c5e9-0e74-45e9-99a2-de24c19ee014",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "b2d7c5e9-0e74-45e9-99a2-de24c19ee014",
                                        "type": "Person",
                                        "name": "Charlie Wilson",
                                        "sort-name": "Wilson, Charlie",
                                        "disambiguation": "R&B singer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        }
                                    ],
                                },
                            ],
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "f376b1bb-da06-3c40-9f01-7a7a910bbe47",
                                    "direction": "forward",
                                    "work": {
                                        "id": "f376b1bb-da06-3c40-9f01-7a7a910bbe47",
                                        "title": "All of the Lights",
                                        "artist-relation-list": [
                                            {
                                                "type": "orchestrator",
                                                "type-id": "0a1771e1-8639-4740-8a43-bdafc050c3da",
                                                "target": "7481f4a7-2a2a-4fa7-8a53-128e247e493d",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "7481f4a7-2a2a-4fa7-8a53-128e247e493d",
                                                    "type": "Person",
                                                    "name": "Rosie Danvers",
                                                    "sort-name": "Danvers, Rosie",
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
                                                "target": "6c6447e1-a906-4882-9b19-cbafdbfaa8d5",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "6c6447e1-a906-4882-9b19-cbafdbfaa8d5",
                                                    "type": "Person",
                                                    "name": "Warren Trotter",
                                                    "sort-name": "Trotter, Warren",
                                                },
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
                        "track_or_recording_length": "301853",
                    },
                    {
                        "id": "a96cf92e-6f71-3938-a0cd-5f7627527958",
                        "position": "6",
                        "number": "6",
                        "length": "380893",
                        "recording": {
                            "id": "2beff74d-69fe-4e53-9a47-26f29b64c6d4",
                            "title": "Monster",
                            "length": "378893",
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
                                    "name": "Jay‐Z",
                                    "artist": {
                                        "id": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                        "type": "Person",
                                        "name": "JAY‐Z",
                                        "sort-name": "JAY‐Z",
                                        "disambiguation": "US rapper",
                                        "alias-list": [
                                            {
                                                "sort-name": "Hova",
                                                "type": "Artist name",
                                                "alias": "Hova",
                                            },
                                            {
                                                "sort-name": "Hova da God",
                                                "type": "Artist name",
                                                "alias": "Hova da God",
                                            },
                                            {
                                                "sort-name": "JAY Z",
                                                "type": "Artist name",
                                                "alias": "JAY Z",
                                            },
                                            {
                                                "sort-name": "Jay - Z",
                                                "type": "Search hint",
                                                "alias": "Jay - Z",
                                            },
                                            {
                                                "sort-name": "Jay Z",
                                                "type": "Search hint",
                                                "alias": "Jay Z",
                                            },
                                            {
                                                "sort-name": "Jay-Hova",
                                                "type": "Artist name",
                                                "alias": "Jay-Hova",
                                            },
                                            {
                                                "sort-name": "Jay-Z",
                                                "type": "Artist name",
                                                "alias": "Jay-Z",
                                            },
                                            {"sort-name": "Jayz", "alias": "Jayz"},
                                            {
                                                "sort-name": "Jaÿ-Z",
                                                "type": "Search hint",
                                                "alias": "Jaÿ-Z",
                                            },
                                            {
                                                "sort-name": "Jigga",
                                                "type": "Artist name",
                                                "alias": "Jigga",
                                            },
                                            {
                                                "sort-name": "S. Carter",
                                                "alias": "S. Carter",
                                            },
                                            {
                                                "sort-name": "Shawn C Carter",
                                                "alias": "Shawn C Carter",
                                            },
                                            {
                                                "sort-name": "Carter, Shawn",
                                                "alias": "Shawn Carter",
                                            },
                                            {
                                                "locale": "en",
                                                "sort-name": "Carter, Shawn Corey",
                                                "type": "Legal name",
                                                "alias": "Shawn Corey Carter",
                                            },
                                            {
                                                "sort-name": "Carter, Shawn Corey",
                                                "type": "Legal name",
                                                "alias": "Shawn Corey Carter",
                                            },
                                        ],
                                        "alias-count": 15,
                                    },
                                },
                                ", ",
                                {
                                    "artist": {
                                        "id": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                        "type": "Person",
                                        "name": "Rick Ross",
                                        "sort-name": "Ross, Rick",
                                        "disambiguation": "US rapper",
                                        "alias-list": [
                                            {
                                                "sort-name": "Rick Ro$$",
                                                "alias": "Rick Ro$$",
                                            },
                                            {
                                                "sort-name": "W. Roberts",
                                                "alias": "W. Roberts",
                                            },
                                            {
                                                "sort-name": "Roberts, William Leonard II",
                                                "type": "Legal name",
                                                "alias": "William Leonard Roberts II",
                                            },
                                        ],
                                        "alias-count": 3,
                                    }
                                },
                                ", ",
                                {
                                    "artist": {
                                        "id": "1036b808-f58c-4a3e-b461-a2c4492ecf1b",
                                        "type": "Person",
                                        "name": "Nicki Minaj",
                                        "sort-name": "Minaj, Nicki",
                                        "alias-list": [
                                            {
                                                "sort-name": "Nicki Minai",
                                                "alias": "Nicki Minai",
                                            },
                                            {
                                                "sort-name": "Nikki Minaj",
                                                "alias": "Nikki Minaj",
                                            },
                                            {
                                                "sort-name": "O. Maraj",
                                                "alias": "O. Maraj",
                                            },
                                            {
                                                "sort-name": "Maraj, Onika",
                                                "alias": "Onika Maraj",
                                            },
                                            {
                                                "sort-name": "Maraj, Onika Tanya",
                                                "type": "Legal name",
                                                "alias": "Onika Tanya Maraj",
                                            },
                                            {
                                                "sort-name": "Maraj-Petty, Onika Tanya",
                                                "type": "Legal name",
                                                "alias": "Onika Tanya Maraj-Petty",
                                            },
                                            {
                                                "locale": "ja",
                                                "sort-name": "ニッキー・ミナージュ",
                                                "alias": "ニッキー・ミナージュ",
                                            },
                                            {"sort-name": "妮琪米娜", "alias": "妮琪米娜"},
                                        ],
                                        "alias-count": 8,
                                    }
                                },
                                " & ",
                                {
                                    "artist": {
                                        "id": "437a0e49-c6ae-42f6-a6c1-84f25ed366bc",
                                        "type": "Group",
                                        "name": "Bon Iver",
                                        "sort-name": "Bon Iver",
                                    }
                                },
                            ],
                            "artist-relation-list": [
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["piano"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "b3eac5f9-7859-4416-ac39-7154e2e8d348",
                                            "attribute": "piano",
                                        }
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
                                    "target": "076774d8-e82d-482f-bd08-0b991b8d5469",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "076774d8-e82d-482f-bd08-0b991b8d5469",
                                        "type": "Person",
                                        "name": "Plain Pat",
                                        "sort-name": "Plain Pat",
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
                                    "target": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                        "type": "Person",
                                        "name": "JAY‐Z",
                                        "sort-name": "JAY‐Z",
                                        "disambiguation": "US rapper",
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
                                    "target": "1036b808-f58c-4a3e-b461-a2c4492ecf1b",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "1036b808-f58c-4a3e-b461-a2c4492ecf1b",
                                        "type": "Person",
                                        "name": "Nicki Minaj",
                                        "sort-name": "Minaj, Nicki",
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
                                    "target": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                        "type": "Person",
                                        "name": "Rick Ross",
                                        "sort-name": "Ross, Rick",
                                        "disambiguation": "US rapper",
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
                                    "target": "6f029cab-9713-3226-a7af-a113a8cde164",
                                    "direction": "forward",
                                    "work": {
                                        "id": "6f029cab-9713-3226-a7af-a113a8cde164",
                                        "type": "Song",
                                        "title": "Monster",
                                        "language": "eng",
                                        "iswc": "T-910.966.919-4",
                                        "iswc-list": ["T-910.966.919-4"],
                                        "artist-relation-list": [
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
                                                "target": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                                    "type": "Person",
                                                    "name": "JAY‐Z",
                                                    "sort-name": "JAY‐Z",
                                                    "disambiguation": "US rapper",
                                                },
                                                "target-credit": "Shawn Carter",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "1036b808-f58c-4a3e-b461-a2c4492ecf1b",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "1036b808-f58c-4a3e-b461-a2c4492ecf1b",
                                                    "type": "Person",
                                                    "name": "Nicki Minaj",
                                                    "sort-name": "Minaj, Nicki",
                                                },
                                                "target-credit": "Onika Maraj",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "d174f580-15bb-49d1-b9d9-086954a71877",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "d174f580-15bb-49d1-b9d9-086954a71877",
                                                    "type": "Person",
                                                    "name": "Patrick Reynolds",
                                                    "sort-name": "Reynolds, Patrick",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                                    "type": "Person",
                                                    "name": "Rick Ross",
                                                    "sort-name": "Ross, Rick",
                                                    "disambiguation": "US rapper",
                                                },
                                                "target-credit": "William Leonard Roberts II",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "0f1d5b01-8784-4870-9bd6-fa43178b9441",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "0f1d5b01-8784-4870-9bd6-fa43178b9441",
                                                    "type": "Person",
                                                    "name": "Justin Vernon",
                                                    "sort-name": "Vernon, Justin",
                                                },
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
                                        ],
                                    },
                                }
                            ],
                            "artist-credit-phrase": "Kanye West feat. Jay‐Z, Rick Ross, Nicki Minaj & Bon Iver",
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
                                "name": "Jay‐Z",
                                "artist": {
                                    "id": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                    "type": "Person",
                                    "name": "JAY‐Z",
                                    "sort-name": "JAY‐Z",
                                    "disambiguation": "US rapper",
                                    "alias-list": [
                                        {
                                            "sort-name": "Hova",
                                            "type": "Artist name",
                                            "alias": "Hova",
                                        },
                                        {
                                            "sort-name": "Hova da God",
                                            "type": "Artist name",
                                            "alias": "Hova da God",
                                        },
                                        {
                                            "sort-name": "JAY Z",
                                            "type": "Artist name",
                                            "alias": "JAY Z",
                                        },
                                        {
                                            "sort-name": "Jay - Z",
                                            "type": "Search hint",
                                            "alias": "Jay - Z",
                                        },
                                        {
                                            "sort-name": "Jay Z",
                                            "type": "Search hint",
                                            "alias": "Jay Z",
                                        },
                                        {
                                            "sort-name": "Jay-Hova",
                                            "type": "Artist name",
                                            "alias": "Jay-Hova",
                                        },
                                        {
                                            "sort-name": "Jay-Z",
                                            "type": "Artist name",
                                            "alias": "Jay-Z",
                                        },
                                        {"sort-name": "Jayz", "alias": "Jayz"},
                                        {
                                            "sort-name": "Jaÿ-Z",
                                            "type": "Search hint",
                                            "alias": "Jaÿ-Z",
                                        },
                                        {
                                            "sort-name": "Jigga",
                                            "type": "Artist name",
                                            "alias": "Jigga",
                                        },
                                        {
                                            "sort-name": "S. Carter",
                                            "alias": "S. Carter",
                                        },
                                        {
                                            "sort-name": "Shawn C Carter",
                                            "alias": "Shawn C Carter",
                                        },
                                        {
                                            "sort-name": "Carter, Shawn",
                                            "alias": "Shawn Carter",
                                        },
                                        {
                                            "locale": "en",
                                            "sort-name": "Carter, Shawn Corey",
                                            "type": "Legal name",
                                            "alias": "Shawn Corey Carter",
                                        },
                                        {
                                            "sort-name": "Carter, Shawn Corey",
                                            "type": "Legal name",
                                            "alias": "Shawn Corey Carter",
                                        },
                                    ],
                                    "alias-count": 15,
                                },
                            },
                            ", ",
                            {
                                "artist": {
                                    "id": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                    "type": "Person",
                                    "name": "Rick Ross",
                                    "sort-name": "Ross, Rick",
                                    "disambiguation": "US rapper",
                                    "alias-list": [
                                        {
                                            "sort-name": "Rick Ro$$",
                                            "alias": "Rick Ro$$",
                                        },
                                        {
                                            "sort-name": "W. Roberts",
                                            "alias": "W. Roberts",
                                        },
                                        {
                                            "sort-name": "Roberts, William Leonard II",
                                            "type": "Legal name",
                                            "alias": "William Leonard Roberts II",
                                        },
                                    ],
                                    "alias-count": 3,
                                }
                            },
                            ", ",
                            {
                                "artist": {
                                    "id": "1036b808-f58c-4a3e-b461-a2c4492ecf1b",
                                    "type": "Person",
                                    "name": "Nicki Minaj",
                                    "sort-name": "Minaj, Nicki",
                                    "alias-list": [
                                        {
                                            "sort-name": "Nicki Minai",
                                            "alias": "Nicki Minai",
                                        },
                                        {
                                            "sort-name": "Nikki Minaj",
                                            "alias": "Nikki Minaj",
                                        },
                                        {"sort-name": "O. Maraj", "alias": "O. Maraj"},
                                        {
                                            "sort-name": "Maraj, Onika",
                                            "alias": "Onika Maraj",
                                        },
                                        {
                                            "sort-name": "Maraj, Onika Tanya",
                                            "type": "Legal name",
                                            "alias": "Onika Tanya Maraj",
                                        },
                                        {
                                            "sort-name": "Maraj-Petty, Onika Tanya",
                                            "type": "Legal name",
                                            "alias": "Onika Tanya Maraj-Petty",
                                        },
                                        {
                                            "locale": "ja",
                                            "sort-name": "ニッキー・ミナージュ",
                                            "alias": "ニッキー・ミナージュ",
                                        },
                                        {"sort-name": "妮琪米娜", "alias": "妮琪米娜"},
                                    ],
                                    "alias-count": 8,
                                }
                            },
                            " & ",
                            {
                                "artist": {
                                    "id": "437a0e49-c6ae-42f6-a6c1-84f25ed366bc",
                                    "type": "Group",
                                    "name": "Bon Iver",
                                    "sort-name": "Bon Iver",
                                }
                            },
                        ],
                        "artist-credit-phrase": "Kanye West feat. Jay‐Z, Rick Ross, Nicki Minaj & Bon Iver",
                        "track_or_recording_length": "380893",
                    },
                    {
                        "id": "ab8b63ee-6bf5-3f4c-a770-4b3c854643b8",
                        "position": "7",
                        "number": "7",
                        "length": "400280",
                        "recording": {
                            "id": "36e2b944-e497-4b83-9bbb-0723fcb197f8",
                            "title": "So Appalled",
                            "length": "398173",
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
                                    "name": "Jay‐Z",
                                    "artist": {
                                        "id": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                        "type": "Person",
                                        "name": "JAY‐Z",
                                        "sort-name": "JAY‐Z",
                                        "disambiguation": "US rapper",
                                        "alias-list": [
                                            {
                                                "sort-name": "Hova",
                                                "type": "Artist name",
                                                "alias": "Hova",
                                            },
                                            {
                                                "sort-name": "Hova da God",
                                                "type": "Artist name",
                                                "alias": "Hova da God",
                                            },
                                            {
                                                "sort-name": "JAY Z",
                                                "type": "Artist name",
                                                "alias": "JAY Z",
                                            },
                                            {
                                                "sort-name": "Jay - Z",
                                                "type": "Search hint",
                                                "alias": "Jay - Z",
                                            },
                                            {
                                                "sort-name": "Jay Z",
                                                "type": "Search hint",
                                                "alias": "Jay Z",
                                            },
                                            {
                                                "sort-name": "Jay-Hova",
                                                "type": "Artist name",
                                                "alias": "Jay-Hova",
                                            },
                                            {
                                                "sort-name": "Jay-Z",
                                                "type": "Artist name",
                                                "alias": "Jay-Z",
                                            },
                                            {"sort-name": "Jayz", "alias": "Jayz"},
                                            {
                                                "sort-name": "Jaÿ-Z",
                                                "type": "Search hint",
                                                "alias": "Jaÿ-Z",
                                            },
                                            {
                                                "sort-name": "Jigga",
                                                "type": "Artist name",
                                                "alias": "Jigga",
                                            },
                                            {
                                                "sort-name": "S. Carter",
                                                "alias": "S. Carter",
                                            },
                                            {
                                                "sort-name": "Shawn C Carter",
                                                "alias": "Shawn C Carter",
                                            },
                                            {
                                                "sort-name": "Carter, Shawn",
                                                "alias": "Shawn Carter",
                                            },
                                            {
                                                "locale": "en",
                                                "sort-name": "Carter, Shawn Corey",
                                                "type": "Legal name",
                                                "alias": "Shawn Corey Carter",
                                            },
                                            {
                                                "sort-name": "Carter, Shawn Corey",
                                                "type": "Legal name",
                                                "alias": "Shawn Corey Carter",
                                            },
                                        ],
                                        "alias-count": 15,
                                    },
                                },
                                ", ",
                                {
                                    "artist": {
                                        "id": "14ecd19f-7121-4192-8549-e5056241a42f",
                                        "type": "Person",
                                        "name": "Pusha T",
                                        "sort-name": "Pusha T",
                                        "alias-list": [
                                            {"sort-name": "Pusha", "alias": "Pusha"}
                                        ],
                                        "alias-count": 1,
                                    }
                                },
                                ", ",
                                {
                                    "name": "CyHi da Prynce",
                                    "artist": {
                                        "id": "6a9e461c-e3c5-4794-a203-98a15daea2df",
                                        "type": "Person",
                                        "name": "CyHi the Prynce",
                                        "sort-name": "CyHi the Prynce",
                                        "alias-list": [
                                            {
                                                "sort-name": "Young, Cydel Charles",
                                                "type": "Legal name",
                                                "alias": "Cydel Charles Young",
                                            },
                                            {
                                                "sort-name": "Young, Cydel",
                                                "type": "Legal name",
                                                "alias": "Cydel Young",
                                            },
                                            {
                                                "sort-name": "Cyhi da Prynce",
                                                "alias": "Cyhi da Prynce",
                                            },
                                            {
                                                "sort-name": "Cyhi da prince",
                                                "alias": "Cyhi da prince",
                                            },
                                            {
                                                "sort-name": "Prince Cy Hi",
                                                "type": "Artist name",
                                                "alias": "Prince Cy Hi",
                                            },
                                        ],
                                        "alias-count": 5,
                                    },
                                },
                                ", ",
                                {
                                    "artist": {
                                        "id": "698ff525-ff51-4206-8f08-60a7458aab24",
                                        "type": "Person",
                                        "name": "Swizz Beatz",
                                        "sort-name": "Swizz Beatz",
                                        "disambiguation": "US hip hop producer",
                                        "alias-list": [
                                            {
                                                "sort-name": "K. Dean",
                                                "alias": "K. Dean",
                                            },
                                            {
                                                "sort-name": "Dean, Kaseem",
                                                "alias": "Kaseem Dean",
                                            },
                                            {
                                                "sort-name": "Dean, Kasseem Daoud",
                                                "type": "Legal name",
                                                "alias": "Kasseem Daoud Dean",
                                            },
                                            {
                                                "sort-name": "Dean, Kasseem Mike",
                                                "alias": "Kasseem Mike Dean",
                                            },
                                            {
                                                "sort-name": "Swiss Beats",
                                                "alias": "Swiss Beats",
                                            },
                                            {
                                                "sort-name": "Swizz Beats",
                                                "alias": "Swizz Beats",
                                            },
                                        ],
                                        "alias-count": 6,
                                    }
                                },
                                " & ",
                                {
                                    "name": "The RZA",
                                    "artist": {
                                        "id": "29c28ac3-27c5-4822-8eb6-0af89a3a7240",
                                        "type": "Person",
                                        "name": "RZA",
                                        "sort-name": "RZA",
                                        "disambiguation": "US rapper / producer",
                                        "alias-list": [
                                            {
                                                "sort-name": "Bobby Digital",
                                                "alias": "Bobby Digital",
                                            },
                                            {
                                                "sort-name": "Bobby Digital Presents",
                                                "alias": "Bobby Digital Presents",
                                            },
                                            {
                                                "sort-name": "Bobby Steels",
                                                "alias": "Bobby Steels",
                                            },
                                            {
                                                "sort-name": "Prince Rakeem",
                                                "alias": "Prince Rakeem",
                                            },
                                            {
                                                "sort-name": "R. Diggs",
                                                "alias": "R. Diggs",
                                            },
                                            {
                                                "sort-name": "RZA as Bobby Digital",
                                                "alias": "RZA as Bobby Digital",
                                            },
                                            {
                                                "sort-name": "Diggs, Robert, Jr.",
                                                "alias": "Robert Diggs, Jr.",
                                            },
                                            {
                                                "sort-name": "Ruler Zig-Zag-Zig-Allah",
                                                "alias": "Ruler Zig-Zag-Zig-Allah",
                                            },
                                            {
                                                "sort-name": "Rza (As Bobby Digital)",
                                                "alias": "Rza (As Bobby Digital)",
                                            },
                                            {
                                                "sort-name": "Abbott, The",
                                                "type": "Artist name",
                                                "alias": "The Abbott",
                                            },
                                            {
                                                "sort-name": "RZA, The",
                                                "type": "Artist name",
                                                "alias": "The RZA",
                                            },
                                            {
                                                "sort-name": "Rzarector, The",
                                                "type": "Artist name",
                                                "alias": "The Rzarector",
                                            },
                                        ],
                                        "alias-count": 12,
                                    },
                                },
                            ],
                            "artist-relation-list": [
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["keyboard"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        }
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
                                    "attribute-list": ["keyboard"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        }
                                    ],
                                },
                                {
                                    "type": "instrument arranger",
                                    "type-id": "4820daa1-98d6-4f8b-aa4b-6895c5b79b27",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["cello"],
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
                                        }
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
                                    "attribute-list": ["co"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ac6f6b4c-a4ec-4483-a04e-9f425a914573",
                                            "attribute": "co",
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
                                    "target": "49c19ad1-eca8-4a0d-99b3-645df7c83dc4",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "49c19ad1-eca8-4a0d-99b3-645df7c83dc4",
                                        "type": "Person",
                                        "name": "Pete Bischoff",
                                        "sort-name": "Bischoff, Pete",
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
                                    "target": "6a9e461c-e3c5-4794-a203-98a15daea2df",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "6a9e461c-e3c5-4794-a203-98a15daea2df",
                                        "type": "Person",
                                        "name": "CyHi the Prynce",
                                        "sort-name": "CyHi the Prynce",
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
                                    "target": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                        "type": "Person",
                                        "name": "JAY‐Z",
                                        "sort-name": "JAY‐Z",
                                        "disambiguation": "US rapper",
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
                                    "target": "14ecd19f-7121-4192-8549-e5056241a42f",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "14ecd19f-7121-4192-8549-e5056241a42f",
                                        "type": "Person",
                                        "name": "Pusha T",
                                        "sort-name": "Pusha T",
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
                                    "target": "29c28ac3-27c5-4822-8eb6-0af89a3a7240",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "29c28ac3-27c5-4822-8eb6-0af89a3a7240",
                                        "type": "Person",
                                        "name": "RZA",
                                        "sort-name": "RZA",
                                        "disambiguation": "US rapper / producer",
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
                                    "target": "698ff525-ff51-4206-8f08-60a7458aab24",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "698ff525-ff51-4206-8f08-60a7458aab24",
                                        "type": "Person",
                                        "name": "Swizz Beatz",
                                        "sort-name": "Swizz Beatz",
                                        "disambiguation": "US hip hop producer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "b3045913-62ac-433e-9211-ac683cdf6b5c",
                                            "attribute": "guest",
                                        }
                                    ],
                                },
                            ],
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "5dcba72d-ded2-3f3c-870d-6ddc4fdb22ee",
                                    "direction": "forward",
                                    "work": {
                                        "id": "5dcba72d-ded2-3f3c-870d-6ddc4fdb22ee",
                                        "title": "So Appalled",
                                        "artist-relation-list": [
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "6a9e461c-e3c5-4794-a203-98a15daea2df",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "6a9e461c-e3c5-4794-a203-98a15daea2df",
                                                    "type": "Person",
                                                    "name": "CyHi the Prynce",
                                                    "sort-name": "CyHi the Prynce",
                                                },
                                                "target-credit": "Cydel Young",
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
                                                "target": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                                    "type": "Person",
                                                    "name": "JAY‐Z",
                                                    "sort-name": "JAY‐Z",
                                                    "disambiguation": "US rapper",
                                                },
                                                "target-credit": "Shawn Carter",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "9c6d95f9-5101-49d9-ae1c-cff73b9e3317",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "9c6d95f9-5101-49d9-ae1c-cff73b9e3317",
                                                    "type": "Person",
                                                    "name": "Manfred Mann",
                                                    "sort-name": "Mann, Manfred",
                                                    "disambiguation": "the person",
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
                                                "target": "29c28ac3-27c5-4822-8eb6-0af89a3a7240",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "29c28ac3-27c5-4822-8eb6-0af89a3a7240",
                                                    "type": "Person",
                                                    "name": "RZA",
                                                    "sort-name": "RZA",
                                                    "disambiguation": "US rapper / producer",
                                                },
                                                "target-credit": "Robert Diggs, Jr.",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "698ff525-ff51-4206-8f08-60a7458aab24",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "698ff525-ff51-4206-8f08-60a7458aab24",
                                                    "type": "Person",
                                                    "name": "Swizz Beatz",
                                                    "sort-name": "Swizz Beatz",
                                                    "disambiguation": "US hip hop producer",
                                                },
                                                "target-credit": "Kasseem Mike Dean",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "4c7fb857-9f76-4a2e-a728-25722e6a1e76",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "4c7fb857-9f76-4a2e-a728-25722e6a1e76",
                                                    "type": "Person",
                                                    "name": "Terrence Thornton",
                                                    "sort-name": "Thornton, Terrence",
                                                },
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
                                        ],
                                    },
                                }
                            ],
                            "artist-credit-phrase": "Kanye West feat. Jay‐Z, Pusha T, CyHi da Prynce, Swizz Beatz & The RZA",
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
                                "name": "Jay‐Z",
                                "artist": {
                                    "id": "f82bcf78-5b69-4622-a5ef-73800768d9ac",
                                    "type": "Person",
                                    "name": "JAY‐Z",
                                    "sort-name": "JAY‐Z",
                                    "disambiguation": "US rapper",
                                    "alias-list": [
                                        {
                                            "sort-name": "Hova",
                                            "type": "Artist name",
                                            "alias": "Hova",
                                        },
                                        {
                                            "sort-name": "Hova da God",
                                            "type": "Artist name",
                                            "alias": "Hova da God",
                                        },
                                        {
                                            "sort-name": "JAY Z",
                                            "type": "Artist name",
                                            "alias": "JAY Z",
                                        },
                                        {
                                            "sort-name": "Jay - Z",
                                            "type": "Search hint",
                                            "alias": "Jay - Z",
                                        },
                                        {
                                            "sort-name": "Jay Z",
                                            "type": "Search hint",
                                            "alias": "Jay Z",
                                        },
                                        {
                                            "sort-name": "Jay-Hova",
                                            "type": "Artist name",
                                            "alias": "Jay-Hova",
                                        },
                                        {
                                            "sort-name": "Jay-Z",
                                            "type": "Artist name",
                                            "alias": "Jay-Z",
                                        },
                                        {"sort-name": "Jayz", "alias": "Jayz"},
                                        {
                                            "sort-name": "Jaÿ-Z",
                                            "type": "Search hint",
                                            "alias": "Jaÿ-Z",
                                        },
                                        {
                                            "sort-name": "Jigga",
                                            "type": "Artist name",
                                            "alias": "Jigga",
                                        },
                                        {
                                            "sort-name": "S. Carter",
                                            "alias": "S. Carter",
                                        },
                                        {
                                            "sort-name": "Shawn C Carter",
                                            "alias": "Shawn C Carter",
                                        },
                                        {
                                            "sort-name": "Carter, Shawn",
                                            "alias": "Shawn Carter",
                                        },
                                        {
                                            "locale": "en",
                                            "sort-name": "Carter, Shawn Corey",
                                            "type": "Legal name",
                                            "alias": "Shawn Corey Carter",
                                        },
                                        {
                                            "sort-name": "Carter, Shawn Corey",
                                            "type": "Legal name",
                                            "alias": "Shawn Corey Carter",
                                        },
                                    ],
                                    "alias-count": 15,
                                },
                            },
                            ", ",
                            {
                                "artist": {
                                    "id": "14ecd19f-7121-4192-8549-e5056241a42f",
                                    "type": "Person",
                                    "name": "Pusha T",
                                    "sort-name": "Pusha T",
                                    "alias-list": [
                                        {"sort-name": "Pusha", "alias": "Pusha"}
                                    ],
                                    "alias-count": 1,
                                }
                            },
                            ", ",
                            {
                                "name": "CyHi da Prynce",
                                "artist": {
                                    "id": "6a9e461c-e3c5-4794-a203-98a15daea2df",
                                    "type": "Person",
                                    "name": "CyHi the Prynce",
                                    "sort-name": "CyHi the Prynce",
                                    "alias-list": [
                                        {
                                            "sort-name": "Young, Cydel Charles",
                                            "type": "Legal name",
                                            "alias": "Cydel Charles Young",
                                        },
                                        {
                                            "sort-name": "Young, Cydel",
                                            "type": "Legal name",
                                            "alias": "Cydel Young",
                                        },
                                        {
                                            "sort-name": "Cyhi da Prynce",
                                            "alias": "Cyhi da Prynce",
                                        },
                                        {
                                            "sort-name": "Cyhi da prince",
                                            "alias": "Cyhi da prince",
                                        },
                                        {
                                            "sort-name": "Prince Cy Hi",
                                            "type": "Artist name",
                                            "alias": "Prince Cy Hi",
                                        },
                                    ],
                                    "alias-count": 5,
                                },
                            },
                            ", ",
                            {
                                "artist": {
                                    "id": "698ff525-ff51-4206-8f08-60a7458aab24",
                                    "type": "Person",
                                    "name": "Swizz Beatz",
                                    "sort-name": "Swizz Beatz",
                                    "disambiguation": "US hip hop producer",
                                    "alias-list": [
                                        {"sort-name": "K. Dean", "alias": "K. Dean"},
                                        {
                                            "sort-name": "Dean, Kaseem",
                                            "alias": "Kaseem Dean",
                                        },
                                        {
                                            "sort-name": "Dean, Kasseem Daoud",
                                            "type": "Legal name",
                                            "alias": "Kasseem Daoud Dean",
                                        },
                                        {
                                            "sort-name": "Dean, Kasseem Mike",
                                            "alias": "Kasseem Mike Dean",
                                        },
                                        {
                                            "sort-name": "Swiss Beats",
                                            "alias": "Swiss Beats",
                                        },
                                        {
                                            "sort-name": "Swizz Beats",
                                            "alias": "Swizz Beats",
                                        },
                                    ],
                                    "alias-count": 6,
                                }
                            },
                            " & ",
                            {
                                "name": "The RZA",
                                "artist": {
                                    "id": "29c28ac3-27c5-4822-8eb6-0af89a3a7240",
                                    "type": "Person",
                                    "name": "RZA",
                                    "sort-name": "RZA",
                                    "disambiguation": "US rapper / producer",
                                    "alias-list": [
                                        {
                                            "sort-name": "Bobby Digital",
                                            "alias": "Bobby Digital",
                                        },
                                        {
                                            "sort-name": "Bobby Digital Presents",
                                            "alias": "Bobby Digital Presents",
                                        },
                                        {
                                            "sort-name": "Bobby Steels",
                                            "alias": "Bobby Steels",
                                        },
                                        {
                                            "sort-name": "Prince Rakeem",
                                            "alias": "Prince Rakeem",
                                        },
                                        {"sort-name": "R. Diggs", "alias": "R. Diggs"},
                                        {
                                            "sort-name": "RZA as Bobby Digital",
                                            "alias": "RZA as Bobby Digital",
                                        },
                                        {
                                            "sort-name": "Diggs, Robert, Jr.",
                                            "alias": "Robert Diggs, Jr.",
                                        },
                                        {
                                            "sort-name": "Ruler Zig-Zag-Zig-Allah",
                                            "alias": "Ruler Zig-Zag-Zig-Allah",
                                        },
                                        {
                                            "sort-name": "Rza (As Bobby Digital)",
                                            "alias": "Rza (As Bobby Digital)",
                                        },
                                        {
                                            "sort-name": "Abbott, The",
                                            "type": "Artist name",
                                            "alias": "The Abbott",
                                        },
                                        {
                                            "sort-name": "RZA, The",
                                            "type": "Artist name",
                                            "alias": "The RZA",
                                        },
                                        {
                                            "sort-name": "Rzarector, The",
                                            "type": "Artist name",
                                            "alias": "The Rzarector",
                                        },
                                    ],
                                    "alias-count": 12,
                                },
                            },
                        ],
                        "artist-credit-phrase": "Kanye West feat. Jay‐Z, Pusha T, CyHi da Prynce, Swizz Beatz & The RZA",
                        "track_or_recording_length": "400280",
                    },
                    {
                        "id": "22aaec52-dbe1-32d9-a0f9-18341cfd0d8b",
                        "position": "8",
                        "number": "8",
                        "length": "354613",
                        "recording": {
                            "id": "c8da6e46-d517-4930-87d8-5be5ab9ca3c9",
                            "title": "Devil in a New Dress",
                            "length": "352466",
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
                                        "id": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                        "type": "Person",
                                        "name": "Rick Ross",
                                        "sort-name": "Ross, Rick",
                                        "disambiguation": "US rapper",
                                        "alias-list": [
                                            {
                                                "sort-name": "Rick Ro$$",
                                                "alias": "Rick Ro$$",
                                            },
                                            {
                                                "sort-name": "W. Roberts",
                                                "alias": "W. Roberts",
                                            },
                                            {
                                                "sort-name": "Roberts, William Leonard II",
                                                "type": "Legal name",
                                                "alias": "William Leonard Roberts II",
                                            },
                                        ],
                                        "alias-count": 3,
                                    }
                                },
                            ],
                            "artist-relation-list": [
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["bass", "guitar", "piano"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "6505f98c-f698-4406-8bf4-8ca43d05c36f",
                                            "attribute": "bass",
                                        },
                                        {
                                            "type-id": "63021302-86cd-4aee-80df-2270d54f4978",
                                            "attribute": "guitar",
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
                                    "target": "43d2e957-de35-4991-baea-2ce2ba0519d7",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "43d2e957-de35-4991-baea-2ce2ba0519d7",
                                        "type": "Person",
                                        "name": "Bink!",
                                        "sort-name": "Bink!",
                                    },
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
                                    "target": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                        "type": "Person",
                                        "name": "Rick Ross",
                                        "sort-name": "Ross, Rick",
                                        "disambiguation": "US rapper",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "b3045913-62ac-433e-9211-ac683cdf6b5c",
                                            "attribute": "guest",
                                        }
                                    ],
                                },
                            ],
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "07e7326c-a12d-38ba-b986-2eb7685c86f9",
                                    "direction": "forward",
                                    "work": {
                                        "id": "07e7326c-a12d-38ba-b986-2eb7685c86f9",
                                        "type": "Song",
                                        "title": "Devil in a New Dress",
                                        "language": "eng",
                                        "iswc": "T-911.405.350-8",
                                        "iswc-list": ["T-911.405.350-8"],
                                        "artist-relation-list": [
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "43d2e957-de35-4991-baea-2ce2ba0519d7",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "43d2e957-de35-4991-baea-2ce2ba0519d7",
                                                    "type": "Person",
                                                    "name": "Bink!",
                                                    "sort-name": "Bink!",
                                                },
                                                "target-credit": "Roosevelt Harrell III",
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
                                                "target": "d5709a02-30e0-4967-92ba-e584d8c21c72",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "d5709a02-30e0-4967-92ba-e584d8c21c72",
                                                    "type": "Person",
                                                    "name": "Gerry Goffin",
                                                    "sort-name": "Goffin, Gerry",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "bf6c29f5-b69f-4842-9031-37f9645d365d",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "bf6c29f5-b69f-4842-9031-37f9645d365d",
                                                    "type": "Person",
                                                    "name": "Carole King",
                                                    "sort-name": "King, Carole",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                                    "type": "Person",
                                                    "name": "Rick Ross",
                                                    "sort-name": "Ross, Rick",
                                                    "disambiguation": "US rapper",
                                                },
                                                "target-credit": "William Leonard Roberts II",
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
                            "artist-credit-phrase": "Kanye West feat. Rick Ross",
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
                                    "id": "13bcb2bb-db37-4397-baf5-e0f085be2d64",
                                    "type": "Person",
                                    "name": "Rick Ross",
                                    "sort-name": "Ross, Rick",
                                    "disambiguation": "US rapper",
                                    "alias-list": [
                                        {
                                            "sort-name": "Rick Ro$$",
                                            "alias": "Rick Ro$$",
                                        },
                                        {
                                            "sort-name": "W. Roberts",
                                            "alias": "W. Roberts",
                                        },
                                        {
                                            "sort-name": "Roberts, William Leonard II",
                                            "type": "Legal name",
                                            "alias": "William Leonard Roberts II",
                                        },
                                    ],
                                    "alias-count": 3,
                                }
                            },
                        ],
                        "artist-credit-phrase": "Kanye West feat. Rick Ross",
                        "track_or_recording_length": "354613",
                    },
                    {
                        "id": "329d6b2b-cc5c-3c19-8232-435791dec4df",
                        "position": "9",
                        "number": "9",
                        "length": "550173",
                        "recording": {
                            "id": "a24f67ff-a81e-4a95-817d-c0b4e5af3e6b",
                            "title": "Runaway",
                            "length": "548200",
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
                                        "id": "14ecd19f-7121-4192-8549-e5056241a42f",
                                        "type": "Person",
                                        "name": "Pusha T",
                                        "sort-name": "Pusha T",
                                        "alias-list": [
                                            {"sort-name": "Pusha", "alias": "Pusha"}
                                        ],
                                        "alias-count": 1,
                                    }
                                },
                            ],
                            "artist-relation-list": [
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["keyboard"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        }
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
                                    "type": "mix",
                                    "type-id": "3e3102e1-1896-4f50-b5b2-dd9824e46efe",
                                    "target": "705c4731-9021-4562-b63d-4fb2eec31821",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "705c4731-9021-4562-b63d-4fb2eec31821",
                                        "type": "Person",
                                        "name": "Cary Clark",
                                        "sort-name": "Clark, Cary",
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
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["co"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ac6f6b4c-a4ec-4483-a04e-9f425a914573",
                                            "attribute": "co",
                                        }
                                    ],
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["co"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ac6f6b4c-a4ec-4483-a04e-9f425a914573",
                                            "attribute": "co",
                                        }
                                    ],
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "d6f3c7d7-3c95-4bf6-8647-0efeec36d704",
                                    "direction": "backward",
                                    "attribute-list": ["co"],
                                    "artist": {
                                        "id": "d6f3c7d7-3c95-4bf6-8647-0efeec36d704",
                                        "type": "Person",
                                        "name": "Emile Haynie",
                                        "sort-name": "Haynie, Emile",
                                        "disambiguation": 'hip hop producer, aka "Emile"',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ac6f6b4c-a4ec-4483-a04e-9f425a914573",
                                            "attribute": "co",
                                        }
                                    ],
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
                                    "type": "recording",
                                    "type-id": "a01ee869-80a8-45ef-9447-c59e91aa7926",
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
                                    "type": "video director",
                                    "type-id": "578ee04d-3227-4335-ba2c-11e8ba420e0b",
                                    "target": "9b825c18-b870-48d6-9577-e28f1180babd",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "9b825c18-b870-48d6-9577-e28f1180babd",
                                        "type": "Person",
                                        "name": "Hype Williams",
                                        "sort-name": "Williams, Hype",
                                        "disambiguation": "music video director",
                                    },
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "14ecd19f-7121-4192-8549-e5056241a42f",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "14ecd19f-7121-4192-8549-e5056241a42f",
                                        "type": "Person",
                                        "name": "Pusha T",
                                        "sort-name": "Pusha T",
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
                                    "target": "66a4b9d2-d5a6-40b8-93d5-0bdd1dbb4b43",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "66a4b9d2-d5a6-40b8-93d5-0bdd1dbb4b43",
                                        "type": "Person",
                                        "name": "The‐Dream",
                                        "sort-name": "The‐Dream",
                                        "disambiguation": "US singer, songwriter & RnB producer Terius Youngdell Nash",
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
                                    "target": "bd8d153a-afff-30e7-a5e9-7efb62886ecb",
                                    "direction": "forward",
                                    "work": {
                                        "id": "bd8d153a-afff-30e7-a5e9-7efb62886ecb",
                                        "title": "Runaway",
                                        "artist-relation-list": [
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
                                                "target": "dbf49f65-d014-4100-9d51-cf9cf8df05bf",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "dbf49f65-d014-4100-9d51-cf9cf8df05bf",
                                                    "type": "Person",
                                                    "name": "J. Branch",
                                                    "sort-name": "Branch, J.",
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
                                                "target": "d6f3c7d7-3c95-4bf6-8647-0efeec36d704",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "d6f3c7d7-3c95-4bf6-8647-0efeec36d704",
                                                    "type": "Person",
                                                    "name": "Emile Haynie",
                                                    "sort-name": "Haynie, Emile",
                                                    "disambiguation": 'hip hop producer, aka "Emile"',
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "4c7fb857-9f76-4a2e-a728-25722e6a1e76",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "4c7fb857-9f76-4a2e-a728-25722e6a1e76",
                                                    "type": "Person",
                                                    "name": "Terrence Thornton",
                                                    "sort-name": "Thornton, Terrence",
                                                },
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
                            "artist-credit-phrase": "Kanye West feat. Pusha T",
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
                                    "id": "14ecd19f-7121-4192-8549-e5056241a42f",
                                    "type": "Person",
                                    "name": "Pusha T",
                                    "sort-name": "Pusha T",
                                    "alias-list": [
                                        {"sort-name": "Pusha", "alias": "Pusha"}
                                    ],
                                    "alias-count": 1,
                                }
                            },
                        ],
                        "artist-credit-phrase": "Kanye West feat. Pusha T",
                        "track_or_recording_length": "550173",
                    },
                    {
                        "id": "bc872f90-386b-35a9-817b-b2d4ee7c6324",
                        "position": "10",
                        "number": "10",
                        "length": "329933",
                        "recording": {
                            "id": "e848d5fd-4590-468a-89af-45e88262c8e3",
                            "title": "Hell of a Life",
                            "length": "327786",
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
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["keyboard"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        }
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
                                    "target": "defc4d0f-5eae-47b2-bd23-8b5373234a8c",
                                    "direction": "backward",
                                    "attribute-list": ["co"],
                                    "artist": {
                                        "id": "defc4d0f-5eae-47b2-bd23-8b5373234a8c",
                                        "type": "Person",
                                        "name": "Mike Caren",
                                        "sort-name": "Caren, Mike",
                                        "disambiguation": "US hip hop producer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ac6f6b4c-a4ec-4483-a04e-9f425a914573",
                                            "attribute": "co",
                                        }
                                    ],
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["co"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ac6f6b4c-a4ec-4483-a04e-9f425a914573",
                                            "attribute": "co",
                                        }
                                    ],
                                },
                                {
                                    "type": "producer",
                                    "type-id": "5c0ceac3-feb4-41f0-868d-dc06f6e27fc0",
                                    "target": "1cd913a1-5641-4b2a-9624-a0417914e3e7",
                                    "direction": "backward",
                                    "attribute-list": ["co"],
                                    "artist": {
                                        "id": "1cd913a1-5641-4b2a-9624-a0417914e3e7",
                                        "type": "Person",
                                        "name": "No I.D.",
                                        "sort-name": "No I.D.",
                                        "disambiguation": "producer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ac6f6b4c-a4ec-4483-a04e-9f425a914573",
                                            "attribute": "co",
                                        }
                                    ],
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
                                    "target": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                    "direction": "backward",
                                    "attribute-list": ["drums (drum set)"],
                                    "artist": {
                                        "id": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                        "type": "Person",
                                        "name": "Anthony Kilhoffer",
                                        "sort-name": "Kilhoffer, Anthony",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "12092505-6ee1-46af-a15a-b5b468b6b155",
                                            "attribute": "drums (drum set)",
                                        }
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
                                    "target": "66a4b9d2-d5a6-40b8-93d5-0bdd1dbb4b43",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "66a4b9d2-d5a6-40b8-93d5-0bdd1dbb4b43",
                                        "type": "Person",
                                        "name": "The‐Dream",
                                        "sort-name": "The‐Dream",
                                        "disambiguation": "US singer, songwriter & RnB producer Terius Youngdell Nash",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        }
                                    ],
                                },
                            ],
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "ed54f980-78f1-32ab-974b-62fae205123c",
                                    "direction": "forward",
                                    "work": {
                                        "id": "ed54f980-78f1-32ab-974b-62fae205123c",
                                        "type": "Song",
                                        "title": "Hell of a Life",
                                        "language": "eng",
                                        "iswc": "T-905.616.080-6",
                                        "iswc-list": ["T-905.616.080-6"],
                                        "artist-relation-list": [
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "123814ce-f7f7-44c9-b84d-0088b1e230a4",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "123814ce-f7f7-44c9-b84d-0088b1e230a4",
                                                    "type": "Person",
                                                    "name": "Geezer Butler",
                                                    "sort-name": "Butler, Geezer",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "defc4d0f-5eae-47b2-bd23-8b5373234a8c",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "defc4d0f-5eae-47b2-bd23-8b5373234a8c",
                                                    "type": "Person",
                                                    "name": "Mike Caren",
                                                    "sort-name": "Caren, Mike",
                                                    "disambiguation": "US hip hop producer",
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
                                                "target": "e5fa0175-2e93-4ca7-90c3-33f239381252",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "e5fa0175-2e93-4ca7-90c3-33f239381252",
                                                    "type": "Person",
                                                    "name": "Tony Iommi",
                                                    "sort-name": "Iommi, Tony",
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
                                                "target": "8aa5b65a-5b3c-4029-92bf-47a544356934",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "8aa5b65a-5b3c-4029-92bf-47a544356934",
                                                    "type": "Person",
                                                    "name": "Ozzy Osbourne",
                                                    "sort-name": "Osbourne, Ozzy",
                                                },
                                                "target-credit": "John Michael Osbourne",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "40a2d063-1b51-4251-90b3-4269d37737d3",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "40a2d063-1b51-4251-90b3-4269d37737d3",
                                                    "type": "Person",
                                                    "name": "Sylvester Stewart",
                                                    "sort-name": "Stewart, Sylvester",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "9082aea0-ee30-4175-8795-6540a8fd3605",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "9082aea0-ee30-4175-8795-6540a8fd3605",
                                                    "type": "Person",
                                                    "name": "Bill Ward",
                                                    "sort-name": "Ward, Bill",
                                                },
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
                                                "target": "810af667-6a1f-40df-87a9-27f726cba4f3",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "810af667-6a1f-40df-87a9-27f726cba4f3",
                                                    "type": "Person",
                                                    "name": "Tony Joe White",
                                                    "sort-name": "White, Tony Joe",
                                                },
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
                        "track_or_recording_length": "329933",
                    },
                    {
                        "id": "c6bc7852-06f0-3531-a4b5-b50b2d9ff8eb",
                        "position": "11",
                        "number": "11",
                        "length": "471933",
                        "recording": {
                            "id": "8089efd2-b32a-4b43-963f-7743e888793a",
                            "title": "Blame Game",
                            "length": "469866",
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
                                        "id": "75a72702-a5ef-4513-bca5-c5b944903546",
                                        "type": "Person",
                                        "name": "John Legend",
                                        "sort-name": "Legend, John",
                                        "alias-list": [
                                            {
                                                "sort-name": "Stephens, John Roger",
                                                "type": "Legal name",
                                                "alias": "John Roger Stephens",
                                            },
                                            {
                                                "sort-name": "Stephens, John",
                                                "alias": "John Stephens",
                                            },
                                        ],
                                        "alias-count": 2,
                                    }
                                },
                            ],
                            "artist-relation-list": [
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                    "direction": "backward",
                                    "attribute-list": ["bass", "piano"],
                                    "artist": {
                                        "id": "73e36439-1e9a-4925-bf2c-1d7f7885fbb0",
                                        "type": "Person",
                                        "name": "Mike Dean",
                                        "sort-name": "Dean, Mike",
                                        "disambiguation": 'US "dirty south" hip-hop producer & mix engineer',
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "6505f98c-f698-4406-8bf4-8ca43d05c36f",
                                            "attribute": "bass",
                                        },
                                        {
                                            "type-id": "b3eac5f9-7859-4416-ac39-7154e2e8d348",
                                            "attribute": "piano",
                                        },
                                    ],
                                },
                                {
                                    "type": "instrument arranger",
                                    "type-id": "4820daa1-98d6-4f8b-aa4b-6895c5b79b27",
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
                                    "target": "c56910df-7197-466c-93d3-3864758faac1",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "c56910df-7197-466c-93d3-3864758faac1",
                                        "type": "Person",
                                        "name": "DJ Frank E",
                                        "sort-name": "DJ Frank E",
                                        "disambiguation": "Justin Franks",
                                    },
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
                                    "target": "685e1d86-b9fd-4c43-ab49-308c7a166a9f",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "685e1d86-b9fd-4c43-ab49-308c7a166a9f",
                                        "type": "Person",
                                        "name": "Ryan Gilligan",
                                        "sort-name": "Gilligan, Ryan",
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
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "306c05ab-e0f2-4648-b97c-225463fa14f9",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "306c05ab-e0f2-4648-b97c-225463fa14f9",
                                        "type": "Person",
                                        "name": "Salma Kenas",
                                        "sort-name": "Kenas, Salma",
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
                                    "target": "75a72702-a5ef-4513-bca5-c5b944903546",
                                    "direction": "backward",
                                    "attribute-list": ["guest"],
                                    "artist": {
                                        "id": "75a72702-a5ef-4513-bca5-c5b944903546",
                                        "type": "Person",
                                        "name": "John Legend",
                                        "sort-name": "Legend, John",
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
                                    "target": "172805a7-6f84-4bb3-8b3b-6dc5bc33b103",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "172805a7-6f84-4bb3-8b3b-6dc5bc33b103",
                                        "type": "Person",
                                        "name": "Chris Rock",
                                        "sort-name": "Rock, Chris",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        }
                                    ],
                                },
                            ],
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "bc1581e0-ac36-3b4d-8fb4-1a5f16e404ac",
                                    "direction": "forward",
                                    "work": {
                                        "id": "bc1581e0-ac36-3b4d-8fb4-1a5f16e404ac",
                                        "title": "Blame Game",
                                        "iswc": "T-905.821.994-6",
                                        "iswc-list": [
                                            "T-905.821.994-6",
                                            "T-906.233.459-2",
                                        ],
                                        "artist-relation-list": [
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
                                                "target": "c56910df-7197-466c-93d3-3864758faac1",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "c56910df-7197-466c-93d3-3864758faac1",
                                                    "type": "Person",
                                                    "name": "DJ Frank E",
                                                    "sort-name": "DJ Frank E",
                                                    "disambiguation": "Justin Franks",
                                                },
                                                "target-credit": "Justin Franks",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "79a09151-f6cc-48f9-9907-3fdd0b68373f",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "79a09151-f6cc-48f9-9907-3fdd0b68373f",
                                                    "type": "Person",
                                                    "name": "Richard D. James",
                                                    "sort-name": "James, Richard D.",
                                                    "disambiguation": "British electronic musician",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "75a72702-a5ef-4513-bca5-c5b944903546",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "75a72702-a5ef-4513-bca5-c5b944903546",
                                                    "type": "Person",
                                                    "name": "John Legend",
                                                    "sort-name": "Legend, John",
                                                },
                                                "target-credit": "John Stephens",
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "7a61b673-fe6f-4aec-8193-7de247139f47",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "7a61b673-fe6f-4aec-8193-7de247139f47",
                                                    "type": "Person",
                                                    "name": "Khloe Mitchell",
                                                    "sort-name": "Mitchell, Khloe",
                                                },
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
                                        ],
                                    },
                                }
                            ],
                            "artist-credit-phrase": "Kanye West feat. John Legend",
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
                                    "id": "75a72702-a5ef-4513-bca5-c5b944903546",
                                    "type": "Person",
                                    "name": "John Legend",
                                    "sort-name": "Legend, John",
                                    "alias-list": [
                                        {
                                            "sort-name": "Stephens, John Roger",
                                            "type": "Legal name",
                                            "alias": "John Roger Stephens",
                                        },
                                        {
                                            "sort-name": "Stephens, John",
                                            "alias": "John Stephens",
                                        },
                                    ],
                                    "alias-count": 2,
                                }
                            },
                        ],
                        "artist-credit-phrase": "Kanye West feat. John Legend",
                        "track_or_recording_length": "471933",
                    },
                    {
                        "id": "d1b78c1f-94d9-3503-a223-2873dec1850b",
                        "position": "12",
                        "number": "12",
                        "length": "258666",
                        "recording": {
                            "id": "a7bade00-f8be-47ae-a0ab-3ce42931213a",
                            "title": "Lost in the World",
                            "length": "256586",
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
                                        "id": "437a0e49-c6ae-42f6-a6c1-84f25ed366bc",
                                        "type": "Group",
                                        "name": "Bon Iver",
                                        "sort-name": "Bon Iver",
                                    }
                                },
                            ],
                            "artist-relation-list": [
                                {
                                    "type": "engineer",
                                    "type-id": "5dcc52af-7064-4051-8d62-7d80f4c3c907",
                                    "target": "a5c6f645-c4db-4cd3-9129-a3ebe9bbabea",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "a5c6f645-c4db-4cd3-9129-a3ebe9bbabea",
                                        "type": "Person",
                                        "name": "Brent Kolatalo",
                                        "sort-name": "Kolatalo, Brent",
                                    },
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["keyboard"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        }
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
                                    "target": "35ecbbc3-3722-4255-9e42-1547c023da7f",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "35ecbbc3-3722-4255-9e42-1547c023da7f",
                                        "type": "Person",
                                        "name": "Alex Graupera",
                                        "sort-name": "Graupera, Alex",
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
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["co"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ac6f6b4c-a4ec-4483-a04e-9f425a914573",
                                            "attribute": "co",
                                        }
                                    ],
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
                                    "target": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                    "direction": "backward",
                                    "attribute-list": [
                                        "additional",
                                        "drums (drum set)",
                                    ],
                                    "artist": {
                                        "id": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                        "type": "Person",
                                        "name": "Anthony Kilhoffer",
                                        "sort-name": "Kilhoffer, Anthony",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        },
                                        {
                                            "type-id": "12092505-6ee1-46af-a15a-b5b468b6b155",
                                            "attribute": "drums (drum set)",
                                        },
                                    ],
                                },
                                {
                                    "type": "programming",
                                    "type-id": "36c50022-44e0-488d-994b-33f11d20301e",
                                    "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                    "direction": "backward",
                                    "attribute-list": ["drums (drum set)"],
                                    "artist": {
                                        "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                        "type": "Person",
                                        "name": "Ken Lewis",
                                        "sort-name": "Lewis, Ken",
                                        "disambiguation": "recording engineer and mixer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "12092505-6ee1-46af-a15a-b5b468b6b155",
                                            "attribute": "drums (drum set)",
                                        }
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
                                    "target": "9fa19223-ec32-4da2-b1a2-79ea8afeb17a",
                                    "direction": "backward",
                                    "attribute-list": ["other vocals"],
                                    "artist": {
                                        "id": "9fa19223-ec32-4da2-b1a2-79ea8afeb17a",
                                        "type": "Person",
                                        "name": "Alvin Fields",
                                        "sort-name": "Fields, Alvin",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "c359be96-620a-435c-bd25-2eb0ce81a22e",
                                            "attribute": "other vocals",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "29bbf567-4468-48e7-b96e-cc6880049db2",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "29bbf567-4468-48e7-b96e-cc6880049db2",
                                        "type": "Person",
                                        "name": "Kay Fox",
                                        "sort-name": "Fox, Kay",
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
                                    "target": "eb7fd13f-5239-4751-bc1f-665f0f1f9dd7",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "eb7fd13f-5239-4751-bc1f-665f0f1f9dd7",
                                        "type": "Person",
                                        "name": "Elly Jackson",
                                        "sort-name": "Jackson, Elly",
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
                                    "target": "8ef1df30-ae4f-4dbd-9351-1a32b208a01e",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "8ef1df30-ae4f-4dbd-9351-1a32b208a01e",
                                        "type": "Person",
                                        "name": "Alicia Keys",
                                        "sort-name": "Keys, Alicia",
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
                                    "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                    "direction": "backward",
                                    "attribute-list": ["other vocals"],
                                    "artist": {
                                        "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                        "type": "Person",
                                        "name": "Ken Lewis",
                                        "sort-name": "Lewis, Ken",
                                        "disambiguation": "recording engineer and mixer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "c359be96-620a-435c-bd25-2eb0ce81a22e",
                                            "attribute": "other vocals",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "0f1d5b01-8784-4870-9bd6-fa43178b9441",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "0f1d5b01-8784-4870-9bd6-fa43178b9441",
                                        "type": "Person",
                                        "name": "Justin Vernon",
                                        "sort-name": "Vernon, Justin",
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
                                    "target": "a42fdc0b-09bc-4a6d-8ae6-db454bf0803a",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "a42fdc0b-09bc-4a6d-8ae6-db454bf0803a",
                                        "type": "Person",
                                        "name": "Tony Williams",
                                        "sort-name": "Williams, Tony",
                                        "disambiguation": "soul/R&B singer/writer",
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
                                    "target": "b2d7c5e9-0e74-45e9-99a2-de24c19ee014",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "b2d7c5e9-0e74-45e9-99a2-de24c19ee014",
                                        "type": "Person",
                                        "name": "Charlie Wilson",
                                        "sort-name": "Wilson, Charlie",
                                        "disambiguation": "R&B singer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        }
                                    ],
                                },
                            ],
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "d35fe69e-d707-3df7-888f-cd3966d7ffde",
                                    "direction": "forward",
                                    "work": {
                                        "id": "d35fe69e-d707-3df7-888f-cd3966d7ffde",
                                        "title": "Lost in the World",
                                        "artist-relation-list": [
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
                                                "target": "20ff3303-4fe2-4a47-a1b6-291e26aa3438",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "20ff3303-4fe2-4a47-a1b6-291e26aa3438",
                                                    "type": "Person",
                                                    "name": "James Brown",
                                                    "sort-name": "Brown, James",
                                                    "disambiguation": "“The Godfather of Soul”",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "826b488f-5164-45ca-abc4-ab11b3c321eb",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "826b488f-5164-45ca-abc4-ab11b3c321eb",
                                                    "type": "Person",
                                                    "name": "Manu Dibango",
                                                    "sort-name": "Dibango, Manu",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "b5b89643-c488-4f39-a302-25cab31084a5",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "b5b89643-c488-4f39-a302-25cab31084a5",
                                                    "type": "Person",
                                                    "name": "Gil Scott‐Heron",
                                                    "sort-name": "Scott‐Heron, Gil",
                                                },
                                            },
                                            {
                                                "type": "writer",
                                                "type-id": "a255bca1-b157-4518-9108-7b147dc3fc68",
                                                "target": "0f1d5b01-8784-4870-9bd6-fa43178b9441",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "0f1d5b01-8784-4870-9bd6-fa43178b9441",
                                                    "type": "Person",
                                                    "name": "Justin Vernon",
                                                    "sort-name": "Vernon, Justin",
                                                },
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
                                        ],
                                    },
                                }
                            ],
                            "artist-credit-phrase": "Kanye West feat. Bon Iver",
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
                                    "id": "437a0e49-c6ae-42f6-a6c1-84f25ed366bc",
                                    "type": "Group",
                                    "name": "Bon Iver",
                                    "sort-name": "Bon Iver",
                                }
                            },
                        ],
                        "artist-credit-phrase": "Kanye West feat. Bon Iver",
                        "track_or_recording_length": "258666",
                    },
                    {
                        "id": "2f0f80f1-2cc5-30d3-a240-29f24abd8842",
                        "position": "13",
                        "number": "13",
                        "length": "98293",
                        "recording": {
                            "id": "db232387-83c8-4578-8a1d-b7759520ed5a",
                            "title": "Who Will Survive in America",
                            "length": "98200",
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
                                    "type": "engineer",
                                    "type-id": "5dcc52af-7064-4051-8d62-7d80f4c3c907",
                                    "target": "a5c6f645-c4db-4cd3-9129-a3ebe9bbabea",
                                    "direction": "backward",
                                    "artist": {
                                        "id": "a5c6f645-c4db-4cd3-9129-a3ebe9bbabea",
                                        "type": "Person",
                                        "name": "Brent Kolatalo",
                                        "sort-name": "Kolatalo, Brent",
                                    },
                                },
                                {
                                    "type": "instrument",
                                    "type-id": "59054b12-01ac-43ee-a618-285fd397e461",
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["keyboard"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "95b0c3d2-9606-4ef5-a019-9b7437f3adda",
                                            "attribute": "keyboard",
                                        }
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
                                    "target": "35ecbbc3-3722-4255-9e42-1547c023da7f",
                                    "direction": "backward",
                                    "attribute-list": ["assistant"],
                                    "artist": {
                                        "id": "35ecbbc3-3722-4255-9e42-1547c023da7f",
                                        "type": "Person",
                                        "name": "Alex Graupera",
                                        "sort-name": "Graupera, Alex",
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
                                    "target": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                    "direction": "backward",
                                    "attribute-list": ["co"],
                                    "artist": {
                                        "id": "a2fdc044-010f-4317-97d2-a1c67e978543",
                                        "type": "Person",
                                        "name": "Jeff Bhasker",
                                        "sort-name": "Bhasker, Jeff",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "ac6f6b4c-a4ec-4483-a04e-9f425a914573",
                                            "attribute": "co",
                                        }
                                    ],
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
                                    "target": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                    "direction": "backward",
                                    "attribute-list": [
                                        "additional",
                                        "drums (drum set)",
                                    ],
                                    "artist": {
                                        "id": "acae00f3-fbf3-440a-9e9e-5e8b75ac3b3e",
                                        "type": "Person",
                                        "name": "Anthony Kilhoffer",
                                        "sort-name": "Kilhoffer, Anthony",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        },
                                        {
                                            "type-id": "12092505-6ee1-46af-a15a-b5b468b6b155",
                                            "attribute": "drums (drum set)",
                                        },
                                    ],
                                },
                                {
                                    "type": "programming",
                                    "type-id": "36c50022-44e0-488d-994b-33f11d20301e",
                                    "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                    "direction": "backward",
                                    "attribute-list": ["drums (drum set)"],
                                    "artist": {
                                        "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                        "type": "Person",
                                        "name": "Ken Lewis",
                                        "sort-name": "Lewis, Ken",
                                        "disambiguation": "recording engineer and mixer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "12092505-6ee1-46af-a15a-b5b468b6b155",
                                            "attribute": "drums (drum set)",
                                        }
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
                                    "target": "9fa19223-ec32-4da2-b1a2-79ea8afeb17a",
                                    "direction": "backward",
                                    "attribute-list": ["other vocals"],
                                    "artist": {
                                        "id": "9fa19223-ec32-4da2-b1a2-79ea8afeb17a",
                                        "type": "Person",
                                        "name": "Alvin Fields",
                                        "sort-name": "Fields, Alvin",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "c359be96-620a-435c-bd25-2eb0ce81a22e",
                                            "attribute": "other vocals",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "29bbf567-4468-48e7-b96e-cc6880049db2",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "29bbf567-4468-48e7-b96e-cc6880049db2",
                                        "type": "Person",
                                        "name": "Kay Fox",
                                        "sort-name": "Fox, Kay",
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
                                    "target": "eb7fd13f-5239-4751-bc1f-665f0f1f9dd7",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "eb7fd13f-5239-4751-bc1f-665f0f1f9dd7",
                                        "type": "Person",
                                        "name": "Elly Jackson",
                                        "sort-name": "Jackson, Elly",
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
                                    "target": "8ef1df30-ae4f-4dbd-9351-1a32b208a01e",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "8ef1df30-ae4f-4dbd-9351-1a32b208a01e",
                                        "type": "Person",
                                        "name": "Alicia Keys",
                                        "sort-name": "Keys, Alicia",
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
                                    "target": "2bdbad13-143b-4791-99da-7a415b516af9",
                                    "direction": "backward",
                                    "attribute-list": ["other vocals"],
                                    "artist": {
                                        "id": "2bdbad13-143b-4791-99da-7a415b516af9",
                                        "type": "Person",
                                        "name": "Ken Lewis",
                                        "sort-name": "Lewis, Ken",
                                        "disambiguation": "recording engineer and mixer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "c359be96-620a-435c-bd25-2eb0ce81a22e",
                                            "attribute": "other vocals",
                                        }
                                    ],
                                },
                                {
                                    "type": "vocal",
                                    "type-id": "0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa",
                                    "target": "0f1d5b01-8784-4870-9bd6-fa43178b9441",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "0f1d5b01-8784-4870-9bd6-fa43178b9441",
                                        "type": "Person",
                                        "name": "Justin Vernon",
                                        "sort-name": "Vernon, Justin",
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
                                    "target": "a42fdc0b-09bc-4a6d-8ae6-db454bf0803a",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "a42fdc0b-09bc-4a6d-8ae6-db454bf0803a",
                                        "type": "Person",
                                        "name": "Tony Williams",
                                        "sort-name": "Williams, Tony",
                                        "disambiguation": "soul/R&B singer/writer",
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
                                    "target": "b2d7c5e9-0e74-45e9-99a2-de24c19ee014",
                                    "direction": "backward",
                                    "attribute-list": ["additional"],
                                    "artist": {
                                        "id": "b2d7c5e9-0e74-45e9-99a2-de24c19ee014",
                                        "type": "Person",
                                        "name": "Charlie Wilson",
                                        "sort-name": "Wilson, Charlie",
                                        "disambiguation": "R&B singer",
                                    },
                                    "attributes": [
                                        {
                                            "type-id": "0a5341f8-3b1d-4f99-a0c6-26b7f4e42c7f",
                                            "attribute": "additional",
                                        }
                                    ],
                                },
                            ],
                            "work-relation-list": [
                                {
                                    "type": "performance",
                                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                                    "target": "7850470c-3f86-3449-9569-eb5a1bd54c97",
                                    "direction": "forward",
                                    "work": {
                                        "id": "7850470c-3f86-3449-9569-eb5a1bd54c97",
                                        "title": "Who Will Survive in America",
                                        "artist-relation-list": [
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
                                                "target": "b5b89643-c488-4f39-a302-25cab31084a5",
                                                "direction": "backward",
                                                "artist": {
                                                    "id": "b5b89643-c488-4f39-a302-25cab31084a5",
                                                    "type": "Person",
                                                    "name": "Gil Scott‐Heron",
                                                    "sort-name": "Scott‐Heron, Gil",
                                                },
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
                        "track_or_recording_length": "98293",
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
