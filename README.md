# DECOY

🎯 **A high-fidelity CS2 simulation environment for strategic multi-agent planning research.** DECOY transforms complex 3D tactical gameplay into efficient discretized simulations while preserving environmental realism. Using neural models trained on real tournament data, it enables researchers to study strategic decision-making without the computational overhead of low-level game mechanics. Perfect for advancing multi-agent AI research in competitive scenarios.

![DECOY Framework](imgs/framework_diagram.jpg)

## Quick Start

### Option A: Use Existing CS:GO Data (Test Code)

```bash
# Setup environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Explore the simulation (uses CS:GO data if available)
python inspector_demo.py
```

### Option B: Start CS2 Migration (Recommended)

See [docs/CS2_DATA_PIPELINE.md](docs/CS2_DATA_PIPELINE.md) for detailed instructions.

**Quick version:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download CS2 demo files from HLTV.org

# 3. Convert demos to training format
python convert_cs2_demos.py path/to/demos --output data/cs2_parsed

# 4. Extract CS2 map geometry (see download_cs2_map.py)

# 5. Process data and train models (see trainer/)
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