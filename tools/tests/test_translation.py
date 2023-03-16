"""
Test the translation
"""

from pyfolio import translator


def test_merging_objects():
    """
    Test to merge objects
    """
    dest = {
        "a": {
            "a": {
                "a": 1,
                "b": 2,
                "c": 3,
            },
            "b": {
                "e": 4,
                "f": 5,
                "g": 6,
            },
        },
        "arr": ["a", "b"],
        "arr2": [
            {"a": "A", "b": 2},
            {"a": "AA", "b": 3},
            {"a": "AAA", "b": 4},
        ],
    }
    source = {
        "a": {
            "a": {
                "a": 4,
            }
        },
        "arr": ["A", "B", "C"],
        "arr2": [
            {"_a": "A", "c": "Hey"},
            {"_a": "AAAA", "b": 5},
            {"a": "AAAAA", "b": 6},
        ],
    }
    translator.merge_objects(source, dest)
    assert dest == {
        "a": {
            "a": {
                "a": 4,
                "b": 2,
                "c": 3,
            },
            "b": {
                "e": 4,
                "f": 5,
                "g": 6,
            },
        },
        "arr": ["A", "B", "C"],
        "arr2": [
            {"a": "A", "b": 2, "c": "Hey"},
            {"_a": "AAAA", "b": 5},
            {"a": "AAAAA", "b": 6},
        ],
    }
