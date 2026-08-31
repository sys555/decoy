# CS2 Data Pipeline Quick Start

This guide walks you through converting CS2 demo files to DECOY training format.

## Prerequisites

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Get CS2 demo files:**

Download professional CS2 matches from:
- **HLTV**: https://www.hltv.org/results
  - Click on a match → "Download GOTV Demo"
- **ESL**: https://play.eslgaming.com/
- **Valve Major Tournaments**: Usually available on Steam

Save `.dem` files to a directory, e.g., `data/cs2_demos/`

## Step 1: Parse a Single Demo (Test)

Test the parser on one demo first:

```bash
python convert_cs2_demos.py data/cs2_demos/single_demo.dem --output data/cs2_parsed --parser awpy
```

This will:
- Parse the demo with awpy
- Convert to DECOY JSON format
- Save to `data/cs2_parsed/single_demo.json`

**Check the output:**
```bash
# View the JSON structure
python -c "import json; d=json.load(open('data/cs2_parsed/single_demo.json')); print(f'Map: {d[\"mapName\"]}, Rounds: {len(d[\"gameRounds\"])}')"
```

## Step 2: Validate Schema

Compare the CS2 JSON to the expected format:

```python
import json

# Load CS2 parsed demo
with open('data/cs2_parsed/single_demo.json') as f:
    cs2_data = json.load(f)

# Check structure
print(f"Map: {cs2_data['mapName']}")
print(f"Rounds: {len(cs2_data['gameRounds'])}")

# Check first round
round0 = cs2_data['gameRounds'][0]
print(f"Round 0 - Winner: {round0['winningSide']}, Reason: {round0['roundEndReason']}")
print(f"Frames: {len(round0['frames'])}")
print(f"T players: {len(round0['tSide']['players'])}")
print(f"CT players: {len(round0['ctSide']['players'])}")

# Check first frame
frame0 = round0['frames'][0]
print(f"\nFirst frame tick: {frame0['tick']}")
print(f"T players in frame: {len(frame0['t']['players'])}")
print(f"CT players in frame: {len(frame0['ct']['players'])}")

# Sample player data
if frame0['t']['players']:
    player = frame0['t']['players'][0]
    print(f"\nSample T player:")
    print(f"  Position: ({player['x']:.1f}, {player['y']:.1f}, {player['z']:.1f})")
    print(f"  HP: {player['hp']}, Armor: {player['armor']}")
```

## Step 3: Process Batch of Demos

Once validated, process multiple demos:

```bash
# Process all demos in a directory
python convert_cs2_demos.py data/cs2_demos/ --output data/cs2_parsed --parser awpy

# Filter by map
python convert_cs2_demos.py data/cs2_demos/ --output data/cs2_parsed --parser awpy --map-filter de_dust2
```

## Step 4: Convert to NPZ Training Format

Use the existing data processing pipeline:

```bash
cd trainer
python data_processing.py --data-folder ../data/cs2_parsed --output-dir ../data/cs2_training --map-filter de_dust2
```

This reads the JSON files and creates NPZ files for training.

## Step 5: Verify NPZ Files

```python
import numpy as np

# Load a training sample
data = np.load('data/cs2_training/some_round.npz')

print("Arrays in file:", data.files)
print("Player trajectory shape:", data['player_trajectory'].shape)  # (10, seq_len, 3)
print("Player HP shape:", data['player_hp_timeseries'].shape)  # (10, seq_len)
print("Winning side:", data['winning_side'])
```

## Troubleshooting

### Issue: awpy not parsing correctly

**Solution:** Check awpy version and CS2 compatibility
```bash
pip show awpy
# Should be >= 1.3.0

# Try demoparser2 instead
python convert_cs2_demos.py data/cs2_demos/demo.dem --output data/cs2_parsed --parser demoparser
```

### Issue: Missing player data in frames

**Possible causes:**
- Demo corruption
- CS2 format changes
- awpy API mismatch

**Debug:**
```python
from awpy import Demo

demo = Demo('data/cs2_demos/demo.dem')
demo.parse()

# Inspect raw awpy output
print("Rounds:", len(demo.rounds))
round0 = demo.rounds[0]
print("Round 0 frames columns:", round0.frames.columns.tolist())
print("Sample frame:\n", round0.frames.head())
```

### Issue: Coordinate system mismatch

CS2 may use different coordinates than CS:GO. Check:
```python
# Compare player positions
# CS:GO typically: x in [-3000, 3000], y in [-3000, 3000], z in [-500, 500]
# If CS2 uses different scale, update transform_cs2_to_panda3d() in env/cs2_environment.py
```

## Next Steps

1. **Get CS2 map geometry** (see `download_cs2_map.py`)
2. **Train models** on CS2 data
3. **Validate simulation** accuracy

---

## Advanced: Schema Differences

### awpy API (may vary by version)

Expected DataFrame columns from `round.frames`:
- `tick`: Game tick
- `seconds`: Time in seconds
- `player_name`: Player name
- `steam_id`: SteamID64
- `team_name`: 'T' or 'CT'
- `x`, `y`, `z`: Position
- `health`: HP
- `armor_value`: Armor points
- `has_helmet`: Boolean
- `is_alive`: Boolean
- `has_bomb`: Boolean
- `pitch`, `yaw`: View angles
- `weapon`: Active weapon name

If your awpy version has different columns, update `convert_awpy_round_to_decoy_format()` in `convert_cs2_demos.py`.

---

Last updated: 2026-08-31
