from pathlib import Path
from typing import Dict, Set

from src.consts import (
    NGRAM_DEFAULT_SIZE,
    NGRAM_FILE_EXTENSION,
    NGRAM_FILE_PATTERN,
)
from src.files import process_data_dir, read_pickle_file, write_pickle_file
from src.indexers.base import Indexer
from src.words import Word


class NGramIndexer(Indexer):
    def __init__(
        self,
        index_dir: Path,
        rebuild: bool = False,
        ngram_size: int = NGRAM_DEFAULT_SIZE,
    ):
        self.index_dir: Path = index_dir
        self.rebuild: bool = rebuild
        self.ngram_size: int = ngram_size
        self.ngram_index: Dict[str, Dict[Word, Set[Path]]] = {}
        self.index: Dict[Word, Set[Path]] = {}

    def build_index(self, data_dir: Path) -> None:
        if not self.index_dir.exists():
            self.index_dir.mkdir()

        if not self.rebuild:
            return

        def process_file(file_path: Path, words: Set[Word]) -> None:
            for word in words:
                if word not in self.index:
                    self.index[word] = set()
                self.index[word].add(file_path)

        process_data_dir(data_dir, process_file)

        for word, paths in self.index.items():
            ngram = word.ngram(self.ngram_size)
            if ngram not in self.ngram_index:
                self.ngram_index[ngram] = {word: paths}
            elif word not in self.ngram_index[ngram]:
                self.ngram_index[ngram][word] = paths
            else:
                self.ngram_index[ngram][word].add(paths)

        for ngram, word_paths in self.ngram_index.items():
            ngram_file_path = self.index_dir / f"{ngram}{NGRAM_FILE_EXTENSION}"
            write_pickle_file(ngram_file_path, word_paths)

    def get_files_for_word(self, word: Word) -> Set[Path]:
        ngram = word.ngram(self.ngram_size)
        ngram_file_path = self.index_dir / f"{ngram}{NGRAM_FILE_EXTENSION}"
        if not ngram_file_path.exists():
            return set()
        words_paths = read_pickle_file(ngram_file_path)
        self.index.update(words_paths)
        return set(self.index.get(word, set()))

    def get_all_words(self) -> Set[Word]:
        for file_path in self.index_dir.glob(NGRAM_FILE_PATTERN):
            self.index.update(read_pickle_file(file_path))
        return set(self.index.keys())
