import re
import os
from collections import Counter

WORD_RE = re.compile(r"[a-z]+")

def words(text: str):
    return WORD_RE.findall(text.lower())

class NorvigCorrector:
    def __init__(self, corpus_path: str):
        if not os.path.isfile(corpus_path):
            raise FileNotFoundError(f"NorvigCorrector: cannot find corpus at '{corpus_path}'")
        text = open(corpus_path, "r", encoding="utf-8", errors="ignore").read()
        self.WORDS = Counter(words(text))
        self.N = sum(self.WORDS.values())

    def probability(self, w: str) -> float:
        return self.WORDS[w] / self.N if self.N > 0 else 0

    def correction(self, token: str) -> str:
        token_low = token.lower()
        if token_low in self.WORDS:
            return token
        candidates = self._candidates(token_low)
        best = max(candidates, key=self.probability)
        return best

    def _candidates(self, word: str):
        return (
            self._known([word]) or
            self._known(self._edits1(word)) or
            self._known(self._edits2(word)) or
            {word}
        )

    def _known(self, words_set):
        return set(w for w in words_set if w in self.WORDS)

    def _edits1(self, word: str):
        letters    = "abcdefghijklmnopqrstuvwxyz"
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [L + R[1:] for (L, R) in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for (L, R) in splits if len(R) > 1]
        replaces   = [L + c + R[1:] for (L, R) in splits if R for c in letters]
        inserts    = [L + c + R       for (L, R) in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def _edits2(self, word: str):
        return set(e2 for e1 in self._edits1(word) for e2 in self._edits1(e1))

def correct_query(raw_query: str, corrector: NorvigCorrector):
    path_part    = ""
    content_part = ""
    tokens = raw_query.strip().split()

    for token in tokens:
        low = token.lower()
        if low.startswith("path:"):
            path_part = token[len("path:"):]
        elif low.startswith("content:"):
            content_part += token[len("content:"):] + " "
        else:
            if content_part != "":
                content_part += token + " "
            else:
                content_part += token + " "

    content_part = content_part.strip()
    raw_terms = content_part.split()
    corrected_terms = []
    corrections = []

    for term in raw_terms:
        suggestion = corrector.correction(term)
        if suggestion.lower() != term.lower():
            corrections.append((term, suggestion))
        corrected_terms.append(suggestion)

    parts = []
    if path_part:
        parts.append(f"path:{path_part}")
    if corrected_terms:
        parts.append("content:" + " ".join(corrected_terms))

    corrected_query = " ".join(parts).strip()
    return corrected_query, corrections
