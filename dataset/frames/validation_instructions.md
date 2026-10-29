# Validation sheet: how to label

For each text choose the ONE frame it emphasises most (what most of the text is about), or `none`.
Read the text, do not search for keywords. Use only the text in the sheet. Fill in the `human_frame` column with the exact frame name.

| frame | choose it when the text mainly talks about |
|---|---|
| innovation_opportunity | benefits, breakthroughs, progress, new products, opportunity, startups |
| risk_safety | harms, dangers, accidents, misuse, safety testing, threats, children harmed |
| regulation_governance | regulators, oversight, enforcement, compliance, treaties, standards, legal responsibility, institutions |
| rights_privacy | privacy, personal data, surveillance, discrimination, civil liberties, copyright |
| economy_labour | jobs, workers, automation, markets, competition between firms or countries, costs, trade |
| misinformation_integrity | false information, deepfakes, hallucinations, manipulation, election integrity, authenticity |
| none | none of these clearly dominates (for example a product review or a personal essay) |

Rules: one label per text; if two frames seem equal choose the one that appears first in the text; do not look at the key file until everyone has finished.

**Human review vs human oversight.** A person checking a machine: human review of automated decisions counts as rights_privacy; human oversight or human intervention as a control counts as regulation_governance. (Example: "people should have the right to a human review of an AI decision" is rights_privacy; "a human must be able to intervene and switch the system off" is regulation_governance.)

**How the 50 texts were chosen.** 25 chatbot answers (13 Llama, 12 Qwen) and 25 news articles (7 US, 6 UK, 6 EU, 6 Other), drawn at random within those groups (seeded); the choice did not use the dictionary or any frame score. A chatbot text is the first 300 words of the answer. A news text is a **window of 250 to 300 words from inside the article**, not its opening. **Window rule:** a target length is drawn at random between 250 and 300 words (seeded); among all windows of that length, the one with the most AI words (AI, artificial intelligence, chatbot, ChatGPT, OpenAI, LLM, ...) and regulation words (regulat-, legislat-, law, rule, bill, ban, oversight, governance, policy, lawmaker) is chosen, provided it has at least two of each; ties go to the earliest window. If no window of that length has two of each, the window with the most such words is used and flagged in the analysis files (two articles are in this case). No frame hit or dictionary term is used to choose a window. A window is a continuous passage, so it may start or end in the middle of an argument: label what you see, not what the article might say before or after.

**Content note.** Some texts discuss suicide, sexual content in the context of chatbot safety, and hate speech. You may skip any text that distresses you: write `skip` in the label column (the scoring scripts treat it as missing and report how many were skipped) and tell the others.
