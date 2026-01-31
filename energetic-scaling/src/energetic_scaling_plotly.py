#!/usr/bin/env python3
"""
Energetic Scaling: Brain/Neural Efficiency vs. Size in Biology
and Compute Efficiency vs. Scale in Technology

Interactive Plotly version with hover tooltips.
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


def load_biological_data():
    """Load biological data from CSV."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'data', 'biological_data.csv')
    df = pd.read_csv(csv_path)
    data = []
    for _, row in df.iterrows():
        data.append({
            "entity": row['entity'],
            "mass": float(row['mass_kg']),
            "neurons": float(row['neurons']),
            "per_kg": float(row['neurons_per_kg']),
            "group": row['group'],
            "impact": row['impact'],
            "notes": row['notes']
        })
    return data


def load_hardware_data():
    """Load hardware data from CSV."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'data', 'hardware_data.csv')
    df = pd.read_csv(csv_path)
    data = []
    for _, row in df.iterrows():
        data.append({
            "entity": row['entity'],
            "year": int(row['year']),
            "cps": float(row['cps']),
            "category": row['category'],
            "impact": row['impact'],
            "notes": row['notes']
        })
    return data


def load_ai_data():
    """Load AI model data from CSV."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'data', 'ai_model_data.csv')
    df = pd.read_csv(csv_path)
    data = []
    for _, row in df.iterrows():
        data.append({
            "entity": row['entity'],
            "year": int(row['year']),
            "flops": float(row['flops']),
            "impact": row['impact'],
            "notes": row['notes'] if 'notes' in row else ""
        })
    return data

BIO_COLORS = {
    "Reptiles": "#7F8C8D",
    "Birds": "#27AE60",
    "Mammals": "#3498DB",
    "Primates": "#9B59B6",
}

TECH_COLORS = {
    "Hardware": "#E67E22",
    "AI": "#E74C3C",
}

IMPACT_SIZES = {
    "Transformative": 22,
    "High": 14,
    "Medium": 10,
    "Low": 7,
}


def create_plotly_chart(bio_data, tech_data, ai_data):
    """Create interactive dual-panel Plotly chart."""

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            '<b>Biological Allometry</b><br><sup>Neural Efficiency vs. Body Size</sup>',
            '<b>Tech Scaling (Kurzweil-inspired)</b><br><sup>Compute Efficiency vs. Time</sup>'
        ),
        horizontal_spacing=0.12
    )

    # ========================================================================
    # LEFT PANEL: Biology
    # ========================================================================
    for group in ["Reptiles", "Birds", "Mammals", "Primates"]:
        group_data = [d for d in bio_data if d["group"] == group]
        if not group_data:
            continue

        x = [d["mass"] for d in group_data]
        y = [d["per_kg"] for d in group_data]
        sizes = [IMPACT_SIZES.get(d["impact"], 10) for d in group_data]
        color = BIO_COLORS[group]

        hover_texts = [
            f"<b>{d['entity']}</b><br>" +
            f"Body Mass: {d['mass']:.4g} kg<br>" +
            f"Total Neurons: {d['neurons']:.2e}<br>" +
            f"Neurons/kg: {d['per_kg']:.2e}<br>" +
            f"Group: {d['group']}<br>" +
            f"Impact: {d['impact']}<br>" +
            f"<i>{d['notes']}</i>"
            for d in group_data
        ]

        # Special marker for Human
        symbols = ['star' if d['entity'] == 'Human' else 'circle' for d in group_data]
        marker_sizes = [s * 1.5 if d['entity'] == 'Human' else s for s, d in zip(sizes, group_data)]

        fig.add_trace(go.Scatter(
            x=x, y=y, mode='markers',
            marker=dict(size=marker_sizes, color=color, symbol=symbols,
                       line=dict(width=1, color='white')),
            name=group, text=hover_texts, hoverinfo='text',
            legendgroup='bio', legendgrouptitle_text='Biology'
        ), row=1, col=1)

    # Add trend line for mammals
    mammal_data = [d for d in bio_data if d["group"] == "Mammals"]
    if len(mammal_data) >= 2:
        log_x = np.log10([d["mass"] for d in mammal_data])
        log_y = np.log10([d["per_kg"] for d in mammal_data])
        from scipy import stats
        slope, intercept, _, _, _ = stats.linregress(log_x, log_y)
        x_fit = np.logspace(-2, 4, 50)
        y_fit = 10**(intercept + slope * np.log10(x_fit))
        fig.add_trace(go.Scatter(
            x=x_fit, y=y_fit, mode='lines',
            line=dict(color=BIO_COLORS["Mammals"], dash='dash', width=2),
            name=f'Mammals trend (slope={slope:.2f})',
            hoverinfo='skip', legendgroup='bio'
        ), row=1, col=1)

    # ========================================================================
    # RIGHT PANEL: Tech
    # ========================================================================
    # Hardware data
    x_hw = [d["year"] for d in tech_data]
    y_hw = [d["cps"] for d in tech_data]
    sizes_hw = [IMPACT_SIZES.get(d["impact"], 10) for d in tech_data]

    hover_hw = [
        f"<b>{d['entity']}</b><br>" +
        f"Year: {d['year']}<br>" +
        f"Compute/$ (cps): {d['cps']:.2e}<br>" +
        f"Impact: {d['impact']}<br>" +
        f"<i>{d['notes']}</i>"
        for d in tech_data
    ]

    fig.add_trace(go.Scatter(
        x=x_hw, y=y_hw, mode='markers',
        marker=dict(size=sizes_hw, color=TECH_COLORS["Hardware"],
                   line=dict(width=1, color='white')),
        name='Hardware (cps/$)', text=hover_hw, hoverinfo='text',
        legendgroup='tech', legendgrouptitle_text='Technology'
    ), row=1, col=2)

    # Kurzweil trend line
    from scipy import stats
    years = np.array([d["year"] for d in tech_data])
    log_cps = np.log10([d["cps"] for d in tech_data])
    slope, intercept, _, _, _ = stats.linregress(years, log_cps)
    x_fit = np.linspace(1935, 2030, 50)
    y_fit = 10**(intercept + slope * x_fit)

    fig.add_trace(go.Scatter(
        x=x_fit, y=y_fit, mode='lines',
        line=dict(color=TECH_COLORS["Hardware"], dash='dash', width=2),
        name=f'Kurzweil trend (~{10**slope:.1f}x/yr)',
        hoverinfo='skip', legendgroup='tech'
    ), row=1, col=2)

    # AI FLOPs (secondary y-axis style - we'll use annotations)
    x_ai = [d["year"] for d in ai_data]
    y_ai = [d["flops"] for d in ai_data]
    sizes_ai = [IMPACT_SIZES.get(d["impact"], 10) for d in ai_data]

    hover_ai = [
        f"<b>{d['entity']}</b><br>" +
        f"Year: {d['year']}<br>" +
        f"Training FLOPs: {d['flops']:.2e}<br>" +
        f"Impact: {d['impact']}<br>" +
        f"<i>{d['notes']}</i>"
        for d in ai_data
    ]

    # Add AI data on secondary y-axis (we'll fake it by scaling)
    # Map FLOPs to cps/$ scale for visual placement
    y_ai_scaled = [f * 1e-12 for f in y_ai]  # Scale down to fit on same visual

    fig.add_trace(go.Scatter(
        x=x_ai, y=y_ai_scaled, mode='markers',
        marker=dict(size=sizes_ai, color=TECH_COLORS["AI"], symbol='diamond',
                   line=dict(width=1, color='white')),
        name='AI Models (FLOPs)', text=hover_ai, hoverinfo='text',
        legendgroup='tech', yaxis='y4'
    ), row=1, col=2)

    # ========================================================================
    # LAYOUT
    # ========================================================================
    fig.update_xaxes(type='log', title_text='Body Mass (kg)', row=1, col=1,
                    gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(type='log', title_text='Neurons per kg Body Mass', row=1, col=1,
                    gridcolor='rgba(128,128,128,0.2)')

    fig.update_xaxes(title_text='Year', row=1, col=2, range=[1935, 2030],
                    gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(type='log', title_text='Compute per Dollar (cps/$)', row=1, col=2,
                    gridcolor='rgba(128,128,128,0.2)')

    # Add shaded regions
    fig.add_vrect(x0=2012, x1=2030, fillcolor='rgba(231,76,60,0.1)',
                 line_width=0, row=1, col=2)

    fig.update_layout(
        title=dict(
            text='<b>Energetic Scaling</b><br>' +
                 '<sup>Neural Efficiency (Biology) vs. Compute Efficiency (Technology)</sup>',
            x=0.5, font=dict(size=20)
        ),
        legend=dict(
            orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5,
            bgcolor='rgba(255,255,255,0.9)'
        ),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='white',
        width=1500, height=700,
        margin=dict(t=120, b=150),
        hovermode='closest',
        autosize=True
    )

    # Footnote
    fig.add_annotation(
        text="Log-log plots reveal power laws. Biology: Neurons/kg shows clade differences; humans outlier (EQ~7). " +
             "Tech: cps/$ mirrors Kurzweil's ~75 quadrillion-fold increase (1939–2024).<br>" +
             "Sources: Herculano-Houzel (neuronal), Kleiber (metabolic 0.75), Kaplan/Charnov (LHT), Kurzweil. Jan 2026.",
        xref='paper', yref='paper', x=0.5, y=-0.18,
        showarrow=False, font=dict(size=10, color='#666'),
        align='center'
    )

    return fig


def main():
    if not PLOTLY_AVAILABLE:
        print("Please install plotly: pip install plotly")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Load data from CSV
    bio_data = load_biological_data()
    tech_data = load_hardware_data()
    ai_data = load_ai_data()
    print(f"Loaded {len(bio_data)} biological, {len(tech_data)} hardware, {len(ai_data)} AI records")

    fig = create_plotly_chart(bio_data, tech_data, ai_data)
    print("Created interactive energetic scaling chart")

    output_path = os.path.join(output_dir, 'energetic_scaling_interactive.html')
    fig.write_html(output_path)
    print(f"Saved: {output_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
