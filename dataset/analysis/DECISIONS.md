# Analysis decisions

Decisions are recorded here with their date, before the step they govern is run.

## 2026-10-29 – Main H1 scoring is full text; the 300-word cut becomes a robustness check

**Decision.** The main H1 analysis scores every text in full: chatbot answers whole, news articles whole (up to the 3,000-word corpus cap), with rarefied entropy (K = 5 frame hits drawn without replacement, at least 500 repeats, fixed seed, averaged).

**Robustness checks (not the main result):**
- topic-selected, length-matched news windows (target lengths drawn from each chatbot model's answer-length distribution)
- fixed 300 words from the start of every text
- fixed 150 words from the start of every text
- draw sizes K = 3 and K = 8
- bounds, pooled, and lexicon-variant runs (no governance frame, no ambiguous terms, with/without prompt-echo terms, no "lawsuit")

**What this replaces.** The earlier team rule "every text is cut to its first 300 words" (`MAX_WORDS` in `framescore.py`, used by notebooks 03 and 06) was the main scoring. It stays in the code and is now the "fixed 300" robustness check. `framescore.py` itself is not changed.

**Why.** A fixed cut treats the two groups unequally (it leaves Llama answers, median 224 words, untouched and trims Qwen and long articles), and the first words of a news article are not representative of the whole article. Rarefaction already controls the dependence of entropy on the number of hits, which is the part of length that matters for the estimator.

**Known limitation (to be stated next to the result).** Rarefaction fixes estimator bias, not real diversity: a longer article can genuinely cover more frames, which raises news entropy and so works against H1.

**State when written.** Lexicon v1.2, signed off 2026-10-27. `H_TESTS_ENABLED = False` in notebooks 05 and 06; no H1, H2 or H3 result file existed. This entry was written before the gates were opened.

## 2026-10-29 – "lawsuit" stays in the lexicon (v1.2 unchanged)
**Rule applied.** Add "lawsuit" to the ambiguous list (as v1.2.1) only if it does not fire in at least a handful of chatbot answers. A handful was read as 5 answers, fixed before looking at the H1 results.
**Result (full-text scoring).** It fires in 6 of 216 answers (7 hits; 2 Llama, 4 Qwen; 4 different questions; not in any prompt) and in 52 of 420 articles (122 hits). 6 is at least 5, so it stays and the lexicon stays v1.2. The count is close to the line, and the term is news-heavy, so the robustness table has a with/without-lawsuit row (`h1_lexicon_variants.csv`).

## 2026-10-29 – Housekeeping done before the gate was opened
- Corpus manifest: the lexicon hash now matches v1.2 and the stale-hash `lexicon_note` was removed.
- Codebooks: the human-review rule ("human review of automated decisions counts as rights_privacy; human oversight or human intervention as a control counts as regulation_governance") was added to `stance_codebook.md` and `validation_instructions.md`. The lexicon already agreed (`human review` in rights_privacy, `human intervention` in regulation_governance).
- Notebook 07: the gate check now passes when a gate is closed, or open with `signed_off` true in the lexicon; it fails if a gate is open or H1-H3 result files exist while the lexicon is unsigned.
- Notebook 03: test 3 (casing-fix regression) re-scores with the saved v1.1 lexicon snapshot, because the live lexicon is now v1.2.

## 2026-10-29 – Gates opened (`H_TESTS_ENABLED = True` in notebooks 05 and 06)
Full-text scoring, K = 5, 1,000 repeats, seed 42, 5,000-draw cluster bootstrap. Output tables are `h1_*.csv`, `h2_*.csv`, `h3_*.csv` in this folder.

Implementation choices not fixed in advance (stated so they can be questioned):
- "Prompt-echo terms" was run two ways: each answer loses the terms in its own prompt (chatbots only, as in notebook 03), and every term found in any prompt is dropped from both groups (symmetric). The symmetric run is the fairer between-group comparison.
- The pooled-counts interval uses the percentile bootstrap, with a bias-corrected "basic" interval added beside it because resampling 18 question clusters shifts the pooled bootstrap downward.
- H3 adds paired region-to-region JSD differences and a split-half noise floor, because overlapping per-region intervals cannot show that a chatbot is closer to one region.
- Windows: one target length per article per model; up to 3 non-overlapping windows; the window must itself pass the corpus on-topic rule; an article shorter than its target keeps all its words.
- The earlier "plain cut of each article to a target length" views in the old notebook 05 were replaced by the topic-selected windows.
