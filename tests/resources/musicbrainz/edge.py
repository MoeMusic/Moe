"""Musicbrainz release containing some various edge cases."""

search = {
    "release-list": [
        {
            "id": "61e48c23-eeb7-4598-a9f0-e2a689f52040",
            "ext:score": "100",
            "title": "R.E.I.D.",
            "status": "Official",
            "text-representation": {"language": "eng", "script": "Latn"},
            "artist-credit": [
                {
                    "name": "Vataff Project",
                    "artist": {
                        "id": "47d79f4d-f334-45a3-89ab-bcd024ef8933",
                        "name": "Vataff Project",
                        "sort-name": "Vataff Project",
                    },
                }
            ],
            "release-group": {
                "id": "bff15202-da14-42b5-803b-0b4653b66ab9",
                "type": "Album",
                "title": "R.E.I.D.",
                "primary-type": "Album",
            },
            "medium-list": [
                {
                    "format": "CD",
                    "disc-list": [],
                    "disc-count": 0,
                    "track-list": [],
                    "track-count": 8,
                }
            ],
            "medium-track-count": 8,
            "medium-count": 1,
            "tag-list": [],
            "artist-credit-phrase": "Vataff Project",
        }
    ],
    "release-count": 582,
}

# date only includes the year
partial_date_year = {
    "release": {
        "id": "112dec42-65f2-3bde-8d7d-26deddde10b2",
        "title": "The Chronic",
        "status": "Official",
        "quality": "normal",
        "text-representation": {"language": "eng", "script": "Latn"},
        "artist-credit": [
            {
                "artist": {
                    "id": "5f6ab597-f57a-40da-be9e-adad48708203",
                    "type": "Person",
                    "name": "Dr. Dre",
                    "sort-name": "Dre, Dr.",
                    "disambiguation": "Andre Young, rap producer",
                }
            }
        ],
        "date": "1992",
        "country": "US",
        "release-event-list": [
            {
                "date": "1992-12-15",
                "area": {
                    "id": "489ce91b-6658-3307-9877-795b68554c98",
                    "name": "United States",
                    "sort-name": "United States",
                    "iso-3166-1-code-list": ["US"],
                },
            }
        ],
        "release-event-count": 1,
        "barcode": "049925061116",
        "asin": "B000003AEP",
        "cover-art-archive": {
            "artwork": "false",
            "count": "0",
            "front": "false",
            "back": "false",
        },
        "medium-list": [
            {
                "position": "1",
                "format": '12" Vinyl',
                "track-list": [],
                "track-count": 16,
            }
        ],
        "medium-count": 1,
        "artist-credit-phrase": "Dr. Dre",
    }
}

# date only includes year and month
partial_date_year_mon = {
    "release": {
        "id": "112dec42-65f2-3bde-8d7d-26deddde10b2",
        "title": "The Chronic",
        "status": "Official",
        "quality": "normal",
        "text-representation": {"language": "eng", "script": "Latn"},
        "artist-credit": [
            {
                "artist": {
                    "id": "5f6ab597-f57a-40da-be9e-adad48708203",
                    "type": "Person",
                    "name": "Dr. Dre",
                    "sort-name": "Dre, Dr.",
                    "disambiguation": "Andre Young, rap producer",
                }
            }
        ],
        "date": "1992-12",
        "country": "US",
        "release-event-list": [
            {
                "date": "1992-12-15",
                "area": {
                    "id": "489ce91b-6658-3307-9877-795b68554c98",
                    "name": "United States",
                    "sort-name": "United States",
                    "iso-3166-1-code-list": ["US"],
                },
            }
        ],
        "release-event-count": 1,
        "barcode": "049925061116",
        "asin": "B000003AEP",
        "cover-art-archive": {
            "artwork": "false",
            "count": "0",
            "front": "false",
            "back": "false",
        },
        "medium-list": [
            {
                "position": "1",
                "format": '12" Vinyl',
                "track-list": [],
                "track-count": 16,
            }
        ],
        "medium-count": 1,
        "artist-credit-phrase": "Dr. Dre",
    }
}
