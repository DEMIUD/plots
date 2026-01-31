# Contributing

Ideas and issues welcome!

## Suggesting New Milestones

Have a technology milestone that should be included? [Open an issue](https://github.com/mschwar/plots/issues/new) with:

- **Year** of launch/release
- **Event** name and brief description
- **Category** (Hardware, Software, AI/Agentic, etc.)
- **Metric** (Training FLOPs or Days to 50M users)
- **Source** for the data

## Reporting Issues

Found an error in the data or visualization? Please open an issue describing:

- Which plot (AI Compute or Adoption Timeline)
- What's incorrect
- Suggested correction with source

## Future Plot Ideas

Interested in seeing additional visualizations? Some ideas under consideration:

- Energy & Inference Costs in AI
- Global AI Model Releases by Year
- Hardware Price/Performance Over Time
- AI Benchmark Progress (MMLU, etc.)

Feel free to suggest others via issues.

## Technical Contributions

Pull requests welcome for:

- Bug fixes in Python scripts
- Improved label positioning
- Additional data points with sources
- Accessibility improvements

### Setup

```bash
pip install matplotlib numpy plotly
```

### Regenerating Plots

```bash
# AI Compute Timeline
cd ai-compute-timeline/src && python ai_compute_timeline.py && python ai_compute_timeline_plotly.py

# Adoption Timeline
cd adoption-timeline/src && python adoption_timeline.py && python adoption_timeline_plotly.py
```

## License

By contributing, you agree that your contributions will be licensed under MIT.
