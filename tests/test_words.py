import pytest
from src.words import Word

def test_word_should_remove_spaces():
    word = Word("  hello  world  ")
    assert word.value == "hello world"

def test_word_should_remove_accents():
    word = Word("olá mundo")
    assert word.value == "ola mundo"

def test_word_should_convert_to_lowercase():
    word = Word("Hello WORLD")
    assert word.value == "hello world"

def test_word_with_multiple_transformations():
    word = Word("  Olá  MÚNDO  ")
    assert word.value == "ola mundo"

def test_word_with_empty_string():
    word = Word("")
    assert word.value == ""
