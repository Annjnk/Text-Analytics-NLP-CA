# Lexicon v1.1 – proposed changes for review

Lexicon tag: v1.1, 2026-10-27, signed off: **False**. **Nothing in this file has been applied to `frame_keywords.json`.** No H1–H3 test has been run.

How to use: tick or strike each line, then tell the assistant to apply the approved ones as v1.2 (new changelog entries) or sign v1.1 off as it is.

## A. Terms that never fire in the chatbot answers (33 of 208)

Proposal rule: keep if it fires in news (3 or more hits); review if 1–2 news hits; drop candidate if no hits anywhere.

| frame | term | hits_news | proposal |
|---|---|---|---|
| economy_labour | labour union | 0 | drop candidate (no hits anywhere) |
| economy_labour | labor union | 0 | drop candidate (no hits anywhere) |
| misinformation_integrity | information ecosystem | 0 | drop candidate (no hits anywhere) |
| regulation_governance | harmonise | 0 | drop candidate (no hits anywhere) |
| rights_privacy | marginalise | 0 | drop candidate (no hits anywhere) |
| rights_privacy | vulnerable group | 0 | drop candidate (no hits anywhere) |
| rights_privacy | due process | 0 | drop candidate (no hits anywhere) |
| rights_privacy | right to explanation | 0 | drop candidate (no hits anywhere) |
| risk_safety | catastrophe | 0 | drop candidate (no hits anywhere) |
| economy_labour | supply chain | 39 | keep (fires in news) |
| economy_labour | chip | 14 | keep (fires in news) |
| economy_labour | export control | 12 | keep (fires in news) |
| economy_labour | labour | 4 | keep (fires in news) |
| economy_labour | semiconductor | 4 | keep (fires in news) |
| economy_labour | trade union | 3 | keep (fires in news) |
| innovation_opportunity | unlock | 20 | keep (fires in news) |
| innovation_opportunity | pioneer | 9 | keep (fires in news) |
| innovation_opportunity | invent | 5 | keep (fires in news) |
| innovation_opportunity | invention | 3 | keep (fires in news) |
| misinformation_integrity | scam | 6 | keep (fires in news) |
| regulation_governance | lawmaker | 19 | keep (fires in news) |
| regulation_governance | sanction | 13 | keep (fires in news) |
| regulation_governance | certification | 4 | keep (fires in news) |
| regulation_governance | statute | 3 | keep (fires in news) |
| rights_privacy | copyright | 78 | keep (fires in news) |
| rights_privacy | civil right | 4 | keep (fires in news) |
| economy_labour | tariff | 2 | review (1-2 news hits) |
| economy_labour | gdp | 1 | review (1-2 news hits) |
| misinformation_integrity | impersonation | 1 | review (1-2 news hits) |
| regulation_governance | legislature | 2 | review (1-2 news hits) |
| rights_privacy | equality | 1 | review (1-2 news hits) |
| rights_privacy | anonymise | 1 | review (1-2 news hits) |
| rights_privacy | child safety | 1 | review (1-2 news hits) |

## B. Candidate missing terms found by reading 60 low-hit news chunks

Read by the AI assistant (all 24 chunks with 0–1 hits plus 36 with 2–4 hits, 15 per region). Counts are chunks/answers containing the term. Not exhaustive; to be confirmed by a human reader.

| term | proposed_frame | news_chunks_with_term | answers_with_term | caution |
|---|---|---|---|---|
| guardrail | risk_safety | 18 | 8 |  |
| parental control | risk_safety | 2 | 0 | child-safety group; 'child' and 'child safety' are already in rights_privacy |
| teenager | risk_safety | 3 | 0 | ambiguous topic word; consider with 'child' as one group |
| suicide | risk_safety | 16 | 0 | sensitive harm term; very rare in regulation framing |
| violent | risk_safety | 4 | 1 |  |
| explicit content | risk_safety | 2 | 0 | article is about sexualised chatbot content |
| hate speech | risk_safety | 3 | 0 | harmful-content topic |
| antisemitic | risk_safety | 3 | 0 | topic word; spelling variants (anti-Semitic) need lemma check |
| superintelligence | risk_safety | 2 | 1 |  |
| rogue | risk_safety | 1 | 0 | headline word; check frequency before adding |
| autonomous | risk_safety | 41 | 35 | also appears in product news (news_0082): ambiguous |
| attacker | risk_safety | 13 | 1 |  |
| lawsuit | regulation_governance | 26 | 6 | legal enforcement; check overlap with litigation |
| court | regulation_governance | 34 | 4 | very general word |
| legislative | regulation_governance | 7 | 6 | the lexicon has legislation / legislate / legislature but not this form |
| oversee | regulation_governance | 6 | 14 | the lexicon has oversight but not the verb |
| human intervention | regulation_governance | 7 | 3 | human-oversight idea; 'human oversight' and 'human in the loop' also candidates |
| restriction | regulation_governance | 15 | 30 | ambiguous: 'ban' and 'prohibit' too general |
| anonymity | rights_privacy | 3 | 4 |  |
| censorship | rights_privacy | 1 | 2 | free-expression topic; 'content filter' is a candidate too |
| private data | rights_privacy | 2 | 1 | phrase; 'personal data' is already in the lexicon |
| patent | rights_privacy | 3 | 0 | intellectual property; or innovation? needs a decision |
| acquisition | economy_labour | 5 | 1 | corporate news, not regulation framing |
| valuation | economy_labour | 6 | 0 | corporate news, not regulation framing |
| plagiarism | misinformation_integrity | 1 | 0 | academic integrity; 'cheating' and 'academic dishonesty' also candidates |
| academic dishonesty | misinformation_integrity | 1 | 0 |  |
| inaccurate | misinformation_integrity | 3 | 3 | also 'incorrect', 'accuracy'; overlaps hallucination |
| problematic | misinformation_integrity | 2 | 14 | very general word |
| echo chamber | misinformation_integrity | 2 | 1 | this example is newsletter boilerplate, not article text: low value |
| news ecosystem | misinformation_integrity | 1 | 0 | the lexicon has 'information ecosystem' |
| sycophancy | risk_safety | 3 | 0 | or misinformation_integrity; needs a decision |
| political bias | misinformation_integrity | 1 | 0 | 'bias' alone was removed in v1.1 (second meaning); phrases 'political bias', 'algorithmic bias', 'implicit bias' could be tested. Do NOT add 'woke' (stance-laden) |

Observations: most 0–1 hit chunks are consumer-tech pieces, essays or school stories, not regulation coverage; the missing-term list is short and most candidates fire in only a few chunks. Corpus-quality counts below.

## C. Corpus quality seen while reading (affects frame density, not the lexicon)

| issue | chunks_affected | share |
|---|---|---|
| subscription / sign-up / membership boilerplate | 15 | 0.036 |
| leftover HTML tags | 1 | 0.002 |
| garbled characters (mojibake) | 3 | 0.007 |
| dateline / share-widget text | 11 | 0.026 |
| corpus articles that still satisfy the on-topic rule within their first 300 words | 157 | 0.374 |
| articles passing the regulation test only thanks to the ambiguous words (law, bill, ban, rule, policy) in the FULL text | 161 | 0.383 |

## D. Existing terms to reconsider

Weak or prompt-linked terms (counts from chatbot answers and news):

| term | frame | on_ambiguous_list | hits_chatbot | hits_news | chatbot_hits_in_prompt_echo |
|---|---|---|---|---|---|
| transform | innovation_opportunity | False | 2 | 39 | 0 |
| creative | innovation_opportunity | False | 9 | 19 | 0 |
| experiment | innovation_opportunity | False | 6 | 23 | 0 |
| unlock | innovation_opportunity | False | 0 | 20 | 0 |
| dominate | economy_labour | False | 14 | 6 | 12 |
| dominance | economy_labour | False | 13 | 6 | 0 |
| progress | innovation_opportunity | True | 79 | 13 | 0 |
| potential | innovation_opportunity | True | 161 | 72 | 0 |
| benefit | innovation_opportunity | True | 109 | 31 | 0 |

Prompt-echo terms (at least 15 chatbot hits, at least 40% of them in answers whose prompt contains the term):

| frame | term | hits_chatbot | echo_share |
|---|---|---|---|
| innovation_opportunity | start up | 42 | 1.0 |
| rights_privacy | human review | 38 | 1.0 |
| rights_privacy | personal datum | 34 | 0.97 |
| economy_labour | worker | 36 | 0.94 |
| rights_privacy | facial recognition | 50 | 0.9 |
| regulation_governance | approval | 54 | 0.83 |
| misinformation_integrity | false | 57 | 0.65 |
| risk_safety | high stake | 28 | 0.5 |
| regulation_governance | regulator | 70 | 0.46 |
| economy_labour | market | 87 | 0.41 |

## E. On-topic rule (corpus is frozen; this concerns limitations and any future version)

- The rule was applied to the full text but frames are scored on the first 300 words: see the share of articles that still satisfy the rule within the head (section C).
- 988 usable articles were rejected for having AI words but fewer than 2 regulation words. 30 are in `data/review_ai_not_regulation.md` with the question to answer (is the regulation word list too narrow?).
- Some regulation words (law, bill, ban, rule, policy) are everyday words; section C counts articles that pass only through them.
