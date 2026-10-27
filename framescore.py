"""Frame scorer shared by every notebook (one scorer, so results cannot drift apart).

Method: lower-case the text, turn hyphens into spaces, lemmatise with spaCy, match the lexicon as lemma phrases with
PhraseMatcher, longest match wins. Lower-casing matters: spaCy keeps capitals in the lemmas of proper nouns ("EU",
"Congress", and sometimes a sentence-initial "Transparency"), so a lower-case pattern would never match them.
"""
import json
import re
from collections import Counter

import numpy as np
import spacy
from spacy.matcher import PhraseMatcher
from spacy.util import filter_spans

MAX_WORDS = 300       # team rule: every text is cut to its first 300 words
MIN_HITS = 5          # minimum hits for a plain (non-rarefied) entropy score

nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])


def norm(text):
    """start-up -> start up, fact-check -> fact check, and lower-case. The one text path for scorer and patterns."""
    return re.sub(r"(?<=\w)[-‐-–](?=\w)", " ", text).lower()


def lem(term):
    return " ".join(t.lemma_.lower() for t in nlp(norm(term)))


def cut(text, n=MAX_WORDS):
    return " ".join(text.split()[:n])


def _build(section):
    matcher, owner = PhraseMatcher(nlp.vocab, attr="LEMMA"), {}
    for frame, terms in section.items():
        for t in dict.fromkeys(lem(t) for t in terms):           # lemma form, duplicates removed
            owner[t] = frame
            matcher.add(frame + "||" + t, [nlp(norm(t))])
    return matcher, owner


build_matcher = _build       # public name: build a matcher for {frame: [terms]} (used to test candidate terms without touching the lexicon)


class Lexicon:
    def __init__(self, path):
        self.raw = json.load(open(path))
        self.version = self.raw["version"]
        self.frames = list(self.raw["frames"])
        self.matcher, self.owner = _build(self.raw["frames"])
        self.ambiguous = {lem(t) for t in self.raw["ambiguous_terms"]}
        self.jur_matcher, self.jur_owner = _build({"jurisdiction": self.raw["jurisdiction_terms"]["terms"]})
        dup = [t for t, c in Counter(lem(t) for ts in self.raw["frames"].values() for t in set(ts)).items() if c > 1]
        assert not dup, f"terms in more than one frame: {dup}"


def find_hits(texts, matcher, owner):
    """Per text: list of (frame, matched lemma phrase). Longest match wins, so a phrase and its parts never double count."""
    out = []
    for doc in nlp.pipe([norm(t) for t in texts], batch_size=64):
        spans = filter_spans([doc[s:e] for _, s, e in matcher(doc)])
        out.append([(owner[l], l) for l in (" ".join(t.lemma_.lower() for t in sp) for sp in spans)])
    return out


def count_vector(hit_list, frames, drop=frozenset()):
    return [sum(1 for f, l in hit_list if f == fr and l not in drop) for fr in frames]


def entropy(c, min_hits=MIN_HITS):
    """Normalised Shannon entropy (0 = all hits in one frame, 1 = perfectly even). NaN below min_hits."""
    c = np.asarray(c, float)
    if c.sum() < min_hits:
        return np.nan
    p = c[c > 0] / c.sum()
    return float(-(p * np.log(p)).sum() / np.log(len(c)))


def rarefied_entropy(c, k, rng, reps=500):
    """Mean normalised entropy of `reps` random draws of k hits (without replacement) from the count vector c.
    Fixes the plug-in estimator's dependence on the number of hits. NaN if the text has fewer than k hits."""
    c = np.asarray(c, int)
    if c.sum() < k:
        return np.nan
    draws = rng.multivariate_hypergeometric(c, k, size=reps)
    p = draws / k
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -np.nansum(np.where(p > 0, p * np.log(p), 0.0), axis=1) / np.log(len(c))
    return float(h.mean())
