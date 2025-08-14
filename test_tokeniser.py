from tokeniser import Tokeniser

def test_simple_words_are_split():
    t = Tokeniser()
    assert t.tokenise("hello world") == ["hello", "world"]

def test_lowercasing():
    t = Tokeniser()
    assert t.tokenise("Hello WORLD") == ["hello", "world"]

def test_strip_punctuation_basic():
    t = Tokeniser()
    assert t.tokenise("hello, world!") == ["hello", "world"]

def test_strip_parentheses_quotes_and_colons():
    t = Tokeniser()
    assert t.tokenise('He said: "Hello (world)!"') == ["he", "said", "hello", "world"]

def test_extra_spaces_are_ignored():
    t = Tokeniser()
    assert t.tokenise("  the   world   ") == ["the", "world"]

def test_example_from_brief():
    t = Tokeniser()
    assert t.tokenise("The world says hello to the world.") == \
           ["the", "world", "says", "hello", "to", "the", "world"]

def test_empty_string_gives_empty_list():
    t = Tokeniser()
    assert t.tokenise("") == []