from pathlib import Path
from typing import Dict, Set

from src.consts import FILES_DEFAULT_INDEX_FILE
from src.files import process_data_dir, read_pickle_file, write_pickle_file
from src.indexers.base import Indexer
from src.words import Word


class FileIndexer(Indexer):
    def __init__(self, index_dir: Path, rebuild: bool = False):
        self.index_path: Path = index_dir / FILES_DEFAULT_INDEX_FILE
        self.rebuild: bool = rebuild
        self.index: Dict[Word, Set[Path]] = {}

    def build_index(self, data_dir: Path) -> None:
        if not self.rebuild and self.index_path.exists():
            self.index = read_pickle_file(self.index_path)
            return None

        def process_words(file_path: Path, words: Set[Word]) -> None:
            for word in words:
                if word not in self.index:
                    self.index[word] = set()
                self.index[word].add(file_path)

        process_data_dir(data_dir, process_words)
        write_pickle_file(self.index_path, self.index)

    def get_files_for_word(self, word: Word) -> Set[Path]:
        return set(self.index.get(word, set()))

    def get_all_words(self) -> Set[Word]:
        return set(self.index.keys())
