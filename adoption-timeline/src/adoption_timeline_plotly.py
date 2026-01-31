#!/usr/bin/env python3
"""
Accelerating Paradigms in Computing & Connectivity: Time to Mass Adoption (1970-2030)
Interactive Plotly version with hover tooltips
"""

import numpy as np
import os

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not installed. Run: pip install plotly")

# Raw data
data_raw = """Year,Event,Category,Days_to_Adoption,Impact
1957,FORTRAN Compiler (IBM),Software/Compiler,3650,High
1969,ARPANET launch,Internet/Web,3650,High
1971,Intel 4004 Microprocessor,Hardware,1825,Medium
1975,Microsoft BASIC / Altair 8800,Software/Compiler,1825,Medium
1981,IBM PC release,Hardware,1460,High
1984,Apple Macintosh (GUI),Hardware,1825,High
1989,World Wide Web proposed (Berners-Lee),Internet/Web,1460,Transformative
1995,Windows 95 + Netscape boom,Internet/Web,730,High
1998,Google Search public,Internet/Web,1095,High
2004,Facebook launch,Social/Apps,365,Transformative
2006,AWS public cloud launch,Cloud/Infrastructure,1095,Transformative
2007,iPhone (1st gen) + App Store (2008),Mobile,730,Transformative
2008,Android Market / App ecosystem,Mobile,365,High
2010,Instagram launch,Social/Apps,270,High
2012,Hadoop / Big Data maturity in cloud,Cloud/Infrastructure,730,Medium
2016,TikTok global launch,Social/Apps,180,High
2022,ChatGPT public launch,AI/Agentic,60,Transformative
2023,Grok (xAI) public on X,AI/Agentic,180,High
2024,o1 / Claude 3.5 / Gemini 1.5 reasoning models,AI/Agentic,90,High
2025,Agentic AI tools scale (Devin-like),AI/Agentic,30,Transformative
2026,Projected omni-modal / recursive agents,AI/Agentic,14,Speculative Transformative"""


def parse_data(raw_data):
    """Parse the raw CSV data into structured format."""
    lines = raw_data.strip().split('\n')
    records = []
    for line in lines[1:]:
        parts = line.split(',')
        if len(parts) >= 5:
            record = {
                'year': int(parts[0]),
                'event': parts[1].strip(),
                'category': parts[2].strip(),
                'days': int(parts[3]),
                'impact': parts[4].strip()
            }
            records.append(record)
    return records


CATEGORY_COLORS = {
    'Hardware': '#3498DB',
    'Software/Compiler': '#E67E22',
    'Internet/Web': '#27AE60',
    'Mobile': '#9B59B6',
    'Social/Apps': '#FF69B4',
    'Cloud/Infrastructure': '#8B4513',
    'AI/Agentic': '#E74C3C',
    'Other': '#7F8C8D'
}

IMPACT_SIZES = {
    'Transformative': 22,
    'Speculative Transformative': 20,
    'High': 14,
    'Medium': 10,
    'Low': 8
}


def days_to_readable(days):
    """Convert days to readable format."""
    if days >= 365:
        years = days / 365
        return f"{days} days (~{years:.1f} years)"
    elif days >= 30:
        months = days / 30
        return f"{days} days (~{months:.1f} months)"
    elif days >= 7:
        weeks = days / 7
        return f"{days} days (~{weeks:.1f} weeks)"
    else:
        return f"{days} days"


def create_plotly_chart(records):
    """Create the interactive Plotly chart."""
    records.sort(key=lambda x: x['year'])

    fig = go.Figure()

    # Add era shading
    eras = [
        (1955, 1990, 'rgba(200,200,200,0.3)', 'PC & Software Foundations'),
        (1990, 2005, 'rgba(100,150,220,0.25)', 'Internet & Web Boom'),
        (2005, 2015, 'rgba(180,150,220,0.25)', 'Mobile & Social Explosion'),
        (2015, 2025, 'rgba(100,200,150,0.25)', 'Cloud & Data Dominance'),
        (2025, 2035, 'rgba(255,150,150,0.3)', 'AI & Agentic Hyper-Scale')
    ]

    for start, end, color, label in eras:
        fig.add_vrect(x0=start, x1=end, fillcolor=color, line_width=0,
                      annotation_text=label, annotation_position="top",
                      annotation_font_size=10, annotation_font_color="gray")

    # Add connecting line
    years = [r['year'] for r in records]
    days = [r['days'] for r in records]
    fig.add_trace(go.Scatter(
        x=years, y=days, mode='lines',
        line=dict(color='rgba(26,82,118,0.4)', width=1.5),
        showlegend=False, hoverinfo='skip'
    ))

    # Add exponential trend line
    trend_years = np.linspace(1957, 2030, 100)
    k = np.log(3650 / 14) / (2026 - 1957)
    trend_days = 3650 * np.exp(-k * (trend_years - 1957))
    fig.add_trace(go.Scatter(
        x=trend_years, y=trend_days, mode='lines',
        line=dict(color='#E67E22', width=2, dash='dash'),
        name='Exponential compression trend',
        hoverinfo='skip'
    ))

    # Group by category for legend
    categories = {}
    for r in records:
        cat = r['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    # Add scatter points by category
    for cat, cat_records in categories.items():
        color = CATEGORY_COLORS.get(cat, '#7F8C8D')

        x_vals = [r['year'] for r in cat_records]
        y_vals = [r['days'] for r in cat_records]
        sizes = [IMPACT_SIZES.get(r['impact'], 10) for r in cat_records]
        symbols = ['diamond' if 'Speculative' in r['impact'] or r['year'] >= 2026 else 'circle'
                   for r in cat_records]

        hover_texts = [
            f"<b>{r['event']}</b><br>" +
            f"Year: {r['year']}<br>" +
            f"Time to 50M: {days_to_readable(r['days'])}<br>" +
            f"Category: {r['category']}<br>" +
            f"Impact: {r['impact']}"
            for r in cat_records
        ]

        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='markers',
            marker=dict(
                size=sizes, color=color,
                symbol=symbols[0] if len(set(symbols)) == 1 else symbols,
                line=dict(width=1.5, color='white')
            ),
            name=cat,
            text=hover_texts,
            hoverinfo='text'
        ))

    # Add key annotations
    key_events = [
        (1957, 'FORTRAN'), (1989, 'WWW'), (2004, 'Facebook'),
        (2007, 'iPhone'), (2022, 'ChatGPT'), (2025, 'Agentic AI')
    ]

    for r in records:
        for yr, lbl in key_events:
            if r['year'] == yr and lbl in r['event']:
                fig.add_annotation(
                    x=r['year'], y=r['days'],
                    text=lbl, showarrow=True,
                    arrowhead=0, arrowsize=0.5, arrowwidth=1,
                    arrowcolor='gray',
                    ax=25, ay=-35,
                    font=dict(size=10, color='#333'),
                    bgcolor='rgba(255,255,255,0.85)',
                    borderpad=3
                )
                break

    # Layout configuration
    fig.update_layout(
        title=dict(
            text='<b>Accelerating Paradigms in Computing & Connectivity</b><br>' +
                 '<sup>Time to Mass Adoption: Days to ~50M Users (1957–2026)</sup>',
            x=0.5, font=dict(size=20)
        ),
        xaxis=dict(
            title='Year', range=[1953, 2032],
            tickmode='linear', tick0=1955, dtick=5,
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            title='Days to ~50M Users or Equivalent Adoption (log₁₀ scale)',
            type='log', range=[1, 4.2],
            gridcolor='rgba(128,128,128,0.3)',
            tickvals=[10, 30, 100, 365, 1000, 3650, 10000],
            ticktext=['10 (~2wk)', '30 (1mo)', '100 (~3mo)', '365 (1yr)', '1000 (~3yr)', '3650 (10yr)', '10000 (~27yr)']
        ),
        legend=dict(
            title='Category',
            yanchor='top', y=0.99, xanchor='left', x=1.02,
            bgcolor='rgba(255,255,255,0.9)'
        ),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='white',
        width=1400, height=800,
        margin=dict(r=200, t=100, b=100),
        hovermode='closest'
    )

    # Add notes
    fig.add_annotation(
        text="Log scale: shortening adoption times appear as downward trend.<br>" +
             "Pre-1990 estimates approximate; post-2010 driven by network effects.<br>" +
             "ChatGPT: fastest ever to 50M users (~60 days). 2025+ speculative.<br>" +
             "Sources: Statista, Asymco, Epoch AI, historical adoption curves.",
        xref='paper', yref='paper', x=0.01, y=0.01,
        showarrow=False, font=dict(size=9, color='#666'),
        bgcolor='rgba(255,255,255,0.9)', borderpad=5,
        align='left'
    )

    fig.add_annotation(
        text="<i>Complements AI Compute FLOPs timeline – shows ecosystem acceleration enabling AI scale</i>",
        xref='paper', yref='paper', x=0.99, y=0.99,
        showarrow=False, font=dict(size=9, color='#888'),
        xanchor='right', yanchor='top'
    )

    return fig


def main():
    if not PLOTLY_AVAILABLE:
        print("Please install plotly: pip install plotly")
        return

    # Determine output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    records = parse_data(data_raw)
    print(f"Parsed {len(records)} records")

    fig = create_plotly_chart(records)

    # Save as interactive HTML
    output_path = os.path.join(output_dir, 'adoption_timeline_interactive.html')
    fig.write_html(output_path)
    print(f"Saved: {output_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
