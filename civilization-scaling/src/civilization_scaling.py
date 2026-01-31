#!/usr/bin/env python3
"""
Scaling Civilization: Energy, Coordination, Memory, and Replication Metrics
Multi-lane log-time timeline (1M Years Ago to 2030+)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import os


def load_data():
    """Load civilization metrics from CSV."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'data', 'civilization_metrics.csv')
    return pd.read_csv(csv_path)


def get_lane_data(df, lane_name):
    """Extract data for a specific lane as list of tuples."""
    lane_df = df[df['Lane'] == lane_name].copy()
    data = []
    for _, row in lane_df.iterrows():
        data.append((
            row['Event'],
            row['Years_Ago'],
            row['Metric_Value'],
            row['Era'],
            row['Impact'],
            row['Phase_Flip'] if pd.notna(row['Phase_Flip']) else ""
        ))
    return data

# Colors
LANE_COLORS = {
    "Energy": "#E67E22",        # Orange
    "Coordination": "#27AE60",  # Green
    "Memory": "#3498DB",        # Blue
    "Replication": "#9B59B6",   # Purple
    "Latency": "#E74C3C",       # Red (overlay)
}

ERA_COLORS = {
    "Prehistory": "#D5D8DC",
    "Neolithic": "#AED6F1",
    "Ancient": "#F9E79F",
    "Pre-Modern": "#FADBD8",
    "Industrial": "#FAD7A0",
    "Modern": "#D5F5E3",
    "Digital": "#E8DAEF",
    "Future": "#FDEDEC",
}

IMPACT_SIZES = {
    "Transformative": 150,
    "High": 90,
    "Medium": 50,
    "Low": 30,
    "Speculative": 80,
}


def years_ago_to_log_x(years_ago):
    """Convert years ago to log x position (reversed: left=old, right=recent)."""
    return -np.log10(years_ago + 1)  # Negative so older is left


def create_multilane_plot(df):
    """Create multi-lane civilization scaling plot."""

    fig, axes = plt.subplots(4, 1, figsize=(18, 14), sharex=True, dpi=150)
    fig.patch.set_facecolor('white')

    # Load data for each lane from CSV
    energy_data = get_lane_data(df, "Energy")
    coordination_data = get_lane_data(df, "Coordination")
    memory_data = get_lane_data(df, "Memory")
    replication_data = get_lane_data(df, "Replication")

    lanes = [
        ("Energy", energy_data, "kcal/person/day", axes[0], True),
        ("Coordination", coordination_data, "Max Stable Group Size", axes[1], True),
        ("Memory", memory_data, "bits/person (accessible)", axes[2], True),
        ("Replication", replication_data, "hours/copy (cost)", axes[3], False),  # Inverted
    ]

    # Phase flip events (vertical lines)
    phase_flips = [
        (800000, "Fire/Cooking\n→ Brains"),
        (250000, "Language\n→ Myths"),
        (12000, "Agriculture\n→ Cities"),
        (5000, "Writing\n→ Institutions"),
        (574, "Printing\n→ Science"),
        (264, "Steam\n→ Industry"),
        (44, "Internet\n→ Global"),
        (4, "AI\n→ Automation"),
    ]

    for lane_name, data, ylabel, ax, upward in lanes:
        ax.set_facecolor('#FAFAFA')
        color = LANE_COLORS[lane_name]

        # Add era shading
        era_spans = [
            (1000000, 12000, "Prehistory"),
            (12000, 5000, "Neolithic"),
            (5000, 500, "Ancient"),
            (500, 200, "Pre-Modern"),
            (200, 50, "Industrial"),
            (50, 10, "Modern"),
            (10, 0.1, "Digital"),
        ]
        for start, end, era in era_spans:
            x0 = years_ago_to_log_x(start)
            x1 = years_ago_to_log_x(end)
            ax.axvspan(x0, x1, alpha=0.3, color=ERA_COLORS.get(era, '#EEE'), zorder=0)

        # Plot data points
        x_vals = [years_ago_to_log_x(d[1]) for d in data]
        y_vals = [d[2] for d in data]
        impacts = [d[4] for d in data]
        sizes = [IMPACT_SIZES.get(imp, 50) for imp in impacts]
        labels = [d[0] for d in data]
        phase_notes = [d[5] for d in data]

        # Connect with line
        ax.plot(x_vals, y_vals, '-', color=color, alpha=0.4, linewidth=1.5, zorder=1)

        # Scatter
        for i, (x, y, s, lbl, imp, pn) in enumerate(zip(x_vals, y_vals, sizes, labels, impacts, phase_notes)):
            marker = 'd' if imp == "Speculative" else 'o'
            edgecolor = 'white' if imp != "Speculative" else '#333'
            alpha = 0.7 if imp == "Speculative" else 1.0
            ax.scatter(x, y, c=color, s=s, marker=marker, alpha=alpha,
                      edgecolors=edgecolor, linewidths=1.5, zorder=3)

        # Add labels for key events
        label_subset = ["Fire/Cooking", "Agriculture", "Steam", "Electricity", "Internet", "AI",
                       "Language", "City-States", "Writing", "Printing", "PCs", "AI Synthesis",
                       "Factory", "Digital", "AI Gen", "Telegraph"]
        for i, (x, y, lbl, imp) in enumerate(zip(x_vals, y_vals, labels, impacts)):
            if any(key in lbl for key in label_subset) or imp == "Transformative":
                fontsize = 7
                y_offset = 1.3 if upward else 0.7
                va = 'bottom' if upward else 'top'
                ax.annotate(lbl, xy=(x, y), xytext=(x, y * y_offset),
                           fontsize=fontsize, ha='center', va=va, alpha=0.8,
                           rotation=30 if x < -4 else 0)

        ax.set_yscale('log')
        ax.set_ylabel(f"{lane_name}\n({ylabel})", fontsize=10, fontweight='bold', color=color)
        ax.tick_params(axis='y', labelsize=8)
        ax.grid(True, which='major', axis='y', linestyle='-', alpha=0.2)

        # Lane title
        ax.text(0.02, 0.95, lane_name, transform=ax.transAxes, fontsize=12,
               fontweight='bold', color=color, va='top')

    # Add phase flip lines across all axes
    for years_ago, label in phase_flips:
        x = years_ago_to_log_x(years_ago)
        for ax in axes:
            ax.axvline(x, color='#888', linestyle='--', alpha=0.5, linewidth=1, zorder=2)
        # Label at top
        axes[0].annotate(label, xy=(x, axes[0].get_ylim()[1]), xytext=(x, axes[0].get_ylim()[1] * 1.5),
                        fontsize=6, ha='center', va='bottom', alpha=0.7, color='#555',
                        rotation=45)

    # X-axis configuration (bottom panel)
    ax_bottom = axes[-1]

    # Custom x-ticks showing years ago
    tick_years = [1000000, 100000, 10000, 1000, 100, 10, 1]
    tick_positions = [years_ago_to_log_x(y) for y in tick_years]
    tick_labels = ['1M', '100K', '10K', '1K', '100', '10', 'Now']

    ax_bottom.set_xticks(tick_positions)
    ax_bottom.set_xticklabels(tick_labels, fontsize=10)
    ax_bottom.set_xlabel('Years Ago (Log Scale) – Prehistory Compressed, Modern Expanded',
                        fontsize=12, fontweight='bold')

    # Set x limits
    for ax in axes:
        ax.set_xlim(years_ago_to_log_x(1200000), years_ago_to_log_x(0.05))

    # Main title
    fig.suptitle('Scaling Civilization: Energy, Coordination, Memory, and Replication\n(1M Years Ago → 2030+)',
                fontsize=16, fontweight='bold', y=0.98)

    # Perspective notes
    perspective_notes = [
        ("Most human existence:\npre-writing (>99%)", 0.15, 0.02),
        ("Agriculture: only\n~12K years", 0.45, 0.02),
        ("Internet: a blink\n(~30 years)", 0.85, 0.02),
    ]
    for note, x_pos, y_pos in perspective_notes:
        fig.text(x_pos, y_pos, note, fontsize=8, style='italic', alpha=0.6,
                ha='center', va='bottom')

    # Footnote
    footnote = ("Log-time compresses prehistory, expands modern acceleration. "
                "S-curves per domain show stacking leaps. Metrics approximate/qualitative pre-1800. "
                "Inspired by: Herculano-Houzel (neurons), Kaplan/Charnov (LHT/OFT), Kurzweil (efficiency). "
                "Sources: OWID, ethnographic data, historical timelines. Jan 2026.")
    fig.text(0.5, -0.02, footnote, ha='center', fontsize=7, style='italic', alpha=0.6,
            wrap=True)

    # Legend
    legend_elements = [
        mpatches.Patch(color=LANE_COLORS["Energy"], label='Energy (kcal/person)'),
        mpatches.Patch(color=LANE_COLORS["Coordination"], label='Coordination (group size)'),
        mpatches.Patch(color=LANE_COLORS["Memory"], label='Memory (bits/person)'),
        mpatches.Patch(color=LANE_COLORS["Replication"], label='Replication (cost ↓)'),
        Line2D([0], [0], linestyle='--', color='#888', label='Phase Flip'),
    ]
    fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.95),
              fontsize=8, framealpha=0.9)

    plt.tight_layout(rect=[0, 0.04, 1, 0.95])

    return fig


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Load data from CSV
    df = load_data()
    print(f"Loaded {len(df)} records from CSV")

    fig = create_multilane_plot(df)
    print("Created civilization scaling plot")

    fig.savefig(os.path.join(output_dir, 'civilization_scaling.png'), dpi=300,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved: civilization_scaling.png")

    fig.savefig(os.path.join(output_dir, 'civilization_scaling.svg'), format='svg',
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved: civilization_scaling.svg")

    fig.savefig(os.path.join(output_dir, 'civilization_scaling_highres.png'), dpi=400,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved: civilization_scaling_highres.png")

    print("\nDone!")


if __name__ == '__main__':
    main()
