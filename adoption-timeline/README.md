# Accelerating Paradigms in Computing & Connectivity

A publication-quality semi-log timeline visualization showing the dramatically shortening time to mass adoption (50M users) for major technology paradigms from 1957 to 2026.

![Adoption Timeline](output/adoption_timeline_highres.png)

## Interactive Version

Open [`output/adoption_timeline_interactive.html`](output/adoption_timeline_interactive.html) in your browser for an interactive version with hover tooltips showing full event details.

## Key Insight

**Adoption time has compressed exponentially**: from ~10 years (FORTRAN, ARPANET) to ~60 days (ChatGPT) - a 60x acceleration over 65 years.

| Era | Example | Time to 50M |
|-----|---------|-------------|
| 1957 | FORTRAN | ~10 years |
| 1989 | WWW | ~4 years |
| 2004 | Facebook | ~1 year |
| 2007 | iPhone | ~2 years |
| 2022 | **ChatGPT** | **~60 days** |
| 2025+ | Agentic AI | ~30 days (projected) |

## Features

- **Semi-logarithmic scale**: Y-axis spans 10 to 10,000 days, turning exponential compression into a visible downward trend
- **Color-coded categories**: Hardware, Internet/Web, Mobile, Social/Apps, Cloud, AI/Agentic
- **Impact-sized markers**: Transformative > High > Medium
- **Era shading**: Visual periods from PC Foundations through AI Hyper-Scale
- **Exponential trend line**: Shows the theoretical compression curve

## Relationship to AI Compute Timeline

This visualization complements the [AI Compute Timeline](../ai-compute-timeline/):
- **Compute timeline**: Shows exponential *growth* in training FLOPs (upward)
- **Adoption timeline**: Shows exponential *compression* in time-to-adoption (downward)

Together they illustrate how infrastructure acceleration enables AI scale.

## Data

The dataset (`data/tech_adoption.csv`) includes 21 milestones with:
- Year of launch/release
- Event description
- Category
- Days to ~50M users/devices/equivalent
- Impact level

### Data Sources

- [Statista](https://www.statista.com/) - Adoption statistics
- [Asymco](http://www.asymco.com/) - Technology adoption curves
- Historical tech adoption research
- [Epoch AI](https://epochai.org/) - AI context

Pre-1990 values are estimates (years converted to days). Post-2010 values reflect network effects and mobile/cloud acceleration. 2025+ projections are speculative based on recent trends.

## Usage

### Requirements

```bash
pip install matplotlib numpy plotly
```

### Generate Static Charts (matplotlib)

```bash
cd src && python adoption_timeline.py
```

Outputs:
- `adoption_timeline.png` (300 DPI)
- `adoption_timeline_highres.png` (400 DPI)
- `adoption_timeline.svg` (vector)

### Generate Interactive HTML (Plotly)

```bash
cd src && python adoption_timeline_plotly.py
```

Outputs:
- `adoption_timeline_interactive.html`

## File Structure

```
adoption-timeline/
├── README.md
├── data/
│   └── tech_adoption.csv
├── src/
│   ├── adoption_timeline.py
│   └── adoption_timeline_plotly.py
└── output/
    ├── adoption_timeline_highres.png
    ├── adoption_timeline.svg
    └── adoption_timeline_interactive.html
```

## License

MIT
