import pickle
from pathlib import Path
from typing import Any, Callable, Set

from src.consts import FILES_DATA_GLOB_PATTERN
from src.words import Word, phrase_to_words


def read_pickle_file(file_path: Path) -> Any:
    with open(file_path, "rb") as f:
        return pickle.load(f)


def write_pickle_file(file_path: Path, data: Any) -> None:
    file_path.touch()
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


def read_text_file(file_path: Path) -> str:
    with open(file_path, "r") as f:
        return f.read()


def process_data_dir(
    data_dir: Path, callback: Callable[[Path, Set[Word]], None]
) -> None:
    for file_path in data_dir.glob(FILES_DATA_GLOB_PATTERN):
        content = read_text_file(file_path)
        words = phrase_to_words(content)
        callback(file_path, words)
