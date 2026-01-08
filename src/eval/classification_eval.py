from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModel
import torch


def _embed_texts(model_name: str, texts: List[str]) -> np.ndarray:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()

    embs = []
    with torch.no_grad():
        for t in texts:
            enc = tokenizer(t, return_tensors="pt", truncation=True, max_length=128)
            out = model(**enc)
            # Use CLS token (first token) representation or pooled_output if available
            if hasattr(out, "pooler_output") and out.pooler_output is not None:
                vec = out.pooler_output.squeeze(0)
            else:
                vec = out.last_hidden_state[:, 0, :].squeeze(0)
            embs.append(vec.cpu().numpy())
    return np.vstack(embs)


def train_eval_linear(model_name: str, df: pd.DataFrame, label_col: str) -> Dict[str, float]:
    texts = df["text"].tolist()
    labels = df[label_col].tolist()
    X = _embed_texts(model_name, texts)
    y = np.array(labels)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

    clf = LogisticRegression(max_iter=200, n_jobs=1)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)

    return {"overall_acc": acc}


def overall_and_per_lang(model_name: str, df: pd.DataFrame, label_col: str) -> Tuple[float, Dict[str, float]]:
    """Train a linear classifier once and return overall + per-language accuracy (on held-out set)."""
    texts = df["text"].tolist()
    labels = df[label_col].tolist()
    langs = df["lang"].tolist()

    X = _embed_texts(model_name, texts)
    y = np.array(labels)
    lang_arr = np.array(langs)
    indices = np.arange(len(y))

    train_idx, test_idx, y_train, y_test = train_test_split(
        indices, y, test_size=0.3, stratify=y, random_state=42
    )

    clf = LogisticRegression(max_iter=200, n_jobs=1)
    clf.fit(X[train_idx], y_train)
    preds = clf.predict(X[test_idx])
    overall = accuracy_score(y_test, preds)

    per_lang = {}
    for lang in sorted(np.unique(lang_arr[test_idx])):
        mask = lang_arr[test_idx] == lang
        per_lang[lang] = accuracy_score(y_test[mask], preds[mask])

    return overall, per_lang


def per_lang_accuracy(model_name: str, df: pd.DataFrame, label_col: str) -> Dict[str, float]:
    results = {}
    for lang in sorted(df["lang"].unique()):
        sub = df[df["lang"] == lang]
        if len(sub) < 4:
            results[lang] = float("nan")
            continue
        metrics = train_eval_linear(model_name, sub, label_col)
        results[lang] = metrics["overall_acc"]
    return results


def simulate_imbalance(model_name: str, df: pd.DataFrame, label_col: str, minority_lang: str, minority_frac: float = 0.3) -> Dict[str, float]:
    # Downsample minority_lang
    majority = df[df["lang"] != minority_lang]
    minority = df[df["lang"] == minority_lang]
    n_keep = max(1, int(len(minority) * minority_frac))
    minority_ds = minority.sample(n=n_keep, random_state=42)
    imbalanced = pd.concat([majority, minority_ds], ignore_index=True)

    return train_eval_linear(model_name, imbalanced, label_col)
