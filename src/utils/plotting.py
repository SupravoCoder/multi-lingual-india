from pathlib import Path
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

plt.switch_backend("Agg")


def plot_grouped_bar(df: pd.DataFrame, x_col: str, y_col: str, hue_col: str, title: str, ylabel: str, out_path: Path):
    """Create grouped bar chart."""
    fig, ax = plt.subplots(figsize=(8, 5))
    models = sorted(df[hue_col].unique())
    langs = sorted(df[x_col].unique())
    width = 0.8 / max(len(models), 1)
    for i, m in enumerate(models):
        vals = [df[(df[x_col] == l) & (df[hue_col] == m)][y_col].mean() for l in langs]
        positions = [j + i * width for j in range(len(langs))]
        ax.bar(positions, vals, width=width, label=m)
    ax.set_xticks([j + width * (len(models) - 1) / 2 for j in range(len(langs))])
    ax.set_xticklabels(langs)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def plot_single_bar(df: pd.DataFrame, x_col: str, y_col: str, title: str, ylabel: str, out_path: Path):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df[x_col], df[y_col])
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
