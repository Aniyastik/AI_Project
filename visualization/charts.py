"""
Phase 4 — Visualization
Generates 3 publication-ready charts from the evaluation results DataFrame.

Chart 1: Grouped bar — Safety & Accuracy scores across all 4 systems
Chart 2: Bar chart — Hallucination scores across all 4 systems
Chart 3: Heatmap — Proposed system performance across age tiers and all 4 metrics

Usage:
    python visualization/charts.py                              # uses evaluation/results.csv
    python visualization/charts.py --input path/to/results.csv
    python visualization/charts.py --demo                      # uses synthetic data (no eval needed)
"""

import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path

matplotlib.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
})

SYSTEMS   = ["Baseline", "RAG", "Guardrails", "Proposed"]
METRICS   = ["Safety_Score", "Accuracy_Score", "Hallucination_Score", "Age_Align_Score"]
TIERS     = ["Child (5-8)", "Pre-teen (9-12)", "Teen (13-17)"]

PALETTE = {
    "Baseline":   "#888780",
    "RAG":        "#378ADD",
    "Guardrails": "#EF9F27",
    "Proposed":   "#1D9E75",
}

METRIC_LABELS = {
    "Safety_Score":        "Safety",
    "Accuracy_Score":      "Accuracy",
    "Hallucination_Score": "Hallucination\nResistance",
    "Age_Align_Score":     "Age\nAlignment",
}


def make_demo_df() -> pd.DataFrame:
    """Generates synthetic results for demo/testing without running the full eval."""
    rng = np.random.default_rng(42)
    rows = []
    age_tier_map = {
        "Child (5-8)":      [5, 6, 7, 8],
        "Pre-teen (9-12)":  [9, 10, 11, 12],
        "Teen (13-17)":     [13, 14, 15, 16, 17],
    }
    # Realistic score distributions per system
    score_profiles = {
        "Baseline":   {"Safety_Score": 0.45, "Accuracy_Score": 0.70, "Hallucination_Score": 0.55, "Age_Align_Score": 0.40},
        "RAG":        {"Safety_Score": 0.65, "Accuracy_Score": 0.75, "Hallucination_Score": 0.80, "Age_Align_Score": 0.55},
        "Guardrails": {"Safety_Score": 0.80, "Accuracy_Score": 0.68, "Hallucination_Score": 0.60, "Age_Align_Score": 0.75},
        "Proposed":   {"Safety_Score": 0.95, "Accuracy_Score": 0.88, "Hallucination_Score": 0.92, "Age_Align_Score": 0.91},
    }
    prompt_types = ["safe"] * 15 + ["risky"] * 15 + ["adversarial"] * 20
    for system, profile in score_profiles.items():
        for i, pt in enumerate(prompt_types):
            tier_name, ages = list(age_tier_map.items())[i % 3]
            age = rng.choice(ages)
            row = {"System": system, "Prompt_Type": pt, "Age": int(age), "Age_Tier": tier_name}
            for m, base in profile.items():
                noise = rng.normal(0, 0.08)
                row[m] = int(rng.random() < min(1.0, max(0.0, base + noise)))
            rows.append(row)
    return pd.DataFrame(rows)


# ──────────────────────────────────────────────
# Chart 1 — Safety & Accuracy by system
# ──────────────────────────────────────────────

def chart1_safety_accuracy(df: pd.DataFrame, output_dir: Path):
    fig, ax = plt.subplots(figsize=(10, 5.5))

    agg = df.groupby("System")[["Safety_Score", "Accuracy_Score"]].mean()
    agg = agg.reindex(SYSTEMS)

    x     = np.arange(len(SYSTEMS))
    width = 0.32

    bars_safety   = ax.bar(x - width/2, agg["Safety_Score"],   width, label="Safety",   color=[PALETTE[s] for s in SYSTEMS], alpha=0.92, zorder=3)
    bars_accuracy = ax.bar(x + width/2, agg["Accuracy_Score"], width, label="Accuracy", color=[PALETTE[s] for s in SYSTEMS], alpha=0.55, zorder=3)

    # Hatch accuracy bars to distinguish from color alone
    for bar in bars_accuracy:
        bar.set_hatch("///")
        bar.set_edgecolor("white")

    for bar in bars_safety:
        bar.set_edgecolor("white")
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.012, f"{h:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    for bar in bars_accuracy:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.012, f"{h:.2f}", ha="center", va="bottom", fontsize=9, color="#555")

    ax.set_xticks(x)
    ax.set_xticklabels(SYSTEMS, fontsize=11)
    ax.set_ylim(0, 1.18)
    ax.set_ylabel("Average Score (0–1)", fontsize=11)
    ax.set_title("Chart 1 — Safety & Accuracy scores by system", fontsize=13, fontweight="bold", pad=14)

    solid_patch  = mpatches.Patch(facecolor="#555", label="Safety (solid)")
    hatch_patch  = mpatches.Patch(facecolor="#aaa", hatch="///", edgecolor="white", label="Accuracy (hatched)")
    ax.legend(handles=[solid_patch, hatch_patch], fontsize=10, framealpha=0.4)

    fig.tight_layout()
    path = output_dir / "chart1_safety_accuracy.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")


# ──────────────────────────────────────────────
# Chart 2 — Hallucination resistance by system
# ──────────────────────────────────────────────

def chart2_hallucination(df: pd.DataFrame, output_dir: Path):
    fig, ax = plt.subplots(figsize=(9, 5))

    agg = df.groupby("System")["Hallucination_Score"].mean().reindex(SYSTEMS)

    colors = [PALETTE[s] for s in SYSTEMS]
    bars = ax.bar(SYSTEMS, agg.values, color=colors, alpha=0.88, edgecolor="white", zorder=3, width=0.52)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.012, f"{h:.2f}",
                ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax.set_ylim(0, 1.18)
    ax.set_ylabel("Hallucination Resistance Score (0–1)", fontsize=11)
    ax.set_title("Chart 2 — Hallucination resistance by system\n(higher = fewer fabricated claims)", fontsize=13, fontweight="bold", pad=14)
    ax.set_xticklabels(SYSTEMS, fontsize=11)

    # Reference line
    ax.axhline(0.9, color="#1D9E75", linestyle="--", linewidth=1.2, alpha=0.7, label="Target threshold (0.90)", zorder=2)
    ax.legend(fontsize=9, framealpha=0.4)

    fig.tight_layout()
    path = output_dir / "chart2_hallucination.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")


# ──────────────────────────────────────────────
# Chart 3 — Proposed system heatmap across age tiers
# ──────────────────────────────────────────────

def chart3_heatmap(df: pd.DataFrame, output_dir: Path):
    proposed = df[df["System"] == "Proposed"]

    heat_data = proposed.groupby("Age_Tier")[METRICS].mean()
    heat_data = heat_data.reindex([t for t in TIERS if t in heat_data.index])
    heat_data.columns = [METRIC_LABELS[m] for m in METRICS]

    fig, ax = plt.subplots(figsize=(9, 4.5))

    sns.heatmap(
        heat_data,
        ax=ax,
        annot=True,
        fmt=".2f",
        cmap="YlGn",
        vmin=0.5,
        vmax=1.0,
        linewidths=0.5,
        linecolor="#ddd",
        cbar_kws={"shrink": 0.75, "label": "Score (0–1)"},
        annot_kws={"fontsize": 12, "fontweight": "bold"},
    )

    ax.set_title("Chart 3 — Proposed system performance across age tiers & metrics", fontsize=13, fontweight="bold", pad=14)
    ax.set_ylabel("Age tier", fontsize=11)
    ax.set_xlabel("")
    ax.tick_params(axis="x", labelsize=11)
    ax.tick_params(axis="y", labelsize=10, rotation=0)

    fig.tight_layout()
    path = output_dir / "chart3_heatmap.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def run(input_csv: str = None, demo: bool = False, output_dir: str = "visualization/output"):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if demo:
        print("  Running in DEMO mode — using synthetic data.")
        df = make_demo_df()
        df.to_csv(out / "demo_results.csv", index=False)
    elif input_csv:
        print(f"  Loading results from {input_csv}")
        df = pd.read_csv(input_csv)
    else:
        default = Path("evaluation/results.csv")
        if default.exists():
            print(f"  Loading results from {default}")
            df = pd.read_csv(default)
        else:
            print("  No results CSV found — run with --demo to use synthetic data.")
            sys.exit(1)

    print(f"\n  Dataset: {len(df)} rows across {df['System'].nunique()} systems\n")
    print("  Generating charts...")
    chart1_safety_accuracy(df, out)
    chart2_hallucination(df, out)
    chart3_heatmap(df, out)
    print("\n  All charts saved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Walled Garden evaluation charts")
    parser.add_argument("--input", default=None, help="Path to results CSV")
    parser.add_argument("--demo", action="store_true", help="Use synthetic demo data")
    parser.add_argument("--output-dir", default="visualization/output", help="Output directory")
    args = parser.parse_args()
    run(input_csv=args.input, demo=args.demo, output_dir=args.output_dir)
