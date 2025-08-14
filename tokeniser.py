class Tokeniser:
    
    END_OF_WORD_SYMBOL = "</w>"
    
    def tokenise(self, text):
        # Lowercase the text
        text = text.lower()

        # Define punctuation characters to remove
        punctuation_chars = '.,!?;:"()'

        # Remove punctuation
        cleaned_text = ""
        for char in text:
            if char not in punctuation_chars:
                cleaned_text += char

        # Split on whitespace and return tokens
        return cleaned_text.split()
    
    def count_tokens(self, tokens):
        # Count how many times each token appears
        counts = {}
        for token in tokens:
            if token in counts:
                counts[token] += 1
            else:
                counts[token] = 1
        return counts
    
    def sort_vocab(self, token_counts):
        # Convert the dictionary into a list of (token, count) pairs
        items = list(token_counts.items())
        sorted_items = []

        # Loop through the items 
        for _ in range(len(items)):
            # Find the highest-count item remaining
            highest = items[0]
            for token, count in items:
                if count > highest[1]:
                    highest = (token, count)

            # Append highest to the sorted list
            sorted_items.append(highest)

            # Remove it from the remaining list
            items.remove(highest)

        return sorted_items
    
    def split_into_subwords(self, tokens):
        subwords = []
        for token in tokens:
            chars = list(token)
            chars.append(self.END_OF_WORD_SYMBOL)
            subwords.append(chars)
        return subwords
    
    def count_symbol_pairs(self, subword_tokens):
        """
        Count frequencies of adjacent symbol pairs across all subword tokens.
        Each subword token is a list like ["t", "h", "e", "</w>"].
        Returns a dict mapping (sym1, sym2) -> count.
        """
        pair_counts = {}

        # Go through each token (list of symbols)
        for symbols in subword_tokens:
            # Create adjacent pairs: (s0,s1), (s1,s2), ...
            
            for a, b in zip(symbols, symbols[1:]):
                pair = (a, b)
                if pair in pair_counts:
                    pair_counts[pair] += 1
                else:
                    pair_counts[pair] = 1

        return pair_counts
    
    def merge_most_frequent_pair(self, subword_tokens, pair_counts):
        """
        Find the most frequent (symbol1, symbol2) pair and merge every
        non-overlapping occurrence of that pair in each subword token.
        If multiple pairs tie for most frequent, choose the first one
        encountered when iterating over pair_counts (insertion order).
        Returns a NEW list of subword tokens with merges applied.
        """
        # If no pairs, nothing to merge
        if not pair_counts:
            return [symbols[:] for symbols in subword_tokens]

        # Find the "best" pair: highest count; ties resolved by first seen
        best_pair = None
        best_count = -1
        for pair, count in pair_counts.items():
            if count > best_count:
                best_pair = pair
                best_count = count

        a, b = best_pair  # the two symbols to merge

        merged_tokens = []
        for symbols in subword_tokens:
            i = 0
            merged = []
            # Scan left-to-right and merge non-overlapping matches
            while i < len(symbols):
                # If the next two symbols match the best pair, merge them
                if i + 1 < len(symbols) and symbols[i] == a and symbols[i + 1] == b:
                    merged.append(symbols[i] + symbols[i + 1])
                    i += 2  # skip both since they have been merged
                else:
                    merged.append(symbols[i])
                    i += 1
            merged_tokens.append(merged)

        return merged_tokens
    

t = Tokeniser()
tokens = t.tokenise("cat car caravan")
sub = t.split_into_subwords(tokens)
print (t.count_symbol_pairs(sub))