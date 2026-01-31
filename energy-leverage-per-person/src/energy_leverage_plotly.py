#!/usr/bin/env python3
"""
Energy Leverage per Person – Interactive Plotly Chart
Kurzweil-simple: shows how humans went from ~1-2× to ~17× body energy leverage
"""

import pandas as pd
import plotly.graph_objects as go
import os

# Constants
METABOLIC_BASELINE_GJ = 3.6  # GJ/person/year
METABOLIC_BASELINE_W = 114.08  # Watts (continuous equivalent)

# Era markers for vertical reference lines
ERA_MARKERS = [
    (-10000, "Agriculture"),
    (-3200, "Writing/States"),
    (1750, "Coal/Steam"),
    (1950, "Acceleration"),
]


def load_data():
    """Load CSV data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(os.path.dirname(script_dir), 'data', 'energy_leverage_datapoints.csv')
    return pd.read_csv(data_path)


def create_interactive_chart(df):
    """Create Plotly interactive chart."""
    fig = go.Figure()

    # Hover template for total energy line
    hover_total = (
        "<b>%{customdata[0]}</b><br>"
        "Year: %{x}<br>"
        "Total: %{y:.0f} W (%{customdata[1]:.1f} GJ/yr)<br>"
        "External: %{customdata[2]:.0f} W<br>"
        "Multiplier: <b>%{customdata[3]:.1f}×</b> metabolic<br>"
        "<extra></extra>"
    )

    hover_external = (
        "<b>%{customdata[0]}</b><br>"
        "Year: %{x}<br>"
        "External only: %{y:.0f} W<br>"
        "(Total minus metabolic)<br>"
        "<extra></extra>"
    )

    # Custom data for hover
    customdata_total = list(zip(
        df['label'],
        df['energy_total_GJ_per_person_year'],
        df['watts_external'],
        df['multiple_vs_metabolic']
    ))

    customdata_external = list(zip(
        df['label'],
        df['energy_external_GJ_per_person_year'],
        df['watts_external'],
        df['multiple_vs_metabolic']
    ))

    # Line 1: Total energy (watts per person)
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['watts_per_person'],
        mode='lines+markers',
        name='Total Energy',
        line=dict(color='#E67E22', width=3),
        marker=dict(size=10, color='#E67E22', line=dict(width=2, color='white')),
        customdata=customdata_total,
        hovertemplate=hover_total
    ))

    # Line 2: External energy (watts per person)
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['watts_external'],
        mode='lines+markers',
        name='External Energy',
        line=dict(color='#3498DB', width=3),
        marker=dict(size=10, color='#3498DB', line=dict(width=2, color='white')),
        customdata=customdata_external,
        hovertemplate=hover_external
    ))

    # Metabolic baseline reference line
    fig.add_hline(
        y=METABOLIC_BASELINE_W,
        line_dash="dot",
        line_color="#888",
        line_width=1.5,
        annotation_text=f"Metabolic baseline (~{METABOLIC_BASELINE_W:.0f} W)",
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="#666"
    )

    # Era markers (vertical lines)
    for year, label in ERA_MARKERS:
        fig.add_vline(
            x=year,
            line_dash="dash",
            line_color="rgba(100,100,100,0.3)",
            line_width=1
        )
        fig.add_annotation(
            x=year,
            y=1,
            yref="paper",
            text=label,
            showarrow=False,
            font=dict(size=9, color="#666"),
            textangle=-45,
            yshift=10
        )

    # Layout
    fig.update_layout(
        title=dict(
            text="<b>Energy Leverage per Person</b><br>"
                 "<sup>From ~2× to ~17× metabolic baseline (foragers → modern)</sup>",
            x=0.5,
            font=dict(size=18)
        ),
        xaxis=dict(
            title="Year",
            tickformat="d",
            gridcolor='rgba(128,128,128,0.2)',
            zeroline=True,
            zerolinecolor='rgba(128,128,128,0.3)',
            zerolinewidth=1
        ),
        yaxis=dict(
            title="Watts per Person (continuous power equivalent)",
            type="log",
            gridcolor='rgba(128,128,128,0.2)',
            tickvals=[100, 200, 500, 1000, 2000],
            ticktext=['100', '200', '500', '1,000', '2,000']
        ),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='white',
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        ),
        height=550,
        width=900,
        margin=dict(b=120),
        autosize=True
    )

    # Caption annotation
    caption = (
        "Humans went from ~1–2× body energy (foragers) to ~17× (modern average). "
        "The post-1750 coal/steam and post-1950 oil/electricity jumps dominate the visual story. "
        "Sources: Nature synthesis (per-capita intervals); Smil (metabolic baseline)."
    )
    fig.add_annotation(
        text=caption,
        xref='paper', yref='paper',
        x=0.5, y=-0.18,
        showarrow=False,
        font=dict(size=10, color='#555'),
        align='center'
    )

    return fig


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    df = load_data()
    fig = create_interactive_chart(df)

    # Save interactive HTML
    html_path = os.path.join(output_dir, 'energy_leverage_interactive.html')
    fig.write_html(html_path)
    print(f"Saved: {html_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
