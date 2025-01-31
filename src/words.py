import re
import unicodedata
from dataclasses import dataclass
from typing import Set


@dataclass()
class Word:
    value: str

    _empty_instance = None

    def __post_init__(self):
        self.value = self.value.strip().lower()

        self.value = (
            unicodedata.normalize("NFKD", self.value)
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )

        self.value = re.sub(r"[^\w\s]", "", self.value)
        self.value = re.sub(r"\s+", " ", self.value)

        if not self.value or self.value.isspace():
            self.value = ""

    @classmethod
    def empty(cls) -> "Word":
        if cls._empty_instance is None:
            cls._empty_instance = cls("")
        return cls._empty_instance

    def is_empty(self) -> bool:
        return self.value == ""

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Word):
            return NotImplemented
        return self.value == other.value

    def __repr__(self) -> str:
        return f"Word('{self.value}')"


def phrase_to_words(phrase: str) -> Set[Word]:
    if not phrase or phrase.isspace():
        return set()

    words = phrase.split()
    words = {Word(word) for word in words}
    words.discard(Word.empty())
    return words
