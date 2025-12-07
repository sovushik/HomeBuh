from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List

def generate_bar_chart(labels: List[str], values: List[float], out_path: Path):
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(labels, values, color="#4c78a8")
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("Amount")
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path

def generate_line_chart(labels: List[str], values: List[float], out_path: Path):
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(labels, values, marker='o', color="#4c78a8")
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("Amount")
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path

def generate_pie_chart(labels: List[str], values: List[float], out_path: Path):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(values, labels=labels, autopct='%1.1f%%', colors=plt.cm.tab20.colors)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path
