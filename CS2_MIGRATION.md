# CS2 Migration Guide

This document tracks the migration from CS:GO to Counter-Strike 2 (CS2).

## Migration Status

### ✅ Completed
- [x] Code renamed from CS:GO to CS2
  - `CSGOEngine` → `CS2Engine`
  - `csgo_environment.py` → `cs2_environment.py`
  - `transform_csgo_to_panda3d()` → `transform_cs2_to_panda3d()`
  - Documentation updated
  - Citation updated

### 🚧 In Progress
- [ ] Data pipeline migration
- [ ] Map geometry extraction
- [ ] Model retraining

### ⏳ Pending
- [ ] Validate CS2 data format compatibility
- [ ] Performance benchmarking

---

## Data Migration

### Current State (CS:GO)
- Demo format: CS:GO `.dem` files parsed to JSON
- Map format: CS:GO BSP → FBX (via Google Drive)
- Training data: Professional CS:GO tournament replays

### Target State (CS2)
- Demo format: CS2 `.dem` files (Source 2 engine)
- Map format: CS2 VBSP/VPK → FBX/glTF
- Training data: Professional CS2 tournament replays

### Tools Added

#### 1. Demo Parser
**Dependencies:**
```bash
pip install awpy>=1.3.0 demoparser2
```

**awpy** - Full-featured CS2 parser
- GitHub: https://github.com/pnxenopoulos/awpy
- Outputs: Polars DataFrames
- Best for: Comprehensive analysis, multiple data views

**demoparser2** - Fast Rust-based parser
- GitHub: https://github.com/LaihoE/demoparser
- Outputs: JSON via Python bindings
- Best for: Speed, query-based extraction

#### 2. Conversion Script
`convert_cs2_demos.py` - Convert CS2 demos to DECOY training format

```bash
# Download CS2 demos from HLTV or other sources
python convert_cs2_demos.py /path/to/demos --output data/cs2_processed
```

**Status:** Skeleton implemented, needs schema mapping

#### 3. Map Extraction
`download_cs2_map.py` - Extract CS2 map geometry

**Manual Method (Current):**
1. Install ValveResourceFormat: https://github.com/ValveResourceFormat/ValveResourceFormat/releases
2. Extract from CS2 installation:
   ```bash
   Decompiler.exe --input "Steam/steamapps/common/Counter-Strike Global Offensive/game/csgo/maps/de_dust2.vpk"
   ```
3. Export as FBX and place in `env/assets/`

**Status:** Manual process documented, automation TODO

---

## Data Schema Differences

### CS:GO Demo → DECOY Format
- Input: JSON from parsed CS:GO demos
- Structure: `gameRounds` array with frame-by-frame data
- Fields: player positions, HP, weapons, bomb status, etc.

### CS2 Demo → DECOY Format (TODO)
**Key Questions:**
- Does CS2 demo structure match CS:GO closely enough?
- Are coordinate systems identical?
- Have weapon IDs or game mechanics changed?

**Action Items:**
1. Parse sample CS2 demo with awpy
2. Compare schema to CS:GO JSON structure
3. Document differences
4. Implement conversion in `convert_cs2_demos.py`

---

## Map Geometry Differences

### Coordinate Systems
- CS:GO: Source 1 engine coordinates
- CS2: Source 2 engine coordinates

**Validation needed:**
- Are coordinate transforms identical?
- Does `transform_cs2_to_panda3d()` work for CS2 data?

### Map Changes (de_dust2 example)
CS2 has updated many classic maps. Known changes:
- Visual improvements
- Potential layout tweaks
- New props/cover

**TODO:** Document specific changes affecting gameplay simulation

---

## Model Retraining Plan

Once CS2 data pipeline is ready:

1. **Damage Model** (`trainer/damage_model.py`)
   - Retrain on CS2 combat data
   - Validate weapon damage values haven't changed

2. **Movement Model** (`trainer/model.py`)
   - Retrain on CS2 player trajectories
   - Check if movement mechanics changed

3. **VAE Models** (`trainer/regression_vae_model.py`)
   - Retrain trajectory generation models
   - May need architecture adjustments

---

## Testing Strategy

### Phase 1: Syntax Validation ✅
- All Python files compile without errors
- Imports resolve correctly

### Phase 2: Data Pipeline (Current)
- [ ] Parse single CS2 demo successfully
- [ ] Convert to DECOY format
- [ ] Load into environment without errors

### Phase 3: Simulation Validation
- [ ] Load CS2 map geometry
- [ ] Verify coordinate transforms
- [ ] Run basic simulation
- [ ] Compare agent behavior to CS:GO baseline

### Phase 4: Model Training
- [ ] Train on small CS2 dataset
- [ ] Validate convergence
- [ ] Compare metrics to CS:GO models

---

## Known Issues

1. **awpy/demoparser2 not yet integrated**
   - Added to requirements.txt
   - Conversion script is skeleton only
   - Need schema mapping implementation

2. **No automated map extraction**
   - Manual process via ValveResourceFormat
   - Community tools still maturing for CS2

3. **No CS2 training data yet**
   - Need to download professional CS2 demos
   - Recommend starting with Major tournaments

---

## Next Steps

### Immediate (This Week)
1. Install dependencies: `pip install -r requirements.txt`
2. Download 1-2 CS2 demo files from HLTV
3. Parse with awpy and inspect data structure
4. Map CS2 schema to DECOY format
5. Implement conversion in `convert_cs2_demos.py`

### Short Term (This Month)
1. Extract de_dust2 from CS2 game files
2. Convert to FBX and test in environment
3. Process small batch of CS2 demos
4. Run initial training experiments

### Long Term (Next Quarter)
1. Process full CS2 tournament dataset
2. Retrain all models
3. Validate simulation accuracy
4. Benchmark against CS:GO baseline

---

## Resources

### CS2 Parsers
- awpy: https://github.com/pnxenopoulos/awpy
- demoparser2: https://github.com/LaihoE/demoparser
- awpy docs: https://awpy.readthedocs.io/

### Map Extraction
- ValveResourceFormat: https://github.com/ValveResourceFormat/ValveResourceFormat
- CS2 Workshop Tools: https://developer.valvesoftware.com/wiki/Counter-Strike_2_Workshop_Tools

### Demo Sources
- HLTV: https://www.hltv.org/results (Professional matches)
- ESL: https://play.eslgaming.com/
- Steam Workshop: Community created content

---

## Questions / Blockers

**Data Format:**
- [ ] Is CS2 replay schema compatible with existing pipeline?

**Map Geometry:**
- [ ] Are CS2 coordinate systems identical to CS:GO?
- [ ] Do physics properties match?

**Gameplay Mechanics:**
- [ ] Have movement speeds changed?
- [ ] Have weapon damage values changed?
- [ ] Are round timings different?

---

Last Updated: 2026-08-31
Status: Data pipeline migration in progress
