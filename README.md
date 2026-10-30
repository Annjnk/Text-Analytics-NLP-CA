# Framing AI regulation: chatbot answers vs news

Text Analytics & NLP, CA1, National College of Ireland (BSHDS4).

| Name | Student ID |
|---|---|
| Anujin Ariunbold | x23171286 |
| Laith Waqas Mohammed Ahmad | x23103493 |
| Uuganbayar Enkhbaatar | x23176377 |

## Research question

How do AI chatbot answers and news articles differ in their emphasis on AI regulation frames, and how does this vary across prompt wording and news region?

- **H1:** chatbot answers spread their emphasis more evenly across six frames (higher rarefied frame entropy) than news articles.
- **H2:** that gap is smaller for leaning prompts (leaning_for / leaning_against) than for neutral prompts.
- **H3 (exploratory):** chatbot frame distributions are closer to some news regions (US, UK, EU, Other) than others (Jensen-Shannon divergence).

The six frames are innovation/opportunity, risk/safety, regulation/governance, rights/privacy, economy/labour and misinformation/integrity. Results are summarised in [`dataset/analysis/RESULTS.md`](dataset/analysis/RESULTS.md), and every analysis decision, with its date, is in [`dataset/analysis/DECISIONS.md`](dataset/analysis/DECISIONS.md).

## Data at a glance

| Corpus | Size | Source |
|---|---|---|
| Chatbot answers | 216 answers: 18 questions × 3 wordings × 2 models × 2 replicates | `llama3.1:8b` and `qwen3.5:9b`, run locally with Ollama |
| News articles | 420 articles from 285 outlets (US 133, Other 104, UK 101, EU 82), July 2025 to June 2026 | URLs from [`brewcoua/genai-gdelt-framing`](https://huggingface.co/datasets/brewcoua/genai-gdelt-framing) (CC BY 4.0), text scraped by us on 26–27 Oct 2026 |

## Repository structure

```
.
├── config.json                # every data path, read by all notebooks
├── framescore.py              # lexicon matcher and rarefied entropy
├── agreement.py               # Cohen's kappa and per-class agreement
├── requirements.txt           # dependencies (version ranges)
├── requirements.lock.txt      # exact versions used for the results
├── collect_answers.ipynb      # 01: collect the chatbot answers
├── news_corpus_v2.ipynb       # build the news corpus (current version)
├── news_corpus.ipynb          # first version, kept for the record; do not run
├── 02_ ... 10_*.ipynb         # analysis notebooks, run in order (see below)
├── dataset/                   # committed: everything except article text
│   ├── prompts.csv            # 54 prompts
│   ├── answers/               # answers.jsonl, run_metadata.json
│   ├── news/                  # URL lists, corpus log, corpus manifest (hashes)
│   ├── frames/                # lexicon v1.2, changelog, codebooks, review files
│   └── analysis/              # result tables and figures, RESULTS.md, DECISIONS.md
├── docs/                      # data_licensing_ethics.md, limitations.md
└── data/                      # NOT committed (git-ignored): article text, labelling sheets
```

`data/` holds publisher text and is never put on GitHub or in the submission ZIP. See [Getting the data](#getting-the-data).

## Setup

Tested with Python 3.12.

```bash
git clone https://github.com/Annjnk/Text-Analytics-NLP-CA
cd Text-Analytics-NLP-CA
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # or requirements.lock.txt for the exact versions
python -m spacy download en_core_web_sm
```

Main versions used for the results (full list in `requirements.lock.txt`): pandas 2.3.3, numpy 2.5.4, spaCy 3.8.16, scikit-learn 1.9.1, nltk 3.10.3, vaderSentiment 3.3.2, trafilatura 2.3.1, matplotlib 3.11.2.

Create a `.env` file in the repository root (it is git-ignored). It is only needed to scrape news:

```
NEWS_CONTACT=your-university-email
```

Ollama is only needed to regenerate the chatbot answers, which are already committed.

## Getting the data

**Chatbot answers** are committed in `dataset/answers/answers.jsonl`. Nothing to download.

**News articles.** The article text belongs to the publishers, so we do not redistribute it. The committed URL list (`dataset/news/urls_full.csv`), sampling settings and cleaning log let anyone rebuild the corpus:

1. Run `news_corpus_v2.ipynb`. It downloads the dataset parquet (about 90 MB) from Hugging Face into `data/` if it is missing, rebuilds the URL sample with seed 42, scrapes it (one request per second, robots.txt respected; our two runs took about 13 hours of wall-clock time including a pause), and cleans it into `data/news_clean.csv`.
2. Compare the result with `dataset/news/corpus_manifest.json` (row count and SHA-256 hash).

A rebuilt corpus will not be identical to ours: pages change, move or disappear after our access dates (26–27 Oct 2026, in `corpus_log.json`). The tables in `dataset/analysis/` were produced from the frozen 420-article corpus whose hash is in the manifest.

**Warning:** `news_corpus_v2.ipynb` writes to `data/news_clean.csv`. If you already have the frozen corpus there, back it up first, or point `news_corpus_csv` in `config.json` to a new file. Do not run `news_corpus.ipynb` (the first version) at all.

## Reproducing the results

Run the notebooks in this order. Every notebook reads its paths from `config.json` and writes its tables and figures to `dataset/analysis/` unless stated otherwise.

| Step | Notebook | What it does | Main outputs |
|---|---|---|---|
| 1 | `collect_answers.ipynb` | Runs the 54 prompts on both chatbots, 2 replicates each. Optional: the answers are committed | `dataset/answers/answers.jsonl`, `run_metadata.json` |
| 2 | `news_corpus_v2.ipynb` | Builds the news corpus (see above) | `data/news_clean.csv`, `dataset/news/*` |
| 3 | `02_chatbot_text_analysis.ipynb` | TF-IDF, n-grams, collocations, log-odds distinctive words, VADER tone | `tfidf_top_by_group.csv`, `ngrams_top.csv`, `collocations_by_chatbot.csv`, `chatbot_vs_news_log_odds.csv`, `vader_by_chatbot_wording.csv` |
| 4 | `03_frame_scoring.ipynb` | Scores every text on the six frames with lexicon v1.2 | `frame_scores_chatbot*.csv`, `frame_scores_news.csv`, `frame_mix_*.csv` |
| 5 | `04_corpus_audit.ipynb` | Deduplication, near-duplicate and on-topic checks. Changes nothing | `dedup_*.csv`, `near_duplicate*.csv` |
| 6 | `05_rarefied_entropy.ipynb` | **H1, H2, H3** with rarefied entropy and cluster bootstrap, plus all robustness runs | `h1_*.csv`, `h2_*.csv`, `h3_*.csv` |
| 7 | `06_style_vs_framing.ipynb` | Style vs framing classifiers, style-matched entropy, frame composition | `style_vs_framing_classifiers.csv`, `composition_*.csv` |
| 8 | `07_lexicon_signoff.ipynb` | Lexicon version, changelog and review files | `dataset/frames/*` |
| 9 | `08_validation_and_dataset_labels.ipynb` | Frame validation sheet, dictionary vs human labels, dictionary vs the dataset's own labels | `validation_*.csv`, `dataset_label_comparison_*.csv` |
| 10 | `09_stance_and_actors.ipynb` | Stance labelling sheets, inter-annotator agreement, stance baseline, named-entity actors | `stance_*.csv`, `actors_*.csv` |
| 11 | `10_limitations_and_ethics.ipynb` | Regenerates the ethics and limitations text from the result files | `docs/*.md` |

Steps 3 to 11 need `data/news_clean.csv`. Steps 9 and 10 also need the labelled sheets in `data/` (see `dataset/frames/validation_instructions.md` and `dataset/frames/stance_codebook.md`). Without them, those notebooks run their tests on dummy labels and skip the real scores.

## Reproducibility

- Random seed 42 for sampling, rarefaction (1,000 draws at K = 5) and the 5,000-draw cluster bootstrap.
- Lexicon v1.2, signed off 27 Oct 2026, before any hypothesis test was run (`dataset/frames/CHANGELOG.md`).
- Corpus frozen 27 Oct 2026, with row count and SHA-256 hash in `dataset/news/corpus_manifest.json`.
- Model names, digests and generation settings for every chatbot run are in `dataset/answers/run_metadata.json`.
- Decisions that affect the analysis are dated in `dataset/analysis/DECISIONS.md`, written before the step they govern.

## Licence, ethics and limitations

- News URLs and metadata: `brewcoua/genai-gdelt-framing` (Couaran, Pathania and Nair, 2026), CC BY 4.0, built from GDELT (CC BY).
- Article text is scraped for non-commercial university research and not redistributed.
- Full details of collection conduct, model licences and ethics are in [`docs/data_licensing_ethics.md`](docs/data_licensing_ethics.md), and the study's limitations are in [`docs/limitations.md`](docs/limitations.md).
