import argparse
import pandas as pd
from pathlib import Path
from typing import List

from src.utils.tokenization_analysis import analyze_tokenization
from src.utils.script_detect import detect_script, is_code_mixed
from src.eval.classification_eval import per_lang_accuracy, simulate_imbalance, overall_and_per_lang

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)


def run_tokenization(models: List[str]):
    lid = load_csv("lid_samples.csv")
    texts_by_lang = {l: lid[lid["lang"] == l]["text"].tolist() for l in lid["lang"].unique()}
    print("Tokenization analysis:")
    for m in models:
        print(f"\nModel: {m}")
        for l, texts in texts_by_lang.items():
            stats = analyze_tokenization(m, texts)
            print(f"  {l}: avg_tokens={stats['avg_tokens']:.2f}, unk_rate={stats['unk_rate']:.4f}")


def run_lid(models: List[str]):
    lid = load_csv("lid_samples.csv")
    for m in models:
        print(f"\nModel: {m} (LID)")
        overall, per_lang = overall_and_per_lang(m, lid, "lang")
        print(f"  overall: acc={overall:.3f}")
        for l, acc in per_lang.items():
            print(f"  {l}: acc={acc:.3f}")


def run_news(models: List[str]):
    news = load_csv("news_samples.csv")
    for m in models:
        print(f"\nModel: {m} (News Classification)")
        overall, per_lang = overall_and_per_lang(m, news, "label")
        print(f"  overall: acc={overall:.3f}")
        for l, acc in per_lang.items():
            print(f"  {l}: acc={acc:.3f}")


def run_imbalance(models: List[str], minority: str, frac: float):
    news = load_csv("news_samples.csv")
    for m in models:
        print(f"\nModel: {m} (Imbalance: minority={minority}, frac={frac})")
        res = simulate_imbalance(m, news, "label", minority_lang=minority, minority_frac=frac)
        print(f"  overall_acc={res['overall_acc']:.3f}")


def run_script_smoke():
    lid = load_csv("lid_samples.csv")
    print("Script detection smoke test:")
    for i, row in lid.head(9).iterrows():
        s = detect_script(row["text"]) or "none"
        cm = is_code_mixed(row["text"])
        print(f"  text[{row['lang']}]: script={s}, code_mixed={cm}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["tokenization", "lid", "news", "imbalance", "smoke"], required=True)
    parser.add_argument("--models", nargs="+", default=["bert-base-multilingual-cased", "xlm-roberta-base", "google/muril-base-cased"])
    parser.add_argument("--minority", default="hi")
    parser.add_argument("--minority_frac", type=float, default=0.3)
    args = parser.parse_args()

    if args.task == "tokenization":
        run_tokenization(args.models)
    elif args.task == "lid":
        run_lid(args.models)
    elif args.task == "news":
        run_news(args.models)
    elif args.task == "imbalance":
        run_imbalance(args.models, args.minority, args.minority_frac)
    elif args.task == "smoke":
        run_script_smoke()


if __name__ == "__main__":
    main()
