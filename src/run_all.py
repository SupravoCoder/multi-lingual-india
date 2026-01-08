import json
import sys
from pathlib import Path
from typing import List
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.utils.tokenization_analysis import analyze_tokenization
from src.eval.classification_eval import per_lang_accuracy, simulate_imbalance, overall_and_per_lang
from src.utils.plotting import plot_grouped_bar, plot_single_bar

DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"


def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)


def run_tokenization(models: List[str]) -> pd.DataFrame:
    lid = load_csv("lid_samples.csv")
    rows = []
    for m in models:
        for lang in sorted(lid["lang"].unique()):
            texts = lid[lid["lang"] == lang]["text"].tolist()
            stats = analyze_tokenization(m, texts)
            rows.append({"model": m, "lang": lang, **stats})
    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "tokenization_stats.csv", index=False)
    plot_grouped_bar(df, x_col="lang", y_col="avg_tokens", hue_col="model", title="Avg tokens per text", ylabel="Avg tokens", out_path=OUT_DIR / "tokenization_avg_tokens.png")
    plot_grouped_bar(df, x_col="lang", y_col="unk_rate", hue_col="model", title="UNK rate", ylabel="UNK rate", out_path=OUT_DIR / "tokenization_unk_rate.png")
    return df


def run_lid(models: List[str]) -> pd.DataFrame:
    lid = load_csv("lid_samples.csv")
    rows = []
    for m in models:
        overall, per_lang = overall_and_per_lang(m, lid, "lang")
        rows.append({"model": m, "lang": "overall", "accuracy": overall})
        for lang, acc in per_lang.items():
            rows.append({"model": m, "lang": lang, "accuracy": acc})
    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "lid_accuracy.csv", index=False)
    plot_grouped_bar(df, x_col="lang", y_col="accuracy", hue_col="model", title="LID accuracy", ylabel="Accuracy", out_path=OUT_DIR / "lid_accuracy.png")
    return df


def run_news(models: List[str]) -> pd.DataFrame:
    news = load_csv("news_samples.csv")
    rows = []
    for m in models:
        overall, per_lang = overall_and_per_lang(m, news, "label")
        rows.append({"model": m, "lang": "overall", "accuracy": overall})
        for lang, acc in per_lang.items():
            rows.append({"model": m, "lang": lang, "accuracy": acc})
    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "news_accuracy.csv", index=False)
    plot_grouped_bar(df, x_col="lang", y_col="accuracy", hue_col="model", title="News classification accuracy", ylabel="Accuracy", out_path=OUT_DIR / "news_accuracy.png")
    return df


def run_imbalance(models: List[str], minority: str, frac: float) -> pd.DataFrame:
    news = load_csv("news_samples.csv")
    rows = []
    for m in models:
        res = simulate_imbalance(m, news, "label", minority_lang=minority, minority_frac=frac)
        rows.append({"model": m, "overall_accuracy": res["overall_acc"], "minority": minority, "fraction": frac})
    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "imbalance_overall.csv", index=False)
    plot_single_bar(df, x_col="model", y_col="overall_accuracy", title=f"Imbalance overall acc (minority={minority}, frac={frac})", ylabel="Accuracy", out_path=OUT_DIR / "imbalance_overall.png")
    return df


def main():
    models = ["bert-base-multilingual-cased", "xlm-roberta-base", "google/muril-base-cased"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    token_df = run_tokenization(models)
    lid_df = run_lid(models)
    news_df = run_news(models)
    imb_df = run_imbalance(models, minority="hi", frac=0.3)

    summary = {
        "tokenization": token_df.to_dict(orient="records"),
        "lid": lid_df.to_dict(orient="records"),
        "news": news_df.to_dict(orient="records"),
        "imbalance": imb_df.to_dict(orient="records"),
    }
    with open(OUT_DIR / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print("Run complete. Artifacts in outputs/.")


if __name__ == "__main__":
    main()
