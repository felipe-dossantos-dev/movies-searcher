from abc import ABC, abstractmethod
from pathlib import Path
from typing import Set

from src.words import Word


class Indexer(ABC):
    @abstractmethod
    def build_index(self, data_dir: Path) -> None:
        """
        Builds the index from the data directory.

        Args:
            data_dir: Path to the directory containing the files
            index_dir: Path to the directory containing the indexes
        """
        pass

    @abstractmethod
    def get_files_for_word(self, word: Word) -> Set[Path]:
        """
        Returns all files that contain a specific word.

        Args:
            word: Word to be searched

        Returns:
            Set of file paths that contain the word
        """
        pass

    @abstractmethod
    def get_all_words(self) -> Set[Word]:
        """
        Returns all indexed words.

        Returns:
            Set of all words in the index
        """
        pass
