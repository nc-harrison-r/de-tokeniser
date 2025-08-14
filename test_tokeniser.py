from tokeniser import Tokeniser

# --- Test tokenise --- #

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



# --- Test count_tokens --- #

def test_count_tokens_empty_list():
    t = Tokeniser()
    assert t.count_tokens([]) == {}

def test_count_tokens_single_token():
    t = Tokeniser()
    assert t.count_tokens(["apple"]) == {"apple": 1}

def test_count_tokens_two_distinct_tokens():
    t = Tokeniser()
    assert t.count_tokens(["apple", "banana"]) == {"apple": 1, "banana": 1}

def test_count_tokens_with_one_repeat():
    t = Tokeniser()
    assert t.count_tokens(["apple", "banana", "apple"]) == {"apple": 2, "banana": 1}

def test_count_tokens_basic_example():
    t = Tokeniser()
    tokens = ["the", "cat", "in", "the", "hat"]
    expected = {"the": 2, "cat": 1, "in": 1, "hat": 1}
    assert t.count_tokens(tokens) == expected

def test_count_tokens_from_short_sentence_via_tokenise():
    t = Tokeniser()
    tokens = t.tokenise("Hello, hello world!")
    # after normalisation: ["hello", "hello", "world"]
    assert t.count_tokens(tokens) == {"hello": 2, "world": 1}

def test_count_tokens_from_longer_sentence_via_tokenise():
    t = Tokeniser()
    text = "The world says hello to the world."
    tokens = t.tokenise(text)
    assert tokens == ["the", "world", "says", "hello", "to", "the", "world"]
    assert t.count_tokens(tokens) == {
        "the": 2, "world": 2, "says": 1, "hello": 1, "to": 1
    }

# --- Test sort_vocab --- #

def test_sort_vocab_single_entry():
    t = Tokeniser()
    counts = {"apple": 1}
    assert t.sort_vocab(counts) == [("apple", 1)]

def test_sort_vocab_multiple_entries():
    t = Tokeniser()
    counts = {"the": 2, "cat": 1, "in": 1, "hat": 1}
    expected = [("the", 2), ("cat", 1), ("in", 1), ("hat", 1)]
    assert t.sort_vocab(counts) == expected

def test_sort_vocab_from_count_tokens():
    t = Tokeniser()
    tokens = t.tokenise("The world says hello to the world.")
    counts = t.count_tokens(tokens)
    sorted_vocab = t.sort_vocab(counts)
    # First entry should be one of the top counts (the or world)
    assert sorted_vocab[0][1] >= sorted_vocab[1][1]

# --- Test split_into_subwords --- #

def test_end_of_word_symbol_exists():
    assert Tokeniser.END_OF_WORD_SYMBOL == "</w>"

def test_split_into_subwords_single_token():
    t = Tokeniser()
    result = t.split_into_subwords(["cat"])
    assert result == [["c", "a", "t", Tokeniser.END_OF_WORD_SYMBOL]]

def test_split_into_subwords_multiple_tokens():
    t = Tokeniser()
    tokens = t.tokenise("The hat")
    expected = [
        ["t", "h", "e", Tokeniser.END_OF_WORD_SYMBOL],
        ["h", "a", "t", Tokeniser.END_OF_WORD_SYMBOL]
    ]
    assert t.split_into_subwords(tokens) == expected

def test_split_into_subwords_empty_token_list():
    t = Tokeniser()
    assert t.split_into_subwords([]) == []

def test_split_into_subwords_handles_single_letter_words():
    t = Tokeniser()
    tokens = t.tokenise("a I")
    expected = [
        ["a", Tokeniser.END_OF_WORD_SYMBOL],
        ["i", Tokeniser.END_OF_WORD_SYMBOL]  # lowercase if tokenise used first
    ]
    assert t.split_into_subwords(tokens) == expected

# --- Test count_symbol_pairs --- #

def test_count_symbol_pairs_empty_input():
    t = Tokeniser()
    assert t.count_symbol_pairs([]) == {}

def test_count_symbol_pairs_single_word_single_pair():
    t = Tokeniser()
    sub = [["a", "</w>"]]
    # pairs: ("a", "</w>")
    assert t.count_symbol_pairs(sub) == {("a", "</w>"): 1}

def test_count_symbol_pairs_single_token_multiple_pairs():
    t = Tokeniser()
    sub = [["c", "a", "t", "</w>"]]
    # pairs: ("c","a"), ("a","t"), ("t","</w>")
    expected = {("c", "a"): 1, ("a", "t"): 1, ("t", "</w>"): 1}
    assert t.count_symbol_pairs(sub) == expected

def test_count_symbol_pairs_from_pipeline_example():
    t = Tokeniser()
    tokens = t.tokenise("the hat")
    sub = t.split_into_subwords(tokens)
    result = t.count_symbol_pairs(sub)
    expected_pairs = {
        ("t", "h"): 1,
        ("h", "e"): 1,
        ("e", "</w>"): 1,
        ("h", "a"): 1,
        ("a", "t"): 1,
        ("t", "</w>"): 1
    }
    assert result == expected_pairs

def test_count_symbol_pairs_two_tokens_accumulate_counts():
    t = Tokeniser()
    sub = [
        ["c", "a", "t", "</w>"],
        ["c", "a", "r", "</w>"]
    ]
    result = t.count_symbol_pairs(sub)
    # shared ("c","a") appears twice
    assert result[("c", "a")] == 2
    assert result[("a", "t")] == 1
    assert result[("a", "r")] == 1
    assert result[("t", "</w>")] == 1
    assert result[("r", "</w>")] == 1

def test_count_symbol_pairs_two_tokens_accumulate_counts():
    t = Tokeniser()
    
    tokens = t.tokenise("cat car caravan")
    sub = t.split_into_subwords(tokens)
    # subwords: [
    # ["c", "a", "t", "</w>"],
    # ["c", "a", "r", "</w>"], 
    # ["c", "a", "r", "a", "v", "a", "n", "</w>"]]

    result = t.count_symbol_pairs(sub)
    expected = {('c', 'a'): 3, 
                ('a', 't'): 1,
                ('t', '</w>'): 1, 
                ('a', 'r'): 2, 
                ('r', '</w>'): 1, 
                ('r', 'a'): 1, 
                ('a', 'v'): 1, 
                ('v', 'a'): 1, 
                ('a', 'n'): 1, 
                ('n', '</w>'): 1}
    assert result == expected