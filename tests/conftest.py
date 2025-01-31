import pytest

from src.indexers import FileIndexer, Indexer, MemoryIndexer
from src.searcher import Searcher


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


@pytest.fixture(params=[MemoryIndexer, FileIndexer])
def indexer_obj(request, data_dir, tmp_path) -> Indexer:
    index_path = tmp_path / "index.json"
    indexer_class = request.param
    if indexer_class is MemoryIndexer:
        indexer = indexer_class()
    if indexer_class is FileIndexer:
        indexer = indexer_class(index_path, True)
    indexer.build_index(data_dir)
    return indexer


@pytest.fixture
def searcher(indexer_obj) -> Searcher:
    return Searcher(indexer_obj)
