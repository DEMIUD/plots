#!/usr/bin/env python3
"""
Scaling Civilization: Multi-lane log-time timeline
Interactive Plotly version with hover tooltips
"""

import numpy as np
import os

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not installed. Run: pip install plotly")

# Data
energy_data = [
    {"event": "Early Hominid", "years_ago": 1000000, "value": 500, "era": "Prehistory", "impact": "Medium", "notes": "Baseline foraging"},
    {"event": "Fire/Cooking", "years_ago": 800000, "value": 2000, "era": "Prehistory", "impact": "Transformative", "notes": "Cooking → Brains (+40% extraction)", "phase": "Cooking → Larger Brains"},
    {"event": "Hunting Cooperation", "years_ago": 300000, "value": 2500, "era": "Prehistory", "impact": "High", "notes": "Group hunts; variance reduction"},
    {"event": "Paleolithic Tools", "years_ago": 50000, "value": 3000, "era": "Prehistory", "impact": "Medium", "notes": "Better tools"},
    {"event": "Agriculture", "years_ago": 12000, "value": 5000, "era": "Neolithic", "impact": "Transformative", "notes": "Surplus → specialization", "phase": "Surplus → Classes/Cities"},
    {"event": "Draft Animals", "years_ago": 8000, "value": 8000, "era": "Neolithic", "impact": "High", "notes": "Oxen/horses multiply labor"},
    {"event": "Irrigation", "years_ago": 5000, "value": 12000, "era": "Ancient", "impact": "High", "notes": "Water control"},
    {"event": "Iron Tools", "years_ago": 3000, "value": 15000, "era": "Ancient", "impact": "Medium", "notes": "Better implements"},
    {"event": "Watermills", "years_ago": 1000, "value": 25000, "era": "Pre-Modern", "impact": "High", "notes": "Non-human power"},
    {"event": "Steam Engine", "years_ago": 264, "value": 50000, "era": "Industrial", "impact": "Transformative", "notes": "Fossil fuels", "phase": "Coal → Industrial Revolution"},
    {"event": "Electricity", "years_ago": 144, "value": 100000, "era": "Industrial", "impact": "Transformative", "notes": "Grid power"},
    {"event": "Oil/ICE", "years_ago": 120, "value": 200000, "era": "Modern", "impact": "High", "notes": "Mobility"},
    {"event": "Nuclear", "years_ago": 74, "value": 500000, "era": "Modern", "impact": "High", "notes": "Dense energy"},
    {"event": "Renewables", "years_ago": 24, "value": 300000, "era": "Digital", "impact": "High", "notes": "Solar/wind"},
    {"event": "AI Compute", "years_ago": 4, "value": 1000000, "era": "Digital", "impact": "High", "notes": "Datacenter surge"},
    {"event": "Fusion (proj)", "years_ago": 0.1, "value": 10000000, "era": "Future", "impact": "Speculative", "notes": "Abundant clean energy"},
]

coordination_data = [
    {"event": "Bands", "years_ago": 1000000, "value": 30, "era": "Prehistory", "impact": "Medium", "notes": "Primate-like groups"},
    {"event": "Language", "years_ago": 250000, "value": 50, "era": "Prehistory", "impact": "Transformative", "notes": "OFT/LHT; Ache-style", "phase": "Language → Shared Myths"},
    {"event": "Ritual/Art", "years_ago": 50000, "value": 150, "era": "Prehistory", "impact": "High", "notes": "Dunbar ~150"},
    {"event": "Villages", "years_ago": 12000, "value": 500, "era": "Neolithic", "impact": "High", "notes": "Sedentism"},
    {"event": "Chiefdoms", "years_ago": 7000, "value": 2000, "era": "Neolithic", "impact": "High", "notes": "Hierarchy"},
    {"event": "City-States", "years_ago": 5000, "value": 10000, "era": "Ancient", "impact": "Transformative", "notes": "Writing/laws", "phase": "Writing → Institutions"},
    {"event": "Empires", "years_ago": 2200, "value": 1000000, "era": "Ancient", "impact": "Transformative", "notes": "Rome/Han"},
    {"event": "Nations", "years_ago": 500, "value": 10000000, "era": "Pre-Modern", "impact": "High", "notes": "Print/nationalism"},
    {"event": "Global Trade", "years_ago": 200, "value": 100000000, "era": "Industrial", "impact": "High", "notes": "Telegraph"},
    {"event": "Multinationals", "years_ago": 74, "value": 500000000, "era": "Modern", "impact": "High", "notes": "Corps"},
    {"event": "Internet", "years_ago": 44, "value": 1000000000, "era": "Digital", "impact": "Transformative", "notes": "Global networks", "phase": "Internet → Instant Global"},
    {"event": "Social Platforms", "years_ago": 14, "value": 3000000000, "era": "Digital", "impact": "High", "notes": "Billions"},
    {"event": "AI Coordination", "years_ago": 4, "value": 5000000000, "era": "Digital", "impact": "High", "notes": "Automated trust", "phase": "AI → Automated Trust"},
    {"event": "Global Mesh (proj)", "years_ago": 0.1, "value": 8000000000, "era": "Future", "impact": "Speculative", "notes": "Universal"},
]

memory_data = [
    {"event": "Oral Only", "years_ago": 1000000, "value": 100, "era": "Prehistory", "impact": "Low", "notes": "Lossy"},
    {"event": "Language", "years_ago": 200000, "value": 1000, "era": "Prehistory", "impact": "Medium", "notes": "Mnemonics"},
    {"event": "Cave Art", "years_ago": 40000, "value": 5000, "era": "Prehistory", "impact": "High", "notes": "External storage", "phase": "Symbols → External Mind"},
    {"event": "Proto-Writing", "years_ago": 8000, "value": 10000, "era": "Neolithic", "impact": "High", "notes": "Tokens"},
    {"event": "Writing", "years_ago": 5000, "value": 50000, "era": "Ancient", "impact": "Transformative", "notes": "Cuneiform", "phase": "Writing → Cumulative Knowledge"},
    {"event": "Libraries", "years_ago": 2500, "value": 500000, "era": "Ancient", "impact": "High", "notes": "Alexandria"},
    {"event": "Printing", "years_ago": 574, "value": 10000000, "era": "Pre-Modern", "impact": "Transformative", "notes": "Gutenberg", "phase": "Print → Scientific Revolution"},
    {"event": "Telegraph", "years_ago": 180, "value": 100000000, "era": "Industrial", "impact": "High", "notes": "Instant"},
    {"event": "Radio/Film", "years_ago": 100, "value": 1000000000, "era": "Industrial", "impact": "High", "notes": "Broadcast"},
    {"event": "TV", "years_ago": 74, "value": 10000000000, "era": "Modern", "impact": "High", "notes": "Mass visual"},
    {"event": "PCs", "years_ago": 44, "value": 100000000000, "era": "Modern", "impact": "Transformative", "notes": "Personal", "phase": "PC → Digital Self"},
    {"event": "Internet", "years_ago": 24, "value": 1000000000000, "era": "Digital", "impact": "Transformative", "notes": "Global access"},
    {"event": "AI Synthesis", "years_ago": 4, "value": 1e15, "era": "Digital", "impact": "Transformative", "notes": "All knowledge", "phase": "AI → Mind Automation"},
    {"event": "Neural (proj)", "years_ago": 0.1, "value": 1e18, "era": "Future", "impact": "Speculative", "notes": "Brain-computer"},
]

replication_data = [
    {"event": "Handcraft", "years_ago": 1000000, "value": 1000, "era": "Prehistory", "impact": "Low", "notes": "Individual"},
    {"event": "Apprentice", "years_ago": 200000, "value": 100, "era": "Prehistory", "impact": "Medium", "notes": "Teaching"},
    {"event": "Molds", "years_ago": 8000, "value": 10, "era": "Neolithic", "impact": "High", "notes": "Templates"},
    {"event": "Scribes", "years_ago": 5000, "value": 50, "era": "Ancient", "impact": "Medium", "notes": "Expensive"},
    {"event": "Printing", "years_ago": 574, "value": 0.1, "era": "Pre-Modern", "impact": "Transformative", "notes": "Mechanical", "phase": "Print → Free Ideas"},
    {"event": "Factory", "years_ago": 200, "value": 0.01, "era": "Industrial", "impact": "Transformative", "notes": "Mass production"},
    {"event": "Mass Media", "years_ago": 100, "value": 0.001, "era": "Industrial", "impact": "High", "notes": "Records/film"},
    {"event": "Photocopy", "years_ago": 60, "value": 0.0001, "era": "Modern", "impact": "Medium", "notes": "Instant doc"},
    {"event": "Digital", "years_ago": 44, "value": 0.00001, "era": "Digital", "impact": "Transformative", "notes": "Zero cost", "phase": "Digital → Free Copy"},
    {"event": "Internet Dist", "years_ago": 24, "value": 0.000001, "era": "Digital", "impact": "High", "notes": "Global"},
    {"event": "AI Gen", "years_ago": 4, "value": 1e-7, "era": "Digital", "impact": "Transformative", "notes": "Instant create", "phase": "AI → Zero Cost Creation"},
    {"event": "Molecular (proj)", "years_ago": 0.1, "value": 1e-10, "era": "Future", "impact": "Speculative", "notes": "Physical copy"},
]

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


def create_plotly_chart():
    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.08,
        subplot_titles=('<b>Energy</b> (kcal/person/day)',
                       '<b>Coordination</b> (max stable group)',
                       '<b>Memory</b> (bits/person accessible)',
                       '<b>Replication</b> (hours/copy – cost ↓)')
    )

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

    fig = create_plotly_chart()
    output_path = os.path.join(output_dir, 'civilization_scaling_interactive.html')
    fig.write_html(output_path)
    print(f"Saved: {output_path}")
    print("\nDone!")


if __name__ == '__main__':
    main()
