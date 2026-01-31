#!/usr/bin/env python3
"""
Energy Leverage per Person – Static Matplotlib Chart
Clean export for PNG/SVG with minimal annotations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Constants
METABOLIC_BASELINE_GJ = 3.6  # GJ/person/year
METABOLIC_BASELINE_W = 114.08  # Watts (continuous equivalent)

# Era markers (reduced set for cleaner static export)
ERA_MARKERS = [
    (1750, "Coal/Steam"),
    (1950, "Acceleration"),
]


def load_data():
    """Load CSV data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(os.path.dirname(script_dir), 'data', 'energy_leverage_datapoints.csv')
    return pd.read_csv(data_path)


def create_static_chart(df):
    """Create clean matplotlib chart for static export."""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#FAFAFA')

    # Total energy line
    ax.plot(df['year'], df['watts_per_person'],
            'o-', color='#E67E22', linewidth=2.5, markersize=8,
            markeredgecolor='white', markeredgewidth=1.5,
            label='Total Energy', zorder=3)

    # External energy line
    ax.plot(df['year'], df['watts_external'],
            'o-', color='#3498DB', linewidth=2.5, markersize=8,
            markeredgecolor='white', markeredgewidth=1.5,
            label='External Energy', zorder=3)

    # Metabolic baseline reference line
    ax.axhline(y=METABOLIC_BASELINE_W, color='#888', linestyle=':',
               linewidth=1.5, label=f'Metabolic (~{METABOLIC_BASELINE_W:.0f} W)', zorder=1)

    # Era markers (subtle)
    for year, label in ERA_MARKERS:
        ax.axvline(x=year, color='#CCC', linestyle='--', linewidth=1, zorder=1)

    # Log scale on y-axis
    ax.set_yscale('log')

    # Y-axis formatting
    ax.set_yticks([100, 200, 500, 1000, 2000])
    ax.set_yticklabels(['100', '200', '500', '1,000', '2,000'])
    ax.set_ylim(50, 3000)

    # X-axis
    ax.set_xlim(-10000, 2100)
    ax.set_xticks([-9000, -5000, -3000, 0, 1000, 1750, 1900, 2000])
    ax.set_xticklabels(['-9000', '-5000', '-3000', '0', '1000', '1750', '1900', '2000'])

    # Grid
    ax.grid(True, which='major', axis='y', linestyle='-', alpha=0.3)
    ax.grid(True, which='major', axis='x', linestyle='-', alpha=0.2)

    # Labels
    ax.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('Watts per Person', fontsize=11, fontweight='bold')
    ax.set_title('Energy Leverage per Person\nFrom ~2× to ~17× metabolic baseline',
                 fontsize=14, fontweight='bold', pad=15)

    # Legend
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)

    # Add multiplier annotations at key points
    for _, row in df.iterrows():
        if row['year'] in [-9000, 1750, 2000]:
            mult = row['multiple_vs_metabolic']
            y_offset = 1.15 if row['year'] != 2000 else 1.12
            ax.annotate(f'{mult:.1f}×',
                       xy=(row['year'], row['watts_per_person']),
                       xytext=(row['year'], row['watts_per_person'] * y_offset),
                       fontsize=8, ha='center', va='bottom', color='#E67E22',
                       fontweight='bold')

    plt.tight_layout()
    return fig


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    export_dir = os.path.join(os.path.dirname(script_dir), 'export')
    os.makedirs(export_dir, exist_ok=True)

    df = load_data()
    fig = create_static_chart(df)

    # Save PNG
    png_path = os.path.join(export_dir, 'energy_leverage.png')
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved: {png_path}")

    # Save high-res PNG
    highres_path = os.path.join(export_dir, 'energy_leverage_highres.png')
    fig.savefig(highres_path, dpi=400, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved: {highres_path}")

    # Save SVG
    svg_path = os.path.join(export_dir, 'energy_leverage.svg')
    fig.savefig(svg_path, format='svg', bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved: {svg_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
