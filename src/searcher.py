from pathlib import Path
from typing import List

from src.indexers import Indexer
from src.words import phrase_to_words


class Searcher:
    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    def search(self, query: str) -> List[Path]:
        search_words = phrase_to_words(query)

        if not search_words:
            return []

        first_word = next(iter(search_words))
        matching_files = self.indexer.get_files_for_word(first_word)

        for word in search_words:
            files_with_word = self.indexer.get_files_for_word(word)
            matching_files = matching_files.intersection(files_with_word)

            if not matching_files:
                return []

        return sorted(list(matching_files))

    def get_available_words(self) -> List[str]:
        return [word.value for word in self.indexer.get_all_words()]
