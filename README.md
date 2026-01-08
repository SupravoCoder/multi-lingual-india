# Evaluating Cross-Lingual Performance Gaps in Multilingual Models for Indian Languages

This mini-project evaluates multilingual models (mBERT, XLM-R, IndicBERT) across Hindi, Bengali, and Tamil on:
- Language Identification (LID)
- Simple News Category Classification (politics, sports, business)
- Tokenization behavior (subword length, unknown token rate)
- Script-level errors
- Data imbalance effects

## Quick Start

### 1) Create/activate a Python environment, then install deps
```bash
# From the project root
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run a smoke test (script detection only)
```bash
python scripts/smoke_test.py
```

### 3) Run tokenization analysis (download models as needed)
```bash
python src/main.py --task tokenization --models bert-base-multilingual-cased xlm-roberta-base google/muril-base-cased
```

### 4) Run LID and classification evaluations
```bash
# Language ID
python src/main.py --task lid --models bert-base-multilingual-cased xlm-roberta-base google/muril-base-cased

# News classification
python src/main.py --task news --models bert-base-multilingual-cased xlm-roberta-base google/muril-base-cased
```

### 5) Simulate imbalance
```bash
python src/main.py --task imbalance --models bert-base-multilingual-cased xlm-roberta-base google/muril-base-cased --minority hi --minority_frac 0.3
```

### 6) Run everything and produce plots
```bash
python src/run_all.py
```
Artifacts land in `outputs/`:
- tokenization_stats.csv, tokenization_avg_tokens.png, tokenization_unk_rate.png
- lid_accuracy.csv, lid_accuracy.png
- news_accuracy.csv, news_accuracy.png
- imbalance_overall.csv, imbalance_overall.png

## Outputs
- Prints per-language accuracies for LID/news classification
- Reports tokenization stats (avg tokens, [UNK] rate)
- Shows impact of imbalance on accuracy

## Notes
- Models will be downloaded on first run.
- IndicBERT identifier may vary; if `ai4bharat/indic-bert` fails, try `ai4bharat/indic-bert-base`.
 - If you prefer IndicBERT and have access, swap `google/muril-base-cased` for your IndicBERT identifier.
- No heavy fine-tuning: we train only shallow linear classifiers on frozen embeddings.
