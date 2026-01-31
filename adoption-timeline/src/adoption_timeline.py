#!/usr/bin/env python3
"""
Accelerating Paradigms in Computing & Connectivity: Time to Mass Adoption (1970-2030)
Publication-quality semi-log timeline visualization
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import os

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
    for line in lines[1:]:  # Skip header
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


# Category color mapping
CATEGORY_COLORS = {
    'Hardware': '#3498DB',           # Blue
    'Software/Compiler': '#E67E22',  # Orange
    'Internet/Web': '#27AE60',       # Green
    'Mobile': '#9B59B6',             # Purple
    'Social/Apps': '#FF69B4',        # Pink
    'Cloud/Infrastructure': '#8B4513',  # Brown
    'AI/Agentic': '#E74C3C',         # Red
    'Other': '#7F8C8D'               # Gray
}

# Impact to marker size mapping
IMPACT_SIZES = {
    'Transformative': 200,
    'Speculative Transformative': 180,
    'High': 120,
    'Medium': 70,
    'Low': 40
}


def get_short_label(event):
    """Extract short label for annotation."""
    labels = {
        'FORTRAN': 'FORTRAN',
        'ARPANET': 'ARPANET',
        'Intel 4004': '4004',
        'Microsoft BASIC': 'MS BASIC',
        'IBM PC': 'IBM PC',
        'Macintosh': 'Mac',
        'World Wide Web': 'WWW',
        'Windows 95': 'Win95',
        'Google Search': 'Google',
        'Facebook': 'Facebook',
        'AWS': 'AWS',
        'iPhone': 'iPhone',
        'Android': 'Android',
        'Instagram': 'Instagram',
        'Hadoop': 'Hadoop',
        'TikTok': 'TikTok',
        'ChatGPT': 'ChatGPT',
        'Grok': 'Grok',
        'o1': 'o1/Claude/Gemini',
        'Agentic AI': 'Agentic AI',
        'omni-modal': 'Omni-modal',
    }
    for key, label in labels.items():
        if key in event:
            return label
    return None


def create_timeline_plot(records):
    """Create the main timeline visualization."""

    # Set up the figure
    fig, ax = plt.subplots(figsize=(16, 10), dpi=150)

    # Set background
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('white')

    # Add era shading
    eras = [
        (1955, 1990, '#E8E8E8', 'PC & Software\nFoundations'),
        (1990, 2005, '#E0F0FF', 'Internet &\nWeb Boom'),
        (2005, 2015, '#F0E0FF', 'Mobile &\nSocial Explosion'),
        (2015, 2025, '#E0FFE8', 'Cloud & Data\nDominance'),
        (2025, 2035, '#FFE0E0', 'AI & Agentic\nHyper-Scale')
    ]

    for start, end, color, label in eras:
        ax.axvspan(start, end, alpha=0.6, color=color, zorder=0)

    # Sort records by year
    records.sort(key=lambda x: x['year'])

    # Extract data
    years = [r['year'] for r in records]
    days = [r['days'] for r in records]
    colors = [CATEGORY_COLORS.get(r['category'], '#7F8C8D') for r in records]
    sizes = [IMPACT_SIZES.get(r['impact'], 70) for r in records]

    # Plot connecting line
    ax.plot(years, days, '-', color='#1A5276', alpha=0.4, linewidth=1.5, zorder=1)

    # Plot scatter points
    for i, r in enumerate(records):
        marker = 'o'
        edgecolor = 'white'
        alpha = 1.0

        # Special markers for speculative/future
        if 'Speculative' in r['impact'] or r['year'] >= 2026:
            marker = 'd'  # Diamond for speculative
            edgecolor = '#333333'
            alpha = 0.7

        ax.scatter(r['year'], r['days'],
                   c=colors[i], s=sizes[i],
                   marker=marker, alpha=alpha,
                   edgecolors=edgecolor, linewidths=1.5,
                   zorder=3)

    # Add exponential compression trend line
    # Roughly halving every 15 years from ~3650 days in 1970 to ~14 days in 2026
    trend_years = np.linspace(1957, 2030, 100)
    # Exponential decay: days = A * exp(-k * (year - 1957))
    # From 3650 in 1957 to ~14 in 2026 (69 years)
    k = np.log(3650 / 14) / (2026 - 1957)
    trend_days = 3650 * np.exp(-k * (trend_years - 1957))
    ax.plot(trend_years, trend_days, '--', color='#E67E22', alpha=0.6, linewidth=2,
            label='Exponential compression trend', zorder=2)

    # Add annotations with custom positioning
    label_positions = {
        'FORTRAN': (2, 1.5, 20),
        'ARPANET': (2, 0.6, -20),
        'Intel 4004': (-5, 1.5, -20),
        'MS BASIC': (2, 1.4, 20),
        'IBM PC': (2, 1.5, 25),
        'Mac': (-5, 0.7, -20),
        'WWW': (2, 1.6, 25),
        'Win95': (2, 1.5, 25),
        'Google': (-4, 0.7, -20),
        'Facebook': (1.5, 1.6, 30),
        'AWS': (-4, 0.6, -25),
        'iPhone': (1.5, 1.7, 30),
        'Android': (-3, 0.6, -25),
        'Instagram': (1.5, 1.6, 30),
        'Hadoop': (-4, 0.6, -20),
        'TikTok': (1.5, 1.8, 35),
        'ChatGPT': (1, 1.8, 40),
        'Grok': (-2.5, 0.5, -35),
        'o1/Claude/Gemini': (0.8, 2, 45),
        'Agentic AI': (-2, 0.5, -40),
        'Omni-modal': (0.5, 2, 50),
    }

    for r in records:
        label = get_short_label(r['event'])
        if label:
            pos = label_positions.get(label, (1.5, 1.5, 25))
            x_offset, y_mult, rotation = pos

            fontsize = 8
            if 'Transformative' in r['impact']:
                fontsize = 9

            ha = 'left' if x_offset >= 0 else 'right'

            ax.annotate(label,
                        xy=(r['year'], r['days']),
                        xytext=(r['year'] + x_offset, r['days'] * y_mult),
                        fontsize=fontsize,
                        ha=ha,
                        rotation=rotation,
                        alpha=0.85,
                        arrowprops=dict(arrowstyle='-', color='gray', alpha=0.4, lw=0.5),
                        zorder=4)

    # Configure axes
    ax.set_yscale('log')
    ax.set_xlim(1953, 2032)
    ax.set_ylim(8, 15000)

    # X-axis configuration
    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    major_ticks = range(1955, 2035, 5)
    ax.set_xticks(major_ticks)
    ax.tick_params(axis='x', labelsize=11)

    # Y-axis configuration
    ax.set_ylabel('Days to ~50M Users or Equivalent Adoption (log₁₀ scale)', fontsize=13, fontweight='bold')
    y_ticks = [10, 30, 100, 365, 1000, 3650, 10000]
    y_labels = ['10\n(~1.5 wk)', '30\n(1 mo)', '100\n(~3 mo)', '365\n(1 yr)', '1000\n(~3 yr)', '3650\n(10 yr)', '10000\n(~27 yr)']
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=9)

    # Grid
    ax.grid(True, which='major', axis='y', linestyle='-', alpha=0.3, color='gray')
    ax.grid(True, which='minor', axis='y', linestyle=':', alpha=0.2, color='gray')
    ax.grid(True, which='major', axis='x', linestyle='-', alpha=0.2, color='gray')

    # Title
    ax.set_title('Accelerating Paradigms in Computing & Connectivity:\nTime to Mass Adoption (1957–2026)',
                 fontsize=18, fontweight='bold', pad=20)

    # Add era labels at top
    for start, end, color, label in eras:
        mid = (start + end) / 2
        ax.text(mid, 12000, label, ha='center', va='bottom', fontsize=8,
                rotation=0, alpha=0.7, style='italic')

    # Create legend - Category
    category_handles = []
    for cat, color in CATEGORY_COLORS.items():
        if any(r['category'] == cat for r in records):
            category_handles.append(mpatches.Patch(color=color, label=cat))

    # Impact size legend
    size_handles = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray',
               markersize=np.sqrt(IMPACT_SIZES['Transformative']/4), label='Transformative'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray',
               markersize=np.sqrt(IMPACT_SIZES['High']/4), label='High'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray',
               markersize=np.sqrt(IMPACT_SIZES['Medium']/4), label='Medium'),
        Line2D([0], [0], marker='d', color='w', markerfacecolor='gray',
               markersize=8, label='Speculative', markeredgecolor='black')
    ]

    # Trend line handle
    trend_handle = Line2D([0], [0], linestyle='--', color='#E67E22',
                          linewidth=2, label='Exponential compression')

    # Position legends
    leg1 = ax.legend(handles=category_handles, loc='upper left',
                     fontsize=8, title='Category', title_fontsize=9,
                     framealpha=0.9, bbox_to_anchor=(1.01, 1))
    ax.add_artist(leg1)

    leg2 = ax.legend(handles=size_handles + [trend_handle], loc='lower left',
                     fontsize=8, title='Impact / Type', title_fontsize=9,
                     framealpha=0.9, bbox_to_anchor=(1.01, 0))

    # Add note box
    note_text = ("Log scale turns accelerating (shortening) adoption into a downward trend.\n"
                 "Pre-1990 estimates approximate; post-2010 driven by network effects & mobile/cloud.\n"
                 "ChatGPT: fastest to 50M users ever (~60 days). 2025+ projections speculative.\n"
                 "Sources: Statista, Asymco, historical tech adoption curves, Epoch AI.")

    props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='gray')
    ax.text(0.02, 0.02, note_text, transform=ax.transAxes, fontsize=7,
            verticalalignment='bottom', bbox=props, family='sans-serif')

    # Add complementary note
    ax.text(0.98, 0.98, 'Complements AI Compute FLOPs timeline –\nshows ecosystem acceleration enabling AI scale',
            transform=ax.transAxes, fontsize=7, ha='right', va='top',
            style='italic', alpha=0.6)

    plt.tight_layout()
    plt.subplots_adjust(right=0.82)

    return fig, ax


def main():
    # Determine output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Parse data
    records = parse_data(data_raw)
    print(f"Parsed {len(records)} records")

    # Create plot
    fig, ax = create_timeline_plot(records)

    # Save outputs
    fig.savefig(os.path.join(output_dir, 'adoption_timeline.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("Saved: adoption_timeline.png (300 DPI)")

    fig.savefig(os.path.join(output_dir, 'adoption_timeline.svg'), format='svg', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("Saved: adoption_timeline.svg")

    fig.savefig(os.path.join(output_dir, 'adoption_timeline_highres.png'), dpi=400, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("Saved: adoption_timeline_highres.png (400 DPI)")

    print("\nDone!")


if __name__ == '__main__':
    main()
