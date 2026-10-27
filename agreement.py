"""Agreement between two labelings (human vs dictionary, or human vs human): accuracy, Cohen's kappa, per-class precision/recall.

y_true is the reference (the human labels, or labeller A); y_pred is what is being checked (the dictionary, or labeller B).
Kappa is symmetric; precision and recall are not (swap the arguments to swap their meaning).
"""
import numpy as np
import pandas as pd


def confusion(y_true, y_pred, labels):
    t, p = pd.Categorical(y_true, categories=labels), pd.Categorical(y_pred, categories=labels)
    return pd.crosstab(t, p, dropna=False, rownames=["reference"], colnames=["checked"])


def cohen_kappa(y1, y2, labels=None):
    """kappa = (p_observed - p_expected) / (1 - p_expected). 1 = perfect, 0 = chance level, negative = worse than chance."""
    y1, y2 = np.asarray(y1), np.asarray(y2)
    if len(y1) != len(y2) or len(y1) == 0:
        raise ValueError("label lists must have the same non-zero length")
    labels = list(labels) if labels is not None else sorted(set(y1) | set(y2))
    p_obs = float(np.mean(y1 == y2))
    p_exp = sum(float(np.mean(y1 == k)) * float(np.mean(y2 == k)) for k in labels)
    if p_exp >= 1.0:
        return 1.0 if p_obs == 1.0 else float("nan")
    return (p_obs - p_exp) / (1.0 - p_exp)


def per_class_report(y_true, y_pred, labels):
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    rows = []
    for k in labels:
        tp = int(np.sum((y_true == k) & (y_pred == k))); n_ref = int(np.sum(y_true == k)); n_pred = int(np.sum(y_pred == k))
        prec = tp / n_pred if n_pred else float("nan"); rec = tp / n_ref if n_ref else float("nan")
        f1 = 2 * prec * rec / (prec + rec) if (prec == prec and rec == rec and prec + rec > 0) else float("nan")
        rows.append({"label": k, "n_reference": n_ref, "n_checked": n_pred, "true_positive": tp, "precision": prec, "recall": rec, "f1": f1})
    return pd.DataFrame(rows)


def agreement_report(y_true, y_pred, labels):
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    return {"n": int(len(y_true)), "accuracy": float(np.mean(y_true == y_pred)), "kappa": cohen_kappa(y_true, y_pred, labels),
            "per_class": per_class_report(y_true, y_pred, labels), "confusion": confusion(y_true, y_pred, labels)}
