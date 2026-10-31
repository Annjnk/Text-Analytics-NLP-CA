"""Builds docs/report_numbers.md from the result files under dataset/ (nothing is typed by hand except the status notes).

Usage, from the repository root:  import report_numbers; report_numbers.build()   (called by 10_limitations_and_ethics.ipynb, section 4).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(".")
A = ROOT / "dataset" / "analysis"
rd = lambda name, **kw: pd.read_csv(A / name, keep_default_na=False, **kw) if kw.pop("keep", True) else pd.read_csv(A / name, **kw)
num = lambda name: pd.read_csv(A / name)                      # numeric tables (NaN kept as NaN)

def f(x, d=3, sign=False):
    if x is None or (isinstance(x, float) and np.isnan(x)) or x == "": return "n/a"
    x = round(float(x), d) + 0.0                                # +0.0 turns -0.0 into 0.0
    return f"{x:+.{d}f}" if sign else f"{x:.{d}f}"
def ci(e, lo, hi, d=3): return f"{f(e, d, True)} [{f(lo, d, True)}, {f(hi, d, True)}]"
def ciu(e, lo, hi, d=3): return f"{f(e, d)} [{f(lo, d)}, {f(hi, d)}]"      # unsigned: JSD and shares cannot be negative
def pct(x, d=0): return f"{100 * x:.{d}f}%"
def table(df, align=None):
    cols = list(df.columns); out = ["| " + " | ".join(str(c).replace("|", "/") for c in cols) + " |", "|" + "|".join("---" if (align is None or align.get(c, "l") == "l") else "--:" for c in cols) + "|"]
    for _, r in df.iterrows(): out.append("| " + " | ".join(str(v).replace("|", "/").replace("\n", " ") for v in r) + " |")
    return "\n".join(out)

L = []                                                         # the document, line by line
last = [0]                                                     # index in L where the content of the current block starts
def H(level, text): L.extend(["", "#" * level + " " + text, ""]); last[0] = len(L)
def P(text): L.extend([text, ""])
def block(title, source, status, note=None):
    L[last[0]:last[0]] = [f"**{title}**", ""]                  # the title goes above the tables and text written since the last block
    L.extend([f"- Source: {source}", f"- Status: {status}"] + ([f"- Note: {note}"] if note else []) + [""]); last[0] = len(L)
FINAL, CAVEAT = "FINAL", "FINAL, with the caveat below"

def pending_list():
    items = []
    vo = num("validation_overall_by_scope.csv")
    items.append(("Frame validation: no second labeller", f"The dictionary was checked against one labelled sheet ({int(vo.loc[0,'n_scored'])} texts scored, {int(vo.loc[0,'n_skipped'])} skipped). There is no human-against-human reliability for frames, and per-frame kappas rest on a handful of texts. Do not report a frame reliability figure; if one is wanted, a second labeller has to label the same 50 texts and the agreement script run on both."))
    adj = rd("stance_adjudication_outcome.csv"); n_cons = int((adj["consensus"] != "").sum()); n_reason = int((adj["reason"] != "").sum())
    items.append(("Stance adjudication: reasons", f"Consensus labels exist for {n_cons} of the {int((adj['kind'] != 'shared, labels agree').sum())} texts the labellers reviewed, but a reason is recorded for only {n_reason}. The labels are final; the reasoning is not documented. Fill the `reason` column of `stance_texts_to_discuss.xlsx` and re-import (notebook 09, section 2e) if the report wants to describe how disputes were settled."))
    items.append(("Stance reference is not independent", "The adjudicated labels are agreed by the two people who produced the earlier labels, so they are not an independent check. Report the human-against-human agreement (before adjudication) as the reliability figure."))
    items.append(("Stance baseline depends on who labelled", "Against labeller A's labels VADER reaches kappa 0.03 and against labeller B's 0.35 (all texts). Quote the adjudicated-reference result and the within-source rows, and say the baseline is labeller-dependent."))
    items.append(("H1 is model-dependent", "Llama is indistinguishable from news; Qwen is higher; the pooled result is marginal and fragile (see section 2). Report all three, not the pooled line alone."))
    items.append(("Lexicon edited after hit counts were seen", "Lexicon v1.2 (9 terms dropped, 7 added) was chosen after looking at hit counts in both corpora, before any H1 to H3 test (`dataset/frames/CHANGELOG.md`, `DECISIONS.md`). State this; the lexicon-variant runs in section 2 show H1 does not rest on it."))
    items.append(("Composition and governance are exploratory", "12 composition comparisons without correction; governance is partly present by design in the prompts, and the on-topic filter shares words with the governance lexicon (section 5)."))
    items.append(("Files from the earlier 300-word design", "`frame_scores_chatbot.csv`, `frame_scores_news.csv`, `entropy_chatbot_by_wording.csv`, `frame_mix_chatbot_by_*.csv` and `frame_mix_by_group.png` come from notebook 03's 300-word scoring. They are descriptive and consistent with lexicon v1.2, but the main analysis is full-text (`DECISIONS.md`, 2026-10-29). Prefer the `*_full*` tables and `composition_*` for the report."))
    items.append(("Validation sheet shows excerpts", "Humans labelled the first 300 words of each answer and a 250 to 300 word window of each article, not the full texts the main analysis scores; two of the 25 news windows do not pass the on-topic rule."))
    return items

def build():
    L.clear(); last[0] = 0
    L.extend(["# Report numbers", "",
          "Every number, table and figure the report needs, with the file it comes from and whether it is final. Generated by `10_limitations_and_ethics.ipynb` (section 4) from the result files, so nothing here is typed by hand except the status notes. If a result file changes, rerun that notebook.", "",
          "**Status legend.** FINAL: computed from final inputs, nothing is waiting on it. FINAL with a caveat: the number is settled but must be quoted with the caveat. PENDING: waiting on something outside the code (listed in section 11).", "",
          "**Conventions.** H1 and the composition tables are chatbot minus news. Intervals are 95% cluster-bootstrap intervals (`question_id` for chatbots, `outlet` for news) unless stated; a `*` marks an interval that excludes zero. K = 5 draws, 1,000 repeats, seed 42, full-text scoring, lexicon v1.2. All paths are relative to the repository root; the result files are in `dataset/analysis/`."])

    # ---------------------------------------------------------------------------------------------- 1 data
    H(2, "1. Data, corpus and lexicon")
    prompts = pd.read_csv(ROOT / "dataset" / "prompts.csv"); ans = pd.read_json(ROOT / "dataset" / "answers" / "answers.jsonl", lines=True)
    H(3, "1.1 Prompts and chatbot answers")
    n_q = prompts["question_id"].nunique(); n_w = prompts["wording"].nunique()
    P(f"{len(prompts)} prompts = {n_q} questions x {n_w} wordings ({', '.join(sorted(prompts['wording'].unique()))}); {len(ans)} answers = {ans['chatbot'].nunique()} chatbots x {ans.groupby('chatbot').size().iloc[0]} answers each (2 replicates per prompt). Each prompt asks for about 250 words of plain prose.")
    block("Prompt and answer counts", "`dataset/prompts.csv`, `dataset/answers/answers.jsonl`", FINAL)
    meta = json.load(open(ROOT / "dataset" / "answers" / "run_metadata.json"))
    rows = []
    for e in meta:
        mi = e.get("model_info", {}); st = e.get("settings", {})
        rows.append({"chatbot": e["chatbot"], "run": e.get("run_type", ""), "status": e.get("status", "used"), "answers in this run": e.get("answers_collected_in_this_run", ""),
                     "model digest / version": (mi.get("model_digest") or mi.get("version") or "")[:14], "temperature": st.get("temperature"), "top_p": st.get("top_p"), "max_output_tokens": st.get("max_output_tokens"), "seed": st.get("seed")})
    P(table(pd.DataFrame(rows)))
    block("Chatbot runs and generation settings", "`dataset/answers/run_metadata.json`", FINAL, "The two Gemini entries are annotated as abandoned (free-tier quota after 21 answers); their answers are not in `answers.jsonl` and not in any analysis.")
    ln = num("length_full_text.csv")
    P(table(ln.assign(**{c: ln[c].map(lambda x: f(x, 1)) for c in ("words_mean", "words_median")}).rename(columns={"group": "group", "n_texts": "texts", "words_mean": "mean words", "words_median": "median words", "words_min": "min", "words_max": "max"})))
    block("Length of the texts scored (full text)", "`dataset/analysis/length_full_text.csv`", FINAL, "News articles are about four times longer than chatbot answers; rarefaction removes the dependence of entropy on hit count, not real diversity.")

    H(3, "1.2 News corpus")
    log = json.load(open(ROOT / "dataset" / "news" / "corpus_log.json")); man = json.load(open(ROOT / "dataset" / "news" / "corpus_manifest.json"))
    P("Selection (URL list, before scraping):"); P(table(pd.DataFrame(log["selection_steps"], columns=["step", "rows"]).assign(rows=lambda d: d["rows"].map(lambda x: f"{int(x):,}"))))
    P("Scraping and cleaning:"); P(table(pd.DataFrame(log["cleaning_steps"], columns=["step", "articles"])))
    block("Selection and cleaning funnel", "`dataset/news/corpus_log.json`", FINAL, f"Pilot: usable text {pct(log['pilot']['usable'])}, on-topic {pct(log['pilot']['on_topic'])}. Window {log['settings']['months'][0]} to {log['settings']['months'][1]}, regions {', '.join(log['settings']['regions'])}, seed {log['settings']['seed']}, at most {log['settings']['max_per_outlet']} per outlet.")
    reg = man["articles_per_region"]; qt = man["articles_per_quarter"]
    P(f"**Frozen corpus: {man['rows']} articles from {man['outlets']} outlets** (US {reg['US']}, Other {reg['Other']}, UK {reg['UK']}, EU {reg['EU']}); at most {man['max_articles_per_outlet']} per outlet; per quarter " + ", ".join(f"{k} {v}" for k, v in qt.items()) + f". Access dates {log['access_dates'][0][:10]} to {log['access_dates'][1][:10]}. SHA-256 of the corpus file: `{man['sha256'][:16]}...`.")
    block("Corpus counts and hash", "`dataset/news/corpus_manifest.json`", FINAL, "The article text itself is not in the repository (publisher text); `04_corpus_audit.ipynb` checks the files against the manifest hashes.")
    dd = num("dedup_before_after_by_region.csv"); P(table(dd.assign(before=dd["before"].astype(int), after=dd["after"].astype(int), removed=dd["removed"].astype(int), **{"removed_%": dd["removed_%"].map(lambda x: f(x, 1))})))
    cl = num("near_duplicate_clusters.csv")
    block("Deduplication before/after", "`dataset/analysis/dedup_before_after_by_region.csv`", FINAL, f"The rule removed exact duplicates only; {len(cl)} clusters of near-duplicate articles ({int(cl['size'].sum())} articles, {int(cl['size'].sum()) - len(cl)} redundant) remain in the frozen corpus (`near_duplicate_clusters.csv`). Report this as a limitation.")

    H(3, "1.3 Lexicon")
    lex = json.load(open(ROOT / "dataset" / "frames" / "frame_keywords.json"))
    P(f"Lexicon version {lex['version']}, signed off: {lex['signed_off']} ({lex.get('signed_off_by')}), tagged {lex['date']}. {sum(len(v) for v in lex['frames'].values())} terms in {len(lex['frames'])} frames; {len(lex['ambiguous_terms'])} ambiguous terms (dropped in one robustness run); {len(lex['jurisdiction_terms']['terms'])} jurisdiction terms (counted separately, never scored as a frame).")
    P(table(pd.DataFrame({"frame": list(lex["frames"]), "terms": [len(v) for v in lex["frames"].values()]})))
    block("Lexicon size and version", "`dataset/frames/frame_keywords.json`, `dataset/frames/CHANGELOG.md`", CAVEAT, "v1.2 (9 terms dropped, 7 added) was chosen after hit counts were seen and before any H1 to H3 test.")
    dens = num("frame_density_full_text.csv")
    P(table(dens[["group", "n_texts", "n_under_5", "hits_mean", "hits_median", "hits_per_100w_mean"]].assign(hits_mean=lambda d: d["hits_mean"].map(lambda x: f(x, 1)), hits_per_100w_mean=lambda d: d["hits_per_100w_mean"].map(lambda x: f(x, 2)))))
    block("Frame hits per text (density)", "`dataset/analysis/frame_density_full_text.csv`", FINAL, "Texts with fewer than 5 hits cannot be rarefied at K = 5 and are excluded from the H1 means (the bounds analysis in section 2 puts them back).")

    # ---------------------------------------------------------------------------------------------- 2 H1
    H(2, "2. H1: chatbot answers spread emphasis more evenly than news")
    h1 = num("h1_main.csv")
    P(table(pd.DataFrame({"comparison": h1["comparison"], "texts (chatbot / news)": h1["n_chatbot"].astype(int).astype(str) + " / " + h1["n_news"].astype(int).astype(str), "chatbot mean": h1["chatbot_mean"].map(f), "news mean": h1["news_mean"].map(f),
                          "difference [95% CI]": [ci(r.diff, r.diff_lo, r.diff_hi) + (" *" if r.excludes_zero else "") for r in h1.itertuples()]})))
    block("H1 main result (full text, K = 5, rarefied normalised entropy)", "`dataset/analysis/h1_main.csv`", CAVEAT,
          "Maximum possible value at K = 5 is 0.898. Positive = chatbot more even. The result is model-dependent: Llama is not distinguishable from news, Qwen is higher, and the pooled interval just excludes zero. Full-text news is about four times longer than answers; rarefaction fixes estimator bias, not real diversity, which works against H1.")
    rs = num("h1_robustness_summary.csv"); runs = rs[~rs["run"].str.startswith("main") & ~rs["run"].str.contains("reference")]
    order = list(dict.fromkeys(rs["run"])); comps = ["Llama vs news", "Qwen vs news", "chatbots pooled vs news"]
    mat = pd.DataFrame({"run": order})
    for c in comps:
        sub = rs[rs["comparison"] == c].set_index("run"); mat[c] = [ci(sub.loc[r, "diff"], sub.loc[r, "diff_lo"], sub.loc[r, "diff_hi"]) + (" *" if sub.loc[r, "excludes_zero"] else "") if r in sub.index else "" for r in order]
    P(table(mat))
    n_runs = runs["run"].nunique()
    cnt = pd.DataFrame({"comparison": comps, "runs with the interval excluding zero, chatbot higher": [f"{int(((runs['comparison'] == c) & runs['excludes_zero'] & (runs['diff'] > 0)).sum())} of {n_runs}" for c in comps],
                        "runs with the point estimate positive": [f"{int(((runs['comparison'] == c) & (runs['diff'] > 0)).sum())} of {n_runs}" for c in comps]})
    P(table(cnt))
    block("H1 robustness summary (one line per run)", "`dataset/analysis/h1_robustness_summary.csv`", CAVEAT, f"{n_runs} robustness runs (the main run and the duplicate 'all terms' reference row are not counted): K = 3 and 8, three bounds rules, pooled counts, six lexicon variants, topic-selected windows, fixed 300- and 150-word cuts. The fixed cuts have the largest gaps but only {pct(1 - num('h1_cut_shares.csv').query('cut == \"first 150 words\" and group == \"news\"')['share_scorable_5_hits'].iloc[0])} of news articles are scorable at 150 words, so they are not stronger evidence.")
    P("Details behind the summary:")
    sk = num("h1_sensitivity_k.csv"); P(table(sk[["comparison", "K"]].assign(**{"difference [95% CI]": [ci(r.diff, r.diff_lo, r.diff_hi) + (" *" if r.excludes_zero else "") for r in sk.itertuples()]})))
    block("Draw size K = 3 and 8", "`dataset/analysis/h1_sensitivity_k.csv`", FINAL, "Never compare values across different K (the maximum entropy differs).")
    bd = num("h1_bounds.csv"); P(table(bd[["comparison", "rule"]].assign(**{"difference [95% CI]": [ci(r.diff, r.diff_lo, r.diff_hi) + (" *" if r.excludes_zero else "") for r in bd.itertuples()]})))
    block("Bounds: texts with fewer than 5 hits scored at the minimum, the group median and the maximum", "`dataset/analysis/h1_bounds.csv`", FINAL)
    pl = num("h1_pooled.csv"); P(table(pd.DataFrame({"comparison": pl["comparison"], "hits drawn": pl["N_hits_drawn"].astype(int), "chatbot pooled": pl["chatbot_pooled_entropy"].map(f), "news pooled": pl["news_pooled_entropy"].map(f),
                                                      "difference [percentile CI]": [ci(r.diff, r.diff_lo, r.diff_hi) for r in pl.itertuples()], "bias-corrected CI": [f"[{f(r.diff_lo_basic, 3, True)}, {f(r.diff_hi_basic, 3, True)}]" for r in pl.itertuples()]})))
    block("Pooled counts (every text used, no exclusions)", "`dataset/analysis/h1_pooled.csv`", FINAL, "No difference for any comparison; both intervals include zero. With few clusters the percentile bootstrap is shifted, so the bias-corrected interval is shown beside it.")
    lv = num("h1_lexicon_variants.csv"); P(table(lv[["run", "comparison"]].assign(**{"difference [95% CI]": [ci(r.diff, r.diff_lo, r.diff_hi) + (" *" if r.excludes_zero else "") for r in lv.itertuples()], "texts excluded (chatbot / news)": lv["excluded_chatbot"].astype(int).astype(str) + " / " + lv["excluded_news"].astype(int).astype(str)}).assign(run=lambda d: d["run"].str.replace("lexicon: ", ""))))
    block("Lexicon variants (no governance frame, no ambiguous terms, prompt-echo terms, no 'lawsuit')", "`dataset/analysis/h1_lexicon_variants.csv`", FINAL, "The two prompt-echo runs differ: one drops each answer's own prompt terms (chatbots only), the other drops every term found in any prompt from both groups (symmetric, the fairer one).")
    wn = num("h1_windows.csv"); P(table(wn[["comparison"]].assign(**{"difference [95% CI]": [ci(r.diff, r.diff_lo, r.diff_hi) + (" *" if r.excludes_zero else "") for r in wn.itertuples()], "texts (chatbot / news windows)": wn["n_chatbot"].astype(int).astype(str) + " / " + wn["n_news"].astype(int).astype(str)})))
    wl = num("h1_window_length_match.csv"); P(table(wl.assign(**{c: wl[c].map(lambda x: f(x, 1)) for c in ("window_words_mean", "window_words_median", "answer_words_mean", "answer_words_median")}).assign(ks_window_vs_answer=lambda d: d["ks_window_vs_answer"].map(f))))
    ws = num("h1_window_survival.csv"); P(table(ws.pivot(index="region", columns="matched_to", values="articles_with_a_window").reset_index()))
    block("Topic-selected, length-matched windows: result, length match and surviving articles", "`dataset/analysis/h1_windows.csv`, `h1_window_length_match.csv`, `h1_window_survival.csv`, `h1_window_length_histograms.png`", FINAL, "Windows match the answer lengths closely (KS statistic in the table). Articles with no window that passes the on-topic rule drop out; the last table counts the survivors per region.")
    fc = num("h1_fixed_cuts.csv"); P(table(fc[["cut_words", "comparison"]].assign(**{"difference [95% CI]": [ci(r.diff, r.diff_lo, r.diff_hi) + (" *" if r.excludes_zero else "") for r in fc.itertuples()]})))
    cs = num("h1_cut_shares.csv"); P(table(cs.assign(**{"on-topic in cut": cs["share_on_topic_in_cut"].map(lambda x: pct(x)), "scorable (>= 5 hits)": cs["share_scorable_5_hits"].map(lambda x: pct(x)), "hits mean": cs["hits_mean"].map(lambda x: f(x, 1))})[["cut", "group", "n_texts", "words_median", "on-topic in cut", "scorable (>= 5 hits)", "hits mean"]]))
    block("Fixed 300-word and 150-word cuts: result and on-topic / scorable shares", "`dataset/analysis/h1_fixed_cuts.csv`, `h1_cut_shares.csv`", FINAL)
    co = num("entropy_length_correlations_full_text.csv"); cp_ = co.pivot_table(index=["texts", "against"], columns="entropy", values="spearman_rho").reset_index(); cp_.columns.name = None
    for c_ in cp_.columns[2:]: cp_[c_] = cp_[c_].map(lambda x: f(x, 3, True))
    P(table(cp_))
    block("Does entropy still depend on length and hit count? (Spearman)", "`dataset/analysis/entropy_length_correlations_full_text.csv`", FINAL, "After rarefaction the within-model correlations are near zero; the pooled-chatbot ones come from pooling two models that differ in both length and entropy.")

    # ---------------------------------------------------------------------------------------------- 3 H2
    H(2, "3. H2: is the gap smaller for leaning prompts?")
    h2 = num("h2_gap_and_contrasts.csv")
    P(table(h2.assign(**{"estimate [95% CI]": [ci(r.estimate, r.lo, r.hi) + (" *" if r.excludes_zero else "") for r in h2.itertuples()]})[["chatbot", "quantity", "estimate [95% CI]", "n_questions"]]))
    block("H2 gaps and paired contrasts by question", "`dataset/analysis/h2_gap_and_contrasts.csv`", CAVEAT, "H2 predicts a negative 'leaning minus neutral' contrast. No contrast excludes zero, so H2 is not supported; with 18 questions that is an absence of evidence, not evidence of absence. Frame identity and stance are tied (15 lexicon terms differ 2x or more between `leaning_for` and `leaning_against` answers, `h2_stance_term_check.csv`), so an entropy difference by wording could come from the arguments themselves.")
    ft = num("frame_mix_by_topic_with_entropy.csv"); ft = ft[ft["chatbot"] == "chatbots pooled"]
    P(table(ft.assign(**{c: ft[c].map(f) for c in ft.columns if c.startswith("share_") or c in ("mean_rarefied_entropy_k5", "pooled_entropy_of_mix")}).drop(columns=["chatbot"])))
    block("Frame mix per prompt topic, next to the entropy (pooled chatbots)", "`dataset/analysis/frame_mix_by_topic_with_entropy.csv`", FINAL, "The prompt set is balanced by design (3 questions per topic), so a pooled mix looks spread out partly because the prompts ask about all six topics.")

    # ---------------------------------------------------------------------------------------------- 4 H3
    H(2, "4. H3 (exploratory): Jensen-Shannon divergence to news regions")
    j = num("h3_jsd_chatbot_vs_news_regions.csv"); regs = ["US", "UK", "EU", "Other"]
    rowsj = []
    for ch in ["Llama", "Qwen", "chatbots pooled"]:
        sub = j[j["chatbot"] == ch].set_index("news_region"); rowsj.append({"chatbot": ch, **{r: ciu(sub.loc[r, "jsd"], sub.loc[r, "lo"], sub.loc[r, "hi"]) for r in regs}, "noise floor (chatbot halves)": f(sub.iloc[0]["noise_floor_chatbot_halves"])})
    P(table(pd.DataFrame(rowsj)))
    nf = j[j["chatbot"] == "Llama"].set_index("news_region")
    P(table(pd.DataFrame({"news region": regs, "articles": [int(nf.loc[r, "n_articles"]) for r in regs], "outlets": [int(nf.loc[r, "n_outlets"]) for r in regs], "frame hits": [int(nf.loc[r, "news_hits"]) for r in regs], "noise floor (news halves)": [f(nf.loc[r, "noise_floor_news_halves"]) for r in regs]})))
    block("JSD between each chatbot's frame distribution and each news region", "`dataset/analysis/h3_jsd_chatbot_vs_news_regions.csv`", CAVEAT, "Exploratory. Base-2 logarithm (0 = identical, 1 = no overlap). EU (82 articles) and UK (101) are the weakest comparisons. Percentile intervals sit above the point estimates because JSD is biased upwards under cluster resampling; compare each divergence with its noise floor.")
    rd3 = num("h3_region_differences.csv"); pr = rd3[rd3["chatbot"] == "chatbots pooled"]
    P(table(pr.assign(**{"difference [95% CI]": [ci(r.estimate, r.lo, r.hi) + (" *" if r.excludes_zero else "") for r in pr.itertuples()]})[["comparison", "difference [95% CI]", "closer_to"]]))
    block("Is the pooled chatbot closer to one region than another? (paired on the same chatbot draws)", "`dataset/analysis/h3_region_differences.csv`", CAVEAT, f"{int(rd3['excludes_zero'].sum())} of {len(rd3)} paired region differences (3 chatbot groups x 6 pairs) exclude zero: no region is reliably closer. The UK is nearest by point estimate.")
    pw = pd.read_csv(A / "h3_pairwise_jsd.csv", index_col=0); pw3 = pw.copy()
    for c_ in pw3.columns: pw3[c_] = pw3[c_].map(lambda x: f(x, 3))
    P(table(pw3.reset_index().rename(columns={"index": "", pw.index.name or "index": ""})))
    block("Pairwise JSD among all six frame distributions (point estimates, for scale)", "`dataset/analysis/h3_pairwise_jsd.csv`", FINAL)

    # ---------------------------------------------------------------------------------------------- 5 composition
    H(2, "5. Frame composition: which frames differ (exploratory)")
    cp = num("composition_by_frame.csv"); frames = list(lex["frames"]); groups = ["Llama", "Qwen", "chatbots pooled", "news (all)", "news | US", "news | UK", "news | EU", "news | Other"]
    P(table(pd.DataFrame({"frame": frames, **{g: [ciu(cp[(cp.group == g) & (cp.frame == fr)].mean_share.iloc[0], cp[(cp.group == g) & (cp.frame == fr)].lo.iloc[0], cp[(cp.group == g) & (cp.frame == fr)].hi.iloc[0]) for fr in frames] for g in groups}})))
    block("Mean share of a text's hits per frame, with 95% cluster-bootstrap intervals", "`dataset/analysis/composition_by_frame.csv`, `composition_by_frame.png`", CAVEAT, "Exploratory: 12 chatbot-minus-news comparisons without correction, and the shares of one text sum to 1.")
    cd = num("composition_differences_vs_news.csv")
    P(table(pd.DataFrame({"frame": frames, **{c: [ci(cd[(cd.chatbot == c) & (cd.frame == fr)].diff_share.iloc[0], cd[(cd.chatbot == c) & (cd.frame == fr)].lo.iloc[0], cd[(cd.chatbot == c) & (cd.frame == fr)].hi.iloc[0]) + (" *" if cd[(cd.chatbot == c) & (cd.frame == fr)].excludes_zero.iloc[0] else "") for fr in frames] for c in ["Llama", "Qwen", "chatbots pooled"]}})))
    block("Chatbot minus all news, share of hits per frame", "`dataset/analysis/composition_differences_vs_news.csv`", CAVEAT, "Chatbots put more of their hits in innovation/opportunity and governance and less in economy/labour; the other three frames do not differ.")
    ge = num("composition_governance_effect.csv")
    P(table(pd.DataFrame({"chatbot": ge["chatbot"], "governance difference, all terms": [ci(r.gov_diff_all_terms, r.lo_all, r.hi_all) + (" *" if r.excludes_zero_all else "") for r in ge.itertuples()],
                          "without the 9 filter-overlap terms": [ci(r.gov_diff_without_overlap, r.lo_without, r.hi_without) + (" *" if r.excludes_zero_without else "") for r in ge.itertuples()],
                          "news governance share (all / without)": [f"{f(r.gov_share_news_all_terms)} / {f(r.gov_share_news_without_overlap)}" for r in ge.itertuples()]})))
    block("Governance difference with and without the nine governance terms that the on-topic filter also counts", "`dataset/analysis/composition_governance_effect.csv`, `composition_differences_no_filter_overlap.csv`", CAVEAT, "Removing the overlap terms lowers the news governance share and raises the chatbot-minus-news difference, so the overlap masks the difference rather than creating it. The prompt-design caveat (every prompt asks what governments should do) is unaffected.")

    # ---------------------------------------------------------------------------------------------- 6 style
    H(2, "6. Style versus framing")
    sc = num("style_vs_framing_classifiers.csv"); P(table(sc.assign(**{"AUC": sc["auc_mean"].map(f), "AUC sd": sc["auc_sd"].map(f), "balanced accuracy": sc["balanced_acc_mean"].map(f)})[["features", "split", "n_folds", "AUC", "AUC sd", "balanced accuracy"]]))
    block("Held-out AUC of the style classifier (A), the frame-mix classifier (B) and both", "`dataset/analysis/style_vs_framing_classifiers.csv`", CAVEAT, "A (style only, every lexicon term removed) is near 1.0 with outlets, questions or a whole chatbot held out; B (six frame shares only) is about 0.70 to 0.74, so the frame mix is not a pure style artefact, but A + B cannot be assessed (A is at the ceiling).")
    sm = num("style_matched_entropy_comparison.csv"); P(table(sm.assign(**{"difference [95% CI]": [ci(r.diff_mean, r.diff_lo, r.diff_hi, 3) + (" *" if (r.diff_lo > 0 or r.diff_hi < 0) else "") for r in sm.itertuples()]})[["chatbot", "pairs_with_both_scored", "difference [95% CI]"]]))
    sb = num("style_matching_balance.csv"); sb2 = sb[sb["spec"] == "2 features"]
    P(table(sb2.assign(SMD_before=sb2["SMD_before"].map(lambda x: f(x, 2, True)), SMD_after=sb2["SMD_after"].map(lambda x: f(x, 2, True)))[["chatbot", "feature", "matched_on", "SMD_before", "SMD_after", "pairs_kept"]]))
    block("Entropy on the style-matched subset (matched on sentence length and commas) and the balance achieved", "`dataset/analysis/style_matched_entropy_comparison.csv`, `style_matching_balance.csv`", CAVEAT, "Matching removes the sentence-length and comma differences and leaves the entropy gaps unchanged. Paragraph breaks and digits cannot be balanced (|SMD| stays above 1), so formatting differences remain.")

    # ---------------------------------------------------------------------------------------------- 7 frame validation
    H(2, "7. Dictionary validation against human frame labels")
    vo = num("validation_overall_by_scope.csv"); P(table(vo.assign(agreement=vo["agreement"].map(f), kappa_all_labels=vo["kappa_all_labels"].map(f))))
    block("Overall agreement and kappa (human = reference; dictionary label computed on the same excerpt)", "`dataset/analysis/validation_overall_by_scope.csv`, `validation_summary.csv`", CAVEAT, "One labelled sheet, no second labeller. The excerpts are not the full texts the main analysis scores. The lexicon was not edited.")
    vp = num("validation_per_frame_by_scope.csv")
    for sc_name in ["all scored texts", "chatbot", "news"]:
        t = vp[vp["scope"] == sc_name]
        P(f"*{sc_name}*"); P(table(t.assign(precision=t["precision"].map(f), recall=t["recall"].map(f), kappa=t["kappa_one_vs_rest"].map(f))[["frame", "n_human", "n_dictionary", "true_positive", "precision", "recall", "kappa", "vs_bar_0.6"]]))
    below = {s: vp[(vp.scope == s) & vp.frame.isin(frames) & (vp["vs_bar_0.6"] == "below")]["frame"].tolist() for s in ["all scored texts", "chatbot", "news"]}
    block("Per-frame precision, recall and one-versus-rest kappa against the 0.6 bar", "`dataset/analysis/validation_per_frame_by_scope.csv`, `validation_per_frame.csv`", CAVEAT, "Frames below 0.6: all texts " + (", ".join(below["all scored texts"]) or "none") + "; chatbot " + (", ".join(below["chatbot"]) or "none") + "; news " + (", ".join(below["news"]) or "none") + ". Each frame has 0 to 14 human labels, so per-frame kappas are unstable; 'none' is never used by the dictionary.")
    vc = pd.read_csv(A / "validation_confusion.csv"); P(table(vc))
    block("Confusion matrix, all scored texts (rows: human, columns: dictionary)", "`dataset/analysis/validation_confusion.csv`, `validation_confusion_by_scope.csv` (by source)", FINAL)
    dp = num("dataset_label_comparison_per_frame.csv"); P(table(dp.assign(**{c: dp[c].map(lambda x: f(x, 3)) for c in ("kappa", "precision_vs_dataset", "recall_vs_dataset")})))
    conf = pd.read_csv(A / "dataset_label_comparison_confusion.csv", index_col=0).to_numpy(float); po = np.trace(conf) / conf.sum(); pe = ((conf.sum(0) / conf.sum()) * (conf.sum(1) / conf.sum())).sum()
    dw = num("dataset_label_comparison_windows_summary.csv")
    P(f"Top frame against the dataset's own `dominant_frame`: {int(conf.sum())} articles, agreement {f(po)}, kappa {f((po - pe) / (1 - pe))}. On the validation sheet's articles: " + "; ".join(f"{r.scope}: agreement {f(r.agreement)}" + (f", kappa {f(r.kappa)}" if r.kappa == r.kappa else "") + f" (n = {int(r.n_articles)})" for r in dw.itertuples()) + ".")
    block("Dictionary against the dataset's own labels (a cross-check, not human validation)", "`dataset/analysis/dataset_label_comparison_per_frame.csv`, `dataset_label_comparison_confusion.csv`, `dataset_label_comparison_windows_summary.csv`", CAVEAT, "The dataset assigns frames from GDELT entity names and quotations, so the two instruments read different material; the per-frame kappa here uses 'at least one hit' as the dictionary's frame-present rule.")

    # ---------------------------------------------------------------------------------------------- 8 stance
    H(2, "8. Stance")
    sa = num("stance_agreement.csv").iloc[0]; sbs = num("stance_agreement_by_source.csv")
    P(f"Human against human on the {int(sa['n_shared'])} shared texts, working independently (before any adjudication): observed agreement {f(sa['agreement'], 2)}, Cohen's kappa {f(sa['kappa_4_labels'])} on four labels and {f(sa['kappa_3_labels'])} on the three plan labels (n = {int(sa['n_three_label'])}).")
    P(table(sbs.assign(agreement=sbs["agreement"].map(f), kappa_4_labels=sbs["kappa_4_labels"].map(f))))
    block("Inter-labeller agreement", "`dataset/analysis/stance_agreement.csv`, `stance_agreement_by_source.csv`, `stance_agreement_confusion.csv`", CAVEAT, "Weak agreement (both kappas below 0.6). Labeller A used 'mixed' far more often than labeller B on the shared texts. 10 texts per source, so the by-source rows are indications.")
    lc = pd.read_csv(A / "stance_label_counts_by_labeller.csv"); P(table(lc))
    block("Label counts by labeller", "`dataset/analysis/stance_label_counts_by_labeller.csv`, `stance_labels_by_source_and_labeller.csv`", FINAL, "In both labellers' labels nearly all news texts are none or mixed and the for/against labels sit on chatbot answers, so stance is almost confounded with source.")
    adj = rd("stance_adjudication_outcome.csv"); oc = adj.groupby(["kind", "outcome"]).size().reset_index(name="texts"); P(table(oc))
    block("Adjudication outcome", "`dataset/analysis/stance_adjudication_outcome.csv` (ids, labels and reasons; no text)", "FINAL for the labels; PENDING for the reasons", f"A reason is recorded for {int((adj['reason'] != '').sum())} of {int((adj['consensus'] != '').sum())} consensus labels. The adjudicated labels are agreed by the people who produced the earlier labels, so they are not independent.")
    rc = num("stance_reference_label_counts.csv"); P(table(rc))
    block("Reference label counts (adjudicated consensus, A only, B only)", "`dataset/analysis/stance_reference_label_counts.csv`", FINAL)
    b3 = num("stance_baseline_three_references.csv"); refs = list(dict.fromkeys(b3["reference"]))
    short = {"majority class": "majority class", "VADER features + logistic regression": "VADER", "TF-IDF (1-2 grams) + logistic regression": "TF-IDF"}
    for ref in refs:
        t = b3[b3["reference"] == ref]; P(f"*Reference: {ref}; stratified cross-validation, mean over {int(t['seeds'].iloc[0])} seeds*")
        P(table(pd.DataFrame({"subset": t["subset"], "model": t["model"].map(short), "n": t["n"].astype(int), "accuracy": t["accuracy_mean"].map(f), "macro-F1": t["macro_f1_mean"].map(f), "kappa [min, max over seeds]": [f"{f(r.kappa_vs_human_mean, 3, True)} [{f(r.kappa_vs_human_min, 2, True)}, {f(r.kappa_vs_human_max, 2, True)}]" for r in t.itertuples()]})))
    block("Stance baseline (majority class, VADER features, TF-IDF + logistic regression) against three references", "`dataset/analysis/stance_baseline_three_references.csv`, `stance_baseline_three_references_seeds.csv`", CAVEAT, "Against the adjudicated reference the all-texts kappa is mostly the chatbot-versus-news difference: within chatbot texts and within news texts both baselines are near zero. The 'majority class' row predicts the overall majority (none), so it scores low accuracy on chatbot texts. The result depends on the labeller.")
    sbp = num("stance_baseline.csv"); P(table(sbp.assign(**{c: sbp[c].map(f) for c in ("accuracy", "macro_f1", "kappa_vs_human")})))
    block("Earlier pooled reference (disputed texts excluded, before adjudication), kept for comparison", "`dataset/analysis/stance_baseline.csv`, `stance_baseline_by_labeller.csv`", "FINAL (superseded by the adjudicated reference above)")
    pdir = num("stance_prompt_direction_summary.csv"); P(table(pdir.assign(**{c: pdir[c].map(lambda x: f(x, 2)) for c in pdir.columns if c.startswith("share_")})))
    block("Chatbot stance labels against the prompt wording (a flagging check, never a label source)", "`dataset/analysis/stance_prompt_direction_summary.csv`, `stance_vs_prompt_wording.csv`, `stance_prompt_direction_flags.csv`", FINAL, "Codebook rule 5: label what the text says, not what the prompt asked, so a difference from the prompt direction is not an error in itself.")

    # ---------------------------------------------------------------------------------------------- 9 text analysis
    H(2, "9. Text analysis baseline (notebook 02)")
    vd = num("vader_news_vs_chatbot.csv"); P(table(vd.assign(**{c: vd[c].map(f) for c in ("mean_vader", "ci_low", "ci_high")})))
    block("VADER compound tone by group (300-word cut, cluster-bootstrap intervals)", "`dataset/analysis/vader_news_vs_chatbot.csv`, `vader_news_vs_chatbot.png`, `vader_by_wording.png`", "FINAL (descriptive; scored on the 300-word cut)")
    P("The word-level tables are lists, not single numbers; cite them by file: `tfidf_top_by_source_with_news.csv` (top TF-IDF terms per group), `ngrams_top_news.csv` and `ngrams_top.csv` (most frequent n-grams), `collocations_news.csv` and `collocations_by_chatbot.csv` (PMI and log-likelihood collocations), `chatbot_vs_news_bigram_log_odds.csv` (distinctive bigrams, z-scores). Status: FINAL, descriptive, 300-word cut; the collocation and log-odds tables are not corrected for the shared topic words in the prompts.")

    # ---------------------------------------------------------------------------------------------- 10 figures
    H(2, "10. Figures")
    figs = [("composition_by_frame.png", "Mean share of hits per frame for Llama, Qwen and the four news regions, with 95% intervals", "05", FINAL),
            ("h1_window_length_histograms.png", "Word counts of the topic-selected news windows against the chatbot answers they are matched to", "05", FINAL),
            ("frame_mix_by_group.png", "Frame mix per chatbot and wording and per news region (300-word cut)", "03", "FINAL, descriptive (300-word cut)"),
            ("vader_news_vs_chatbot.png", "VADER tone by group with intervals", "02", "FINAL, descriptive"),
            ("vader_by_wording.png", "VADER tone of chatbot answers by prompt wording", "02", "FINAL, descriptive")]
    P(table(pd.DataFrame([{"figure": f"`dataset/analysis/{n}`", "shows": s, "notebook": nb, "status": st, "file present": (A / n).exists()} for n, s, nb, st in figs])))
    P("There is no figure for H1 in the repository. If the report needs one, draw it from `h1_main.csv` and `h1_robustness_summary.csv` (difference with interval, one row per run).")

    # ---------------------------------------------------------------------------------------------- 11 pending
    H(2, "11. Still pending, or to state in the report")
    for i, (t, d) in enumerate(pending_list(), 1): P(f"{i}. **{t}.** {d}")
    Path("docs").mkdir(exist_ok=True)
    (Path("docs") / "report_numbers.md").write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    print("written docs/report_numbers.md:", len(L), "lines")


if __name__ == "__main__":
    build()
