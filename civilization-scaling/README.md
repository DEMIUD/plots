# Scaling Civilization: Energy, Coordination, Memory, Replication

A multi-lane log-time timeline showing how four fundamental metrics have scaled over human history (1M years ago → 2030+).

![Civilization Scaling](output/civilization_scaling_highres.png)

## Interactive Version

Open [`output/civilization_scaling_interactive.html`](output/civilization_scaling_interactive.html) for hover details on each milestone and phase flip.

## The Four Lanes

| Lane | Metric | Trend | Key Phase Flips |
|------|--------|-------|-----------------|
| **Energy** | kcal/person/day | ↑ Upward | Fire → Agriculture → Steam → Electricity |
| **Coordination** | Max stable group | ↑ Upward | Language → Writing → Print → Internet |
| **Memory** | bits/person accessible | ↑ Upward | Symbols → Writing → Print → AI |
| **Replication** | hours/copy (cost) | ↓ Downward | Scribes → Print → Digital → AI Gen |

## Key Insight: Log-Time Compression

The log x-axis reveals a striking truth:
- **~99% of human existence** was pre-writing (left side, compressed)
- **Agriculture** is only ~12K years old
- **Internet** is a blink (~30 years)
- **AI** is instantaneous on this scale

## Phase Flips (Stacking Events)

Vertical dashed lines mark where multiple lanes "flip" together:

| Years Ago | Event | Stacking Effect |
|-----------|-------|-----------------|
| 800K | Fire/Cooking | Energy extraction → brain growth |
| 250K | Language | Coordination via shared myths |
| 12K | Agriculture | Surplus → classes/cities/writing |
| 5K | Writing | Institutional trust at scale |
| 574 | Printing | Ideas replicate free → science |
| 264 | Steam | Fossil fuels → industrial revolution |
| 44 | Internet | Global instant coordination |
| 4 | AI | Mind automation begins |

## Theoretical Foundations

This visualization bridges:

- **Biology**: Herculano-Houzel (neurons/kcal), Kaplan/Charnov (LHT/OFT forager returns)
- **Technology**: Kurzweil (price-performance), network effects
- **Anthropology**: Dunbar number, institutional economics

S-curves in each lane show how new "infrastructure layers" enable the next leap.

## Perspective Notes

> "Most human existence was pre-writing (>99%)"

> "Agriculture: only ~12K years"

> "Internet: a blink (~30 years)"

> "Progress is uneven – compression accelerates"

## Data Sources

- Our World in Data (energy, population)
- Ethnographic studies (Ache, Tsimane forager data)
- Historical technology timelines
- Wikipedia/WBWI for memory/latency history

## Usage

```bash
pip install matplotlib numpy plotly

# Static charts
cd src && python civilization_scaling.py

# Interactive HTML
cd src && python civilization_scaling_plotly.py
```

## Related Visualizations

- [AI Compute Timeline](../ai-compute-timeline/) – Training FLOPs growth
- [Adoption Timeline](../adoption-timeline/) – Time to 50M users compression
- [Energetic Scaling](../energetic-scaling/) – Biology vs. tech efficiency

## License

MIT
