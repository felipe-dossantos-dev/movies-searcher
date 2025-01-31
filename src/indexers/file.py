from pathlib import Path
from typing import Dict, Set

import ujson

from src.indexers.base import Indexer
from src.words import Word


class FileIndexer(Indexer):
    def __init__(self, index_path: Path, rebuild: bool = False):
        self.index_path: Path = index_path
        self.rebuild: bool = rebuild
        self.index: Dict[Word, Set[Path]] = {}

    def build_index(self, data_dir: Path) -> None:
        if not self.rebuild and self.index_path.exists():
            with open(self.index_path, "r") as f:
                raw_index = ujson.load(f)
                self.index = {
                    Word(word): {Path(p) for p in paths}
                    for word, paths in raw_index.items()
                }
            return self.index

        for file_path in data_dir.glob("*.txt"):
            with open(file_path, "r") as f:
                content = f.read()
                words = [Word(w) for w in content.split()]
                for word in words:
                    if word not in self.index:
                        self.index[word] = set()
                    self.index[word].add(file_path)

        with open(self.index_path, "w") as f:
            serializable_index = {
                word.value: [str(p) for p in paths]
                for word, paths in self.index.items()
            }
            ujson.dump(serializable_index, f)

        return self.index

    def get_files_for_word(self, word: Word) -> Set[Path]:
        return set(self.index.get(word, set()))

    def get_all_words(self) -> Set[Word]:
        return set(self.index.keys())
