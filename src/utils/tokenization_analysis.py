from typing import Dict, List, Tuple
from transformers import AutoTokenizer
from collections import Counter


def analyze_tokenization(model_name: str, texts: List[str]) -> Dict[str, float]:
    """Compute tokenization stats for a model over a list of texts.
    Returns dict with avg_tokens, unk_rate, vocab_overlap_est.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    unk_token = tokenizer.unk_token
    total_tokens = 0
    unk_tokens = 0

    for t in texts:
        toks = tokenizer.tokenize(t)
        total_tokens += len(toks)
        unk_tokens += sum(1 for tok in toks if tok == unk_token)

    avg_tokens = total_tokens / max(len(texts), 1)
    unk_rate = unk_tokens / max(total_tokens, 1)

    return {
        "avg_tokens": avg_tokens,
        "unk_rate": unk_rate,
    }
