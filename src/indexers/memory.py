from pathlib import Path
from typing import Set, Dict

from src.indexers.base import Indexer
from src.words import Word

class MemoryIndexer(Indexer):
    def __init__(self):
        self.index : Dict[Word, Set[Path]] = {}
    
    def build_index(self, data_dir: Path) -> None:
        for file_path in data_dir.glob('*.txt'):
            with open(file_path, 'r') as f:
                content = f.read()
                words = [Word(w) for w in content.split()]
                for word in words:
                    if word not in self.index:
                        self.index[word] = set()
                    self.index[word].add(file_path)
        
        return self.index
    
    def get_files_for_word(self, word: Word) -> Set[Path]:
        return set(self.index.get(word, set()))
    
    def get_all_words(self) -> Set[Word]:
        return set(self.index.keys())
