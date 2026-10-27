# Data, licensing and ethics (draft for the report)

*Drafted from what the repository does, with figures read from its files. Not legal advice; check wording with the module's guidance before submission.*

## 1. News data: source, licence and what we store

**Source.** The URL list comes from the Hugging Face dataset `brewcoua/genai-gdelt-framing` (Couaran, Pathania and Nair, 2026), a derived dataset of 1,116,091 online news articles on generative-AI governance (November 2022 to June 2026) built from the GDELT 2.0 Global Knowledge Graph. The dataset is released under **CC BY 4.0** and GDELT under CC BY; we attribute both and cite the paper. The dataset contains URLs and metadata only (`document_id` = URL, month, region, frame flags and embedding scores) and **no article text**. We use the URL, month and region to select articles, and the dataset's own frame labels once, as a cross-check of our dictionary.

**What we did to the data.** We filtered to July 2025 to June 2026 (314,876 articles), kept URLs with an AI term in the path (37,832), restricted EU and Other to likely-English domains, capped each outlet at 15, and drew a balanced sample of 2,360 URLs (US, UK, EU, Other). After scraping and cleaning the corpus has **420 articles from 285 outlets** (US 133, Other 104, UK 101, EU 82). The corpus is frozen: its SHA-256 hash and counts are recorded in `dataset/news/corpus_manifest.json`.

**Article text belongs to the publishers.** We scraped publicly available pages for non-commercial university research, and we do **not redistribute article text**. The repository therefore stores:

| stored in the repository (committed) | kept only on the authors' machines (git-ignored: `.env, .DS_Store, __pycache__/, .ipynb_checkpoints/, .venv/, data/`) |
|---|---|
| URL list (URL, month, region, outlet, quarter), sampling and cleaning log, corpus manifest with file hashes | scraped pages and the cleaned corpus (`data/scraped.csv`, `data/news_clean.csv`) |
| per-text frame scores and counts, lexicon, actor and entropy tables, chatbot answers and prompts | the dataset parquet file (about 90 MB, re-downloadable) |
| a few audit tables that carry **article titles and URLs** (never body text): `dataset/analysis/near_duplicates_remaining.csv`, `dataset/analysis/dedup_removed_articles.csv`, `dataset/analysis/near_duplicate_clusters.csv`, `dataset/analysis/dataset_label_disagreement_examples.csv`; and, as the only body text, about thirty short example quotations (at most about 20 words each) in `07_lexicon_signoff.ipynb`, used to document candidate lexicon terms | validation and stance labelling sheets, review files and low-hit samples, because they contain article text |

The submission ZIP must exclude `data/`. Anyone can rebuild the corpus from the URL list, the notebooks and `config.json`.

## 2. Collection conduct

- **robots.txt.** The scraper reads each site's `robots.txt` (Python `urllib.robotparser`) before every first request to a site and skips URLs it disallows: 38 of 2,360 sampled URLs were skipped for that reason.
- **Rate limit.** One request per second, one request per URL, no parallel requests. Pages that answered 401, 403, 429 or 451 were not retried or worked around (310 URLs). Pages that looked paywalled were dropped (3); we did not log in or bypass any access control.
- **Identification.** Requests carry the User-Agent `NCI-student-research/1.0 (contact: <university e-mail address>)` so that a site operator can reach us. The address is a university address read from a git-ignored `.env` file and is not published in the repository.
- **Access dates.** 2026-10-26 to 2026-10-27 (UTC), recorded in `dataset/news/corpus_log.json`. An earlier pilot scrape by a team member on 19 and 20 October 2026 (900 URLs, a first version of the corpus that was discarded because only 45 articles were usable) followed the same robots.txt and rate-limit rules and is not part of the analysed data.
- **Outcome of the scrape.** 2,360 URLs requested; 1,564 gave usable English text (66%); 504 were on-topic; 420 remained after removing duplicates.

## 3. Chatbot answers and terms of use

We generated 216 answers (54 prompts x 2 chatbots x 2 replicates). The prompts are generic policy questions and contain no personal data.
- **Llama 3.1 (8B)** ran locally through Ollama under the Llama 3.1 Community License Agreement (Meta); **Qwen3.5 (9B)** ran locally under the Apache License 2.0. Local models send nothing to a third party. Model digests, versions and settings are recorded in `dataset/answers/run_metadata.json`.
- **Gemini** (`gemini-3.8-flash`, Google AI Studio free tier) was tried first. The free tier allows only 20 requests per day for that model, so the attempt was abandoned after 21 answers, all of which were removed from the analysis; the two attempts stay in `run_metadata.json` annotated as abandoned. Before submission, check the current Gemini API terms: on the free tier Google may use prompts and outputs to improve its products, which is acceptable here only because the prompts are generic policy questions with no personal data.
- Chatbot output is machine-generated text; we analyse it as data and do not present it as the authors' or anyone's opinion.

## 4. Ethical considerations

- **No human participants.** Labelling (frame validation, stance) is done by team members on public texts and on chatbot output. No participant data are collected.
- **Personal data in news text.** Articles name public figures and sometimes private individuals (for example victims in court or safety stories). Article text stays on our machines; committed outputs hold counts, scores, URLs and titles of already published articles. Actor tables list the most mentioned organisations and public figures only.
- **Distressing content.** Some texts discuss suicide, sexual content in the context of chatbot safety, and hate speech. The labelling instructions carry a content note and allow skipping a text.
- **Load on publishers.** About 2,360 page requests were made in two runs (wall-clock span 13 hours including a pause), never faster than one request per second overall, and no site was asked for more than 15 pages.
- **Bias and representativeness.** The corpus is English-language and AI-focused (URL filter), and "Other" means English-language outlets outside the US, EU and UK. Findings describe this corpus, not news in general (see `docs/limitations.md`).
- **Reproducibility.** Seeds, settings, hashes and access dates are recorded; the dataset file is identical in every copy we hold (SHA-256 checked in `04_corpus_audit.ipynb`).
