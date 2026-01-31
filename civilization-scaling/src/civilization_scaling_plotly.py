#!/usr/bin/env python3
"""
Scaling Civilization: Multi-lane log-time timeline
Interactive Plotly version with hover tooltips
"""

import numpy as np
import pandas as pd
import os

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not installed. Run: pip install plotly")


def load_data():
    """Load civilization metrics from CSV."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'data', 'civilization_metrics.csv')
    return pd.read_csv(csv_path)


def get_lane_data(df, lane_name):
    """Extract data for a specific lane as list of dicts."""
    lane_df = df[df['Lane'] == lane_name].copy()
    data = []
    for _, row in lane_df.iterrows():
        data.append({
            "event": row['Event'],
            "years_ago": row['Years_Ago'],
            "value": row['Metric_Value'],
            "era": row['Era'],
            "impact": row['Impact'],
            "notes": row['Notes'],
            "phase": row['Phase_Flip'] if pd.notna(row['Phase_Flip']) else None
        })
    return data

LANE_COLORS = {
    "Energy": "#E67E22",
    "Coordination": "#27AE60",
    "Memory": "#3498DB",
    "Replication": "#9B59B6",
}

IMPACT_SIZES = {
    "Transformative": 18,
    "High": 12,
    "Medium": 8,
    "Low": 6,
    "Speculative": 10,
}


def years_ago_to_x(years_ago):
    return -np.log10(years_ago + 1)


def create_plotly_chart(df):
    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.08,
        subplot_titles=('<b>Energy</b> (kcal/person/day)',
                       '<b>Coordination</b> (max stable group)',
                       '<b>Memory</b> (bits/person accessible)',
                       '<b>Replication</b> (hours/copy – cost ↓)')
    )

    # Load data for each lane from CSV
    energy_data = get_lane_data(df, "Energy")
    coordination_data = get_lane_data(df, "Coordination")
    memory_data = get_lane_data(df, "Memory")
    replication_data = get_lane_data(df, "Replication")

    lanes = [
        ("Energy", energy_data, 1),
        ("Coordination", coordination_data, 2),
        ("Memory", memory_data, 3),
        ("Replication", replication_data, 4),
    ]

    for lane_name, data, row in lanes:
        color = LANE_COLORS[lane_name]
        x_vals = [years_ago_to_x(d["years_ago"]) for d in data]
        y_vals = [d["value"] for d in data]
        sizes = [IMPACT_SIZES.get(d["impact"], 10) for d in data]

        hover_texts = [
            f"<b>{d['event']}</b><br>" +
            f"Years Ago: {d['years_ago']:,}<br>" +
            f"Value: {d['value']:.2e}<br>" +
            f"Era: {d['era']}<br>" +
            f"Impact: {d['impact']}<br>" +
            f"<i>{d['notes']}</i>" +
            (f"<br><b>Phase: {d.get('phase', '')}</b>" if d.get('phase') else "")
            for d in data
        ]

        symbols = ['diamond' if d['impact'] == 'Speculative' else 'circle' for d in data]

        # Line
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='lines',
            line=dict(color=color, width=1.5),
            showlegend=False, hoverinfo='skip'
        ), row=row, col=1)

        # Markers
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='markers',
            marker=dict(size=sizes, color=color, symbol=symbols,
                       line=dict(width=1, color='white')),
            name=lane_name if row == 1 else None,
            text=hover_texts, hoverinfo='text',
            showlegend=(row == 1)
        ), row=row, col=1)

    # Phase flip vertical lines
    phase_flips = [800000, 250000, 12000, 5000, 574, 264, 44, 4]
    for years in phase_flips:
        x = years_ago_to_x(years)
        for row in [1, 2, 3, 4]:
            fig.add_vline(x=x, line_dash="dash", line_color="gray",
                         opacity=0.5, row=row, col=1)

    # X-axis
    tick_years = [1000000, 100000, 10000, 1000, 100, 10, 1]
    tick_positions = [years_ago_to_x(y) for y in tick_years]
    tick_labels = ['1M', '100K', '10K', '1K', '100', '10', 'Now']

    fig.update_xaxes(
        tickvals=tick_positions, ticktext=tick_labels,
        title_text='Years Ago (Log Scale) – Prehistory Compressed, Modern Expanded',
        row=4, col=1
    )

    for row in [1, 2, 3, 4]:
        fig.update_yaxes(type='log', row=row, col=1, gridcolor='rgba(128,128,128,0.2)')
        fig.update_xaxes(range=[years_ago_to_x(1500000), years_ago_to_x(0.05)], row=row, col=1)

    fig.update_layout(
        title=dict(
            text='<b>Scaling Civilization</b><br>' +
                 '<sup>Energy, Coordination, Memory, Replication (1M Years Ago → 2030+)</sup>',
            x=0.5, font=dict(size=18)
        ),
        height=900, width=1400,
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='white',
        hovermode='closest',
        autosize=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
    )

    # Footnote
    fig.add_annotation(
        text="Log-time compresses prehistory (~99% of human existence pre-writing), expands modern acceleration. " +
             "Phase flips (dashed lines) show stacking events. Inspired by Herculano-Houzel, Kaplan/Charnov LHT, Kurzweil.",
        xref='paper', yref='paper', x=0.5, y=-0.08,
        showarrow=False, font=dict(size=9, color='#666'), align='center'
    )

    return fig


def main():
    if not PLOTLY_AVAILABLE:
        print("Install plotly: pip install plotly")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    df = load_data()
    fig = create_plotly_chart(df)
    output_path = os.path.join(output_dir, 'civilization_scaling_interactive.html')
    fig.write_html(output_path)
    print(f"Saved: {output_path}")
    print("\nDone!")


if __name__ == '__main__':
    main()
