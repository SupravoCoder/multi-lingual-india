from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.utils.script_detect import detect_script, is_code_mixed

DATA = Path(__file__).resolve().parent.parent / "data" / "lid_samples.csv"

def main():
    df = pd.read_csv(DATA)
    print("Script detection smoke test:")
    for i, row in df.head(12).iterrows():
        s = detect_script(row["text"]) or "none"
        cm = is_code_mixed(row["text"])
        print(f"  [{row['lang']}] -> script={s}, code_mixed={cm} | {row['text'][:40]}")

if __name__ == "__main__":
    main()
