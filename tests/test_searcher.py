from pathlib import Path

import pytest


def test_search_with_spaces_only(searcher):
    results = searcher.search("   ")
    assert len(results) == 0


@pytest.mark.parametrize(
    "word,expected_count,expected_files",
    [
        ("world", 2, {"file1.txt", "file3.txt"}),
        ("universe", 1, {"file2.txt"}),
        ("nonexistent", 0, []),
    ],
)
def test_searcher(searcher, data_dir, word, expected_count, expected_files):
    files = searcher.search(word)

    assert len(files) == expected_count

    relative_paths = {p.relative_to(data_dir) for p in files}
    expected_paths = {Path(f) for f in expected_files}
    assert relative_paths == expected_paths


def test_get_available_words(searcher):
    assert set(searcher.get_available_words()) == {
        "hello",
        "world",
        "test",
        "universe",
        "testing",
        "is",
    }
