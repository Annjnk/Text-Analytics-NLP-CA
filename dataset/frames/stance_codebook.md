# Stance codebook

**Unit:** one text (the first 300 words of an answer or article).
**Question:** what is the text's position on **government regulation of AI** (or on the specific rule or measure it discusses)?

| label | use it when | invented example (not from the data) |
|---|---|---|
| for | the text favours rules, oversight or restrictions, or argues they are needed | "Strong rules are needed because unchecked AI systems can harm people, and companies will not police themselves." |
| against | the text opposes rules or argues they would do more harm than good | "Heavy-handed AI rules would stifle innovation and push companies and talent to countries with lighter regulation." |
| mixed | the text weighs both sides, or reports both sides without favouring one, or supports some rules and opposes others | "Rules could protect people from harm, but if they are too strict they risk slowing down small companies; the details matter." |
| none | no position on regulation, or the text is not about regulation | "The company unveiled a new AI assistant with a faster model and a longer battery life." |

**Rules**
1. Label the text's own position, not the topic. A text about a ban is not "for" the ban unless it endorses it.
2. A quoted opinion counts only if the text clearly adopts it. A report that quotes one supporter and one critic is `mixed`.
3. Descriptive reporting of a new law with no evaluation is `none`.
4. If a text argues one side but admits a drawback in a sentence, label the side it argues (`for` or `against`), not `mixed`.
5. Chatbot answers to "why is it a good idea" or "why is it a bad idea" prompts often argue one side: label what the text says, not what the prompt asked.
6. If unsure between a side and `mixed`, choose `mixed`; if unsure between `mixed` and `none`, choose `none` only when regulation is not discussed.
7. Label alone. Compare after both labellers have finished.

**Agreement:** the 20 shared texts give Cohen's kappa (all four labels, and the three labels for / against / mixed). Disputed shared texts are discussed and given one consensus label.

**Content note.** Some texts discuss suicide, sexual content in the context of chatbot safety, and hate speech. You may skip any text that distresses you: write `skip` in the label column (the scoring scripts treat it as missing and report how many were skipped) and tell the others.
