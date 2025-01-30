from src.words import Word, phrase_to_words

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

def test_word_with_punctuation():
    word = Word("  !! . ")
    assert word == word.empty()

def test_word_with_empty_string():
    word = Word("")
    assert word.value == ""

def test_phrase_to_words_with_simple_phrase():
    words = phrase_to_words("hello world")
    assert words == {Word("hello"), Word("world")}

def test_phrase_to_words_with_accents_and_spaces():
    words = phrase_to_words("  Olá  MÚNDO  ")
    assert words == {Word("ola"), Word("mundo")}

def test_empty_word_in_set():
    words = {Word.empty(), Word("hello"), Word.empty()}
    assert len(words) == 2
    assert Word.empty() in words

def test_phrase_to_words_returns_empty_set_for_invalid_words():
    assert phrase_to_words("") == set()
    assert phrase_to_words("   ") == set()
    assert phrase_to_words("!@#$") == set()

def test_empty_word_equality_and_singleton():
    empty1 = Word.empty()
    empty2 = Word.empty()
    normal_word = Word("hello")
    
    assert empty1 == empty2
    assert empty1 != normal_word
    assert hash(empty1) == hash(empty2)

def test_phrase_to_words_with_some_invalid_words():
    words = phrase_to_words("hello !@#$ world")
    assert words == {Word("hello"), Word("world")}
