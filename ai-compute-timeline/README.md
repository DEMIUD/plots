# History of Compute & Intelligence

A publication-quality semi-log timeline visualization showing training FLOPs for key AI milestones from 1900 to 2026.

![AI Compute Timeline](output/ai_compute_timeline_highres.png)

## Interactive Version

Open [`output/ai_compute_timeline_interactive.html`](output/ai_compute_timeline_interactive.html) in your browser for an interactive version with hover tooltips showing full event details.

## Features

- **Semi-logarithmic scale**: Y-axis spans 10^0 to 10^27 FLOPs, showing exponential growth as straight lines
- **Color-coded categories**: Hardware, Model Release, AI Milestone, Theoretical Foundation, etc.
- **Impact-sized markers**: Transformative > High > Medium (larger = more impactful)
- **Era shading**: Visual periods from Mechanical & Theoretical (1900-1940) through Reasoning & Agentic (2022+)
- **Moore's Law reference**: Dashed orange line showing transistor doubling trajectory
- **Pre/Post 2010 distinction**: Dashed line for proxy values vs. solid line for actual training compute

## Data

The dataset (`data/ai_milestones.csv`) includes 50 milestones with:
- Year
- Event description
- Category (Hardware, AI Milestone, Model Release, etc.)
- Compute estimate (FLOPs or proxy)
- Parameters (where applicable)
- Impact level (Transformative, High, Medium)

### Data Sources

- [Epoch AI](https://epochai.org/) - Training compute estimates
- [Our World in Data](https://ourworldindata.org/) - Historical trends
- Various scaling reports and model announcements

Pre-2010 values are rough proxies (ops/sec equivalents) and not directly comparable to training FLOPs. Post-2023 estimates based on published research and scaling trends. Speculative 2026+ points marked with diamond markers.

## Usage

### Requirements

```bash
pip install matplotlib numpy plotly
```

### Generate Static Charts (matplotlib)

```bash
python src/ai_compute_timeline.py
```

Outputs:
- `ai_compute_timeline.png` (300 DPI)
- `ai_compute_timeline_highres.png` (400 DPI)
- `ai_compute_timeline.svg` (vector)

### Generate Interactive HTML (Plotly)

```bash
python src/ai_compute_timeline_plotly.py
```

Outputs:
- `ai_compute_timeline_interactive.html`

## File Structure

```
ai-compute-timeline/
├── README.md
├── data/
│   └── ai_milestones.csv      # Source data
├── src/
│   ├── ai_compute_timeline.py        # Matplotlib version
│   └── ai_compute_timeline_plotly.py # Plotly interactive version
└── output/
    ├── ai_compute_timeline_highres.png
    ├── ai_compute_timeline.svg
    └── ai_compute_timeline_interactive.html
```

## License

MIT
