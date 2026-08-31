# DECOY

🎯 **A high-fidelity CS2 simulation environment for strategic multi-agent planning research.** DECOY transforms complex 3D tactical gameplay into efficient discretized simulations while preserving environmental realism. Using neural models trained on real tournament data, it enables researchers to study strategic decision-making without the computational overhead of low-level game mechanics. Perfect for advancing multi-agent AI research in competitive scenarios.

![DECOY Framework](imgs/framework_diagram.jpg)

## Quick Start

```bash
# Setup environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Explore the simulation
python inspector_demo.py
```

## Features

- **Discretized Strategic Planning**: High-level tactical decisions without low-level mechanics
- **Real Data Integration**: Neural models trained on professional CS2 tournament data  
- **Efficient Simulation**: Computationally lightweight while maintaining environmental fidelity
- **Research Ready**: Built for multi-agent planning and behavior generation research

## CS2 Migration Status

⚠️ **Migration in progress from CS:GO to CS2.** See [CS2_MIGRATION.md](CS2_MIGRATION.md) for details.

**Completed:**
- ✅ Code refactored for CS2
- ✅ Added CS2 demo parser dependencies (awpy, demoparser2)

**In Progress:**
- 🚧 Data pipeline conversion (CS2 demos → training format)
- 🚧 Map geometry extraction (CS2 Source 2 format)

**Pending:**
- ⏳ Model retraining on CS2 tournament data

## Roadmap

- [ ] Complete CS2 data pipeline migration
- [ ] CS2 map geometry extraction automation
- [ ] Retrain all models on CS2 data
- [ ] MARL training examples
- [ ] Environment customization tools
- [ ] Interactive waypoint visualizer


# Citation

```bib
@inproceedings{wang2025cs2,
  author    = {Yunzhe Wang and Volkan Ustun and Chris McGroarty},
  title     = {A data-driven discretized {CS2} simulation environment to facilitate strategic multi-agent planning research},
  booktitle = {Proceedings of the 2025 Winter Simulation Conference (WSC)},
  year      = {2025},
  address   = {Los Angeles, CA, USA},
  publisher = {IEEE},
}
```