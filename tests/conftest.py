import pytest
from src.searcher import MovieSearcher
from src.indexers import Indexer, MemoryIndexer

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

@pytest.fixture
def searcher(indexer_obj) -> MovieSearcher:
    return MovieSearcher(indexer_obj)