import pickle
from pathlib import Path
from typing import Dict, Set

from src.consts import (
    FILES_DATA_GLOB_PATTERN,
    NGRAM_DEFAULT_SIZE,
    NGRAM_FILE_EXTENSION,
    NGRAM_FILE_PATTERN,
)
from src.indexers.base import Indexer
from src.words import Word, phrase_to_words


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

        for file_path in data_dir.glob(FILES_DATA_GLOB_PATTERN):
            with open(file_path, "r") as f:
                content = f.read()
                words = phrase_to_words(content)
                for word in words:
                    if word not in self.index:
                        self.index[word] = set()
                    self.index[word].add(file_path)

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
            ngram_file_path.touch()
            with open(ngram_file_path, "wb") as f:
                pickle.dump(word_paths, f)

    def get_files_for_word(self, word: Word) -> Set[Path]:
        ngram = word.ngram(self.ngram_size)
        ngram_file_path = self.index_dir / f"{ngram}{NGRAM_FILE_EXTENSION}"
        if not ngram_file_path.exists():
            return set()
        with open(ngram_file_path, "rb") as f:
            words_paths = pickle.load(f)
            self.index.update(words_paths)
        return set(self.index.get(word, set()))

    def get_all_words(self) -> Set[Word]:
        for file_path in self.index_dir.glob(NGRAM_FILE_PATTERN):
            with open(file_path, "rb") as f:
                self.index.update(pickle.load(f))
        return set(self.index.keys())
