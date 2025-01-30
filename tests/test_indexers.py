from typing import Type
import pytest
from pathlib import Path

from src.indexers import MemoryIndexer, Indexer
from src.words import Word


@pytest.fixture
def data_dir(tmp_path):
    test_files = {
        "file1.txt": "hello world test",
        "file2.txt": "hello universe testing",
        "file3.txt": "world is testing",
    }

    for filename, content in test_files.items():
        file_path = tmp_path / filename
        file_path.write_text(content)

    return tmp_path


@pytest.fixture(params=[MemoryIndexer])
def indexer_obj(request, data_dir) -> Indexer:
    indexer_class = request.param
    indexer = indexer_class()
    indexer.build_index(data_dir)
    return indexer


def test_build_index(indexer_obj: Indexer):
    """Test if all words are correctly indexed."""
    all_words = indexer_obj.get_all_words()
    expected_words = {
        Word("hello"),
        Word("world"),
        Word("test"),
        Word("universe"),
        Word("testing"),
        Word("is"),
    }
    assert all_words == expected_words


@pytest.mark.parametrize(
    "word,expected_count,expected_files",
    [
        ("world", 2, {"file1.txt", "file3.txt"}),
        ("universe", 1, {"file2.txt"}),
        ("nonexistent", 0, []),
    ],
)
def test_get_files_for_word(
    indexer_obj, data_dir, word, expected_count, expected_files
):
    files = indexer_obj.get_files_for_word(Word(word))

    assert len(files) == expected_count

    relative_paths = {p.relative_to(data_dir) for p in files}
    expected_paths = {Path(f) for f in expected_files}
    assert relative_paths == expected_paths


def test_get_all_words(indexer_obj):
    assert indexer_obj.get_all_words() == {
        Word("hello"),
        Word("world"),
        Word("test"),
        Word("universe"),
        Word("testing"),
        Word("is"),
    }


def test_empty_directory(tmp_path):
    """Test indexing an empty directory."""
    indexer = MemoryIndexer()
    indexer.build_index(tmp_path)

    assert len(indexer.get_all_words()) == 0


def test_file_with_no_words(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    indexer = MemoryIndexer()
    indexer.build_index(tmp_path)

    assert len(indexer.get_all_words()) == 0
