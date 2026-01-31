#!/usr/bin/env python3
"""
History of Compute & Intelligence: Training FLOPs for Key AI Milestones (1900-2026)
Interactive Plotly version with hover tooltips
"""

import numpy as np
import re

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not installed. Run: pip install plotly")

# Raw data (same as matplotlib version)
data_raw = """Year	Event	Category	Compute_FLOPs	Parameters	Impact
1904	Vacuum Tube (Fleming) - Enabled electronic switching for computing	Hardware	N/A	N/A	High
1936	Turing Machine (Alan Turing) - Defined computability limits	Theoretical Foundation	N/A	N/A	Transformative
1937	Shannon's Thesis - Boolean logic to electrical circuits (birth of the bit)	Theoretical Foundation	N/A	N/A	Transformative
1945	ENIAC - First programmable electronic general-purpose computer	Hardware	Proxy: ~5e2 ops/sec	N/A	High
1947	Transistor (Bell Labs) - Solid-state replacement for tubes	Hardware	N/A	N/A	Transformative
1950	Turing's "Computing Machinery and Intelligence" - Turing Test proposed	Theoretical Foundation	N/A	N/A	High
1956	Dartmouth Conference - "Artificial Intelligence" term coined; birth of AI field	AI Milestone	N/A	N/A	Transformative
1957	Perceptron (Rosenblatt) - Early neural network hardware	Model Release	Proxy: low	N/A	High
1958	Integrated Circuit (Kilby) - Multiple transistors on one chip	Hardware	N/A	N/A	Transformative
1959	Arthur Samuel coins "Machine Learning"; self-improving checkers program	AI Milestone	Proxy: low	N/A	Medium
1965	Moore's Law stated (Gordon Moore) - Transistor doubling prediction	Hardware	N/A	N/A	Transformative
1969	ARPANET - Precursor to Internet; Shakey the Robot (first mobile planner)	Infrastructure;Robotics	Proxy: low	N/A	High
1971	Intel 4004 - First commercial microprocessor	Hardware	N/A	N/A	High
1973	First AI Winter begins (~1973-1980) - Funding cuts after overhype	AI Winter	N/A	N/A	Medium
1986	Backpropagation revival (Rumelhart/Hinton) - Enabled multi-layer neural nets	Model/Architecture	N/A	N/A	High
1987	Second AI Winter (~1987-1993) - Expert systems collapse	AI Winter	N/A	N/A	Medium
1997	Deep Blue (IBM) - Brute-force chess victory over Kasparov	AI Milestone	Proxy: ~1e10 ops/sec	N/A	High
2000	Honda ASIMO - Advanced humanoid walking (rule-based)	Robotics	N/A	N/A	Medium
2002	Roomba (iRobot) - First mass-market autonomous home robot	Robotics	N/A	N/A	Medium
2006	Hinton et al. rebrand "Deep Learning"; deep belief networks	Model/Architecture	N/A	N/A	High
2006	AWS launch - Cloud computing infrastructure for scale	Infrastructure	N/A	N/A	Transformative
2007	NVIDIA CUDA - GPUs enabled for general-purpose parallel computing	Hardware	N/A	N/A	Transformative
2009	ImageNet dataset (Fei-Fei Li) - 14M+ labeled images fuel vision models	Dataset	N/A	N/A	Transformative
2010	DeepMind founded - Goal to solve intelligence	AI Milestone	N/A	N/A	High
2011	IBM Watson wins Jeopardy!; Siri launches (Apple)	AI Milestone	N/A	N/A	High
2012	AlexNet - CNN crushes ImageNet; deep learning breakthrough	Model Release	6.00E+17	60M	Transformative
2012	Google Cat Paper - Unsupervised learning from YouTube videos	Model Release	~1e16	N/A	High
2013	Word2Vec (Google) - Semantic word embeddings	Model/Architecture	N/A	N/A	High
2013	DeepMind DQN - Atari games from pixels (reinforcement learning)	Model Release	~1e15	N/A	High
2014	GANs invented (Ian Goodfellow) - Generative adversarial networks	Model/Architecture	N/A	N/A	Transformative
2015	OpenAI founded; TensorFlow open-sourced; ResNet (very deep nets)	AI Milestone;Model/Architecture	N/A	N/A	Transformative
2016	AlphaGo (DeepMind) - Defeats Lee Sedol in Go	Model Release	~1e18	N/A	Transformative
2017	Transformers paper ("Attention Is All You Need")	Model/Architecture	N/A	N/A	Transformative
2018	GPT-1 (OpenAI); BERT (Google) - Transformer NLP advances	Model Release	~1e17-1e18	110M-340M	High
2019	GPT-2 (OpenAI) - Emergent scaling behaviors	Model Release	~1e19	1.5B	High
2020	GPT-3 (OpenAI) - 175B params; few-shot learning	Model Release	3.14E+23	175B	Transformative
2020	AlphaFold (DeepMind) - Protein structure prediction breakthrough	Model Release	~1e20+	N/A	Transformative
2021	DALL-E (OpenAI) - Text-to-image generation; Codex (early coding)	Generative	High compute	N/A	High
2022	ChatGPT (based on GPT-3.5) - Mass adoption of conversational AI	Model Release	~few e23	N/A	Transformative
2022	Stable Diffusion - Open-source diffusion model revolution	Generative	~1e20+	1B+	Transformative
2023	GPT-4 (OpenAI) - Multimodal; major capability jump	Model Release	~2e25	N/A (est. trillions)	Transformative
2023	Gemini 1.0 (Google); Grok-1 (xAI); Llama 2 (Meta open weights)	Model Release	1e24-1e25 range	N/A-70B	High
2024	Sora (OpenAI video gen); Claude 3 family (Anthropic); o1 reasoning model	Generative;Reasoning/Agentic	2e25-5e25	N/A- hundreds B	Transformative
2024	Gemini 1.5/2.0; Llama 3.1 405B (Meta); EU AI Act	Model Release;Regulation	4e25 (Llama 3.1 est.)	405B	High
2025	Grok-3 (xAI) - Frontier reasoning model	Model Release	>1e26 (est.)	N/A	Transformative
2025	o3 / Claude 4 family advances; Gemini 2.5/3; agentic tools scale (Devin etc.)	Reasoning/Agentic	1e26-5e26 range	N/A	High
2025	Quantum error-correction milestones (e.g. Willow-like chips)	Quantum/Future Speculative	N/A	N/A	Medium
2026	Agentic AI & recursive self-improvement loops emerge at scale	Reasoning/Agentic	Speculative 1e27+	N/A	Speculative High
2026	Tesla Optimus production pivot; world models (Genie-like)	Robotics;Generative	Speculative	N/A	Speculative High
2026	Omni-modal single models; recursive learning + infinite context	Speculative	Speculative 1e28+	N/A	Speculative Transformative"""


def parse_flops(value):
    """Convert FLOPs string to numeric value."""
    if not value or value == 'N/A':
        return None
    value = str(value).strip()
    if 'Speculative' in value:
        match = re.search(r'(\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
        if match:
            return float(f"{match.group(1)}e{match.group(2)}")
        return 1e27
    if 'High compute' in value or value == 'Speculative':
        return 1e21
    if 'Proxy' in value:
        match = re.search(r'(\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
        if match:
            return float(f"{match.group(1)}e{match.group(2)}")
        if 'low' in value.lower():
            return 1e6
        return 1e3
    range_match = re.search(r'(\d+\.?\d*)e(\d+)[-–](\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
    if range_match:
        low = float(f"{range_match.group(1)}e{range_match.group(2)}")
        high = float(f"{range_match.group(3)}e{range_match.group(4)}")
        return np.sqrt(low * high)
    if value.startswith('>'):
        match = re.search(r'(\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
        if match:
            return float(f"{match.group(1)}e{match.group(2)}")
    if 'few' in value.lower():
        match = re.search(r'e(\d+)', value, re.IGNORECASE)
        if match:
            return 3 * 10**int(match.group(1))
    match = re.search(r'^~?(\d+\.?\d*)[eE](\d+)', value)
    if match:
        return float(f"{match.group(1)}e{match.group(2)}")
    match = re.search(r'(\d+\.?\d*)[eE]\+?(\d+)', value)
    if match:
        return float(f"{match.group(1)}e{match.group(2)}")
    match = re.search(r'~?(\d+\.?\d*)e(\d+)\+?', value, re.IGNORECASE)
    if match:
        return float(f"{match.group(1)}e{match.group(2)}")
    return None


def get_primary_category(cat_str):
    if not cat_str:
        return 'Other'
    return cat_str.split(';')[0].strip()


def parse_data(raw_data):
    lines = raw_data.strip().split('\n')
    records = []
    for line in lines[1:]:
        parts = line.split('\t')
        if len(parts) >= 5:
            year_str = parts[0].strip()
            year_match = re.match(r'(\d{4})', year_str)
            if year_match:
                year = int(year_match.group(1))
                if '(early)' in year_str:
                    year += 0.2
                elif '(future)' in year_str:
                    year += 0.5
            else:
                continue
            record = {
                'year': year,
                'event': parts[1].strip(),
                'category': parts[2].strip(),
                'flops_raw': parts[3].strip(),
                'parameters': parts[4].strip() if len(parts) > 4 else 'N/A',
                'impact': parts[5].strip() if len(parts) > 5 else 'Medium'
            }
            record['flops'] = parse_flops(record['flops_raw'])
            record['primary_category'] = get_primary_category(record['category'])
            records.append(record)
    return records


CATEGORY_COLORS = {
    'Hardware': '#E67E22',
    'Theoretical Foundation': '#7F8C8D',
    'AI Milestone': '#16A085',
    'Model Release': '#8E44AD',
    'Model/Architecture': '#9B59B6',
    'Dataset': '#27AE60',
    'Robotics': '#E74C3C',
    'AI Winter': '#BDC3C7',
    'Infrastructure': '#8B4513',
    'Generative': '#FF69B4',
    'Reasoning/Agentic': '#1D8348',
    'Quantum/Future Speculative': '#9B59B6',
    'Speculative': '#9B59B6',
    'Other': '#3498DB'
}

IMPACT_SIZES = {
    'Transformative': 22,
    'Speculative Transformative': 18,
    'High': 14,
    'Speculative High': 12,
    'Medium': 10,
    'Low': 8
}


def create_plotly_chart(records):
    # Assign proxy values for records without FLOPs
    for r in records:
        if r['flops'] is None:
            if r['year'] < 1945:
                r['flops'] = 1e2
            elif r['year'] < 1960:
                r['flops'] = 1e4
            elif r['year'] < 1980:
                r['flops'] = 1e6
            elif r['year'] < 2000:
                r['flops'] = 1e8
            elif r['year'] < 2010:
                r['flops'] = 1e10
            else:
                r['flops'] = 1e12

    records.sort(key=lambda x: x['year'])

    fig = go.Figure()

    # Add era shading as shapes
    eras = [
        (1900, 1940, 'rgba(200,200,200,0.2)', 'Mechanical & Theoretical'),
        (1940, 1960, 'rgba(100,150,220,0.2)', 'Electronic Dawn'),
        (1960, 2000, 'rgba(100,200,100,0.2)', "Moore's Law Scaling"),
        (2000, 2012, 'rgba(255,200,100,0.2)', 'Parallel & Early Deep'),
        (2012, 2022, 'rgba(180,150,220,0.2)', 'Deep Learning Big Bang'),
        (2022, 2027, 'rgba(255,150,150,0.2)', 'Reasoning & Agentic Era')
    ]

    for start, end, color, label in eras:
        fig.add_vrect(x0=start, x1=end, fillcolor=color, line_width=0,
                      annotation_text=label, annotation_position="top",
                      annotation_font_size=10, annotation_font_color="gray")

    # Add connecting line - split pre/post 2010 to show discontinuity
    pre_2010 = [(r['year'], r['flops']) for r in records if r['year'] < 2010]
    post_2010 = [(r['year'], r['flops']) for r in records if r['year'] >= 2010]

    if pre_2010:
        pre_years, pre_flops = zip(*pre_2010)
        fig.add_trace(go.Scatter(
            x=pre_years, y=pre_flops, mode='lines',
            line=dict(color='rgba(50,50,50,0.25)', width=1, dash='dash'),
            showlegend=False, hoverinfo='skip', name='Pre-2010 (proxy)'
        ))

    if post_2010:
        post_years, post_flops = zip(*post_2010)
        fig.add_trace(go.Scatter(
            x=post_years, y=post_flops, mode='lines',
            line=dict(color='rgba(50,50,50,0.4)', width=1.5),
            showlegend=False, hoverinfo='skip', name='Post-2010 (actual)'
        ))

    # Group records by category for legend
    categories = {}
    for r in records:
        cat = r['primary_category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    # Add scatter points by category
    for cat, cat_records in categories.items():
        color = CATEGORY_COLORS.get(cat, '#3498DB')

        x_vals = [r['year'] for r in cat_records]
        y_vals = [r['flops'] for r in cat_records]
        sizes = [IMPACT_SIZES.get(r['impact'], 10) for r in cat_records]
        symbols = ['diamond' if 'Speculative' in r['impact'] or r['year'] >= 2026
                   else ('triangle-down' if 'Winter' in r['category'] else 'circle')
                   for r in cat_records]

        hover_texts = [
            f"<b>{r['event'][:60]}...</b><br>" +
            f"Year: {int(r['year'])}<br>" +
            f"Category: {r['category']}<br>" +
            f"Compute: {r['flops_raw']}<br>" +
            f"Parameters: {r['parameters']}<br>" +
            f"Impact: {r['impact']}"
            for r in cat_records
        ]

        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='markers',
            marker=dict(
                size=sizes, color=color,
                symbol=symbols[0] if len(set(symbols)) == 1 else symbols,
                line=dict(width=1, color='white')
            ),
            name=cat,
            text=hover_texts,
            hoverinfo='text'
        ))

    # Add Moore's Law reference line
    moore_years = np.linspace(1965, 2005, 100)
    moore_start = 1e6
    moore_flops = moore_start * np.power(2, (moore_years - 1965) / 2)
    fig.add_trace(go.Scatter(
        x=moore_years, y=moore_flops, mode='lines',
        line=dict(color='#E67E22', width=2, dash='dash'),
        name="Moore's Law trajectory",
        hoverinfo='skip'
    ))

    # Add key event annotations
    key_events = [
        (1936, 'Turing Machine'), (1945, 'ENIAC'), (1947, 'Transistor'),
        (1956, 'AI Born'), (1965, "Moore's Law"), (1997, 'Deep Blue'),
        (2007, 'CUDA'), (2009, 'ImageNet'), (2012, 'AlexNet'),
        (2016, 'AlphaGo'), (2017, 'Transformers'), (2020, 'GPT-3'),
        (2022, 'ChatGPT'), (2023, 'GPT-4'), (2025, 'Grok-3')
    ]

    for r in records:
        for yr, lbl in key_events:
            if abs(r['year'] - yr) < 0.5 and lbl in r['event']:
                fig.add_annotation(
                    x=r['year'], y=r['flops'],
                    text=lbl, showarrow=True,
                    arrowhead=0, arrowsize=0.5, arrowwidth=1,
                    arrowcolor='gray',
                    ax=30, ay=-40,
                    font=dict(size=9, color='#333'),
                    bgcolor='rgba(255,255,255,0.8)',
                    borderpad=2
                )
                break

    # Layout configuration
    fig.update_layout(
        title=dict(
            text='<b>History of Compute & Intelligence</b><br>' +
                 '<sup>Training FLOPs for Key AI Milestones (1900–2026)</sup>',
            x=0.5, font=dict(size=20)
        ),
        xaxis=dict(
            title='Year', range=[1898, 2028],
            tickmode='linear', tick0=1900, dtick=10,
            gridcolor='rgba(128,128,128,0.2)',
            minor=dict(tickmode='linear', tick0=1900, dtick=5)
        ),
        yaxis=dict(
            title='Total Training Compute (FLOPs, log₁₀)',
            type='log', range=[1, 29],
            gridcolor='rgba(128,128,128,0.3)',
            tickformat='.0e'
        ),
        legend=dict(
            title='Category',
            yanchor='top', y=0.99, xanchor='left', x=1.02,
            bgcolor='rgba(255,255,255,0.9)'
        ),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='white',
        width=1400, height=800,
        margin=dict(r=200, t=100, b=80),
        hovermode='closest'
    )

    # Add frontier cluster bracket annotation
    fig.add_annotation(
        x=2022.5, y=3e25,
        text="<b>2023–25 Frontier Cluster</b><br>(10²⁴–10²⁶ FLOPs)",
        showarrow=False,
        font=dict(size=10, color='#444'),
        bgcolor='rgba(255,255,255,0.85)',
        borderpad=4,
        xanchor='right'
    )

    # Add note
    fig.add_annotation(
        text="Log scale: exponential growth appears as straight lines.<br>" +
             "Pre-2010 values are rough proxies (ops/sec, not directly comparable).<br>" +
             "Speculative 2026+ points marked with diamonds.<br>" +
             "Sources: Epoch AI, Our World in Data. Estimates as of Jan 2026.",
        xref='paper', yref='paper', x=0.01, y=0.01,
        showarrow=False, font=dict(size=9, color='#666'),
        bgcolor='rgba(255,255,255,0.9)', borderpad=5,
        align='left'
    )

    return fig


def main():
    if not PLOTLY_AVAILABLE:
        print("Please install plotly: pip install plotly")
        return

    records = parse_data(data_raw)
    print(f"Parsed {len(records)} records")

    fig = create_plotly_chart(records)

    # Save as interactive HTML
    fig.write_html('/Users/mschwar/ai_compute_timeline_interactive.html')
    print("Saved: ai_compute_timeline_interactive.html")

    # Save as static image (requires kaleido)
    try:
        fig.write_image('/Users/mschwar/ai_compute_timeline_plotly.png', scale=2)
        print("Saved: ai_compute_timeline_plotly.png")
    except Exception as e:
        print(f"Note: Static image export requires kaleido: pip install kaleido")

    print("\nDone!")


if __name__ == '__main__':
    main()
