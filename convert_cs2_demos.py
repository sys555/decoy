#!/usr/bin/env python3
"""
Convert CS2 demo files to the format used by DECOY training pipeline.

This script uses awpy to parse CS2 demos and converts them to the same
JSON/NPZ format that the original CS:GO data processing expects.
"""

import os
import json
import argparse
from pathlib import Path
from tqdm import tqdm
import numpy as np

try:
    from awpy import Demo
    AWPY_AVAILABLE = True
except ImportError:
    AWPY_AVAILABLE = False
    print("Warning: awpy not installed. Run: pip install awpy")

try:
    from demoparser2 import DemoParser
    DEMOPARSER_AVAILABLE = True
except ImportError:
    DEMOPARSER_AVAILABLE = False
    print("Warning: demoparser2 not installed. Run: pip install demoparser2")


def parse_cs2_demo_awpy(demo_path):
    """Parse CS2 demo using awpy and convert to DECOY format."""
    if not AWPY_AVAILABLE:
        raise RuntimeError("awpy is required but not installed")

    print(f"Parsing {demo_path} with awpy...")
    demo = Demo(demo_path)

    # Parse the demo
    demo.parse()

    # awpy.Demo provides:
    # - demo.header: map name, tick rate, etc.
    # - demo.rounds: list of Round objects
    # - Each Round has: .frames (DataFrame), .kills, .damages, .bomb_events, etc.

    game_data = {
        "mapName": demo.header.get("map_name", "unknown"),
        "gameRounds": []
    }

    # Convert each round
    for round_obj in demo.rounds:
        round_data = convert_awpy_round_to_decoy_format(round_obj)
        if round_data:
            game_data["gameRounds"].append(round_data)

    return game_data


def convert_awpy_round_to_decoy_format(round_obj):
    """
    Convert an awpy Round object to DECOY's expected JSON format.

    DECOY expects:
    {
        "roundNum": int,
        "roundEndReason": str,
        "winningSide": "T" or "CT",
        "tSide": {"players": [...]},
        "ctSide": {"players": [...]},
        "frames": [
            {
                "tick": int,
                "t": {"players": [{"steamID", "x", "y", "z", "hp", "armor", "hasHelmet", "viewX", "viewY", "isAlive", "hasBomb", "inventory": [...]}]},
                "ct": {"players": [...]},
                "bomb": {"x", "y", "z"}
            }
        ],
        "damages": [...]
    }
    """
    try:
        # awpy Round object has:
        # - round_obj.frames: DataFrame with columns like 'tick', 'seconds', 'player_name', 'team_name', 'x', 'y', 'z', 'health', etc.
        # - round_obj.kills: list of kill events
        # - round_obj.damages: list of damage events
        # - round_obj.bomb_events: plant/defuse events
        # - round_obj.round_end_reason: reason round ended
        # - round_obj.winner_team: 'T' or 'CT'

        frames_df = round_obj.frames
        if frames_df is None or len(frames_df) == 0:
            return None

        # Group frames by tick
        ticks = sorted(frames_df['tick'].unique())

        frames_list = []
        for tick in ticks:
            tick_data = frames_df[frames_df['tick'] == tick]

            frame = {
                "tick": int(tick),
                "t": {"players": []},
                "ct": {"players": []},
                "bomb": {}
            }

            # Process each player in this tick
            for _, player_row in tick_data.iterrows():
                player_data = {
                    "steamID": str(player_row.get('steam_id', player_row.get('player_name', 'unknown'))),
                    "name": str(player_row.get('player_name', 'unknown')),
                    "x": float(player_row.get('x', 0)),
                    "y": float(player_row.get('y', 0)),
                    "z": float(player_row.get('z', 0)),
                    "hp": int(player_row.get('health', 0)),
                    "armor": int(player_row.get('armor_value', 0)),
                    "hasHelmet": bool(player_row.get('has_helmet', False)),
                    "viewX": float(player_row.get('pitch', 0)),  # awpy: pitch/yaw
                    "viewY": float(player_row.get('yaw', 0)),
                    "isAlive": bool(player_row.get('is_alive', True)),
                    "hasBomb": bool(player_row.get('has_bomb', False)),
                    "inventory": []  # TODO: extract from awpy if available
                }

                team = player_row.get('team_name', 'Unknown')
                if team == 'T':
                    frame["t"]["players"].append(player_data)
                elif team == 'CT':
                    frame["ct"]["players"].append(player_data)

            # TODO: Extract bomb position from awpy
            # May need to check bomb_events or dedicated bomb tracking

            frames_list.append(frame)

        # Get team rosters (use first frame to establish player lists)
        t_players = []
        ct_players = []
        if frames_list and len(frames_list) > 0:
            first_frame = frames_list[0]
            t_players = [{"steamID": p["steamID"], "name": p["name"]}
                        for p in first_frame["t"]["players"]]
            ct_players = [{"steamID": p["steamID"], "name": p["name"]}
                         for p in first_frame["ct"]["players"]]

        # Convert damages
        damages_list = []
        if hasattr(round_obj, 'damages') and round_obj.damages is not None:
            for dmg in round_obj.damages:
                damage_data = {
                    "tick": int(dmg.get('tick', 0)),
                    "attackerSteamID": str(dmg.get('attacker_steam_id', 'unknown')),
                    "victimSteamID": str(dmg.get('victim_steam_id', 'unknown')),
                    "hpDamage": int(dmg.get('hp_damage', 0)),
                    "armorDamage": int(dmg.get('armor_damage', 0)),
                    "weapon": str(dmg.get('weapon', 'unknown')),
                    "weaponClass": str(dmg.get('weapon_class', 'unknown')),
                    "hitGroup": str(dmg.get('hit_group', 'Generic')),
                    "isFriendlyFire": bool(dmg.get('is_friendly_fire', False))
                }
                damages_list.append(damage_data)

        round_data = {
            "roundNum": int(round_obj.round_num) if hasattr(round_obj, 'round_num') else 0,
            "roundEndReason": str(round_obj.round_end_reason) if hasattr(round_obj, 'round_end_reason') else "Unknown",
            "winningSide": str(round_obj.winner_team) if hasattr(round_obj, 'winner_team') else "Unknown",
            "tSide": {"players": t_players},
            "ctSide": {"players": ct_players},
            "frames": frames_list,
            "damages": damages_list
        }

        return round_data

    except Exception as e:
        print(f"Error converting round: {e}")
        import traceback
        traceback.print_exc()
        return None


def parse_cs2_demo_demoparser(demo_path):
    """Parse CS2 demo using demoparser2 and convert to DECOY format."""
    if not DEMOPARSER_AVAILABLE:
        raise RuntimeError("demoparser2 is required but not installed")

    print(f"Parsing {demo_path} with demoparser2...")
    parser = DemoParser(demo_path)

    # Get basic info
    header = parser.parse_header()

    # TODO: Extract frame-by-frame data
    # demoparser2 uses a query-based approach

    game_data = {
        "mapName": header.get("map_name", "unknown"),
        "gameRounds": []
    }

    return game_data


def convert_demo_to_npz(demo_path, output_dir, parser="awpy"):
    """
    Convert a CS2 demo file to NPZ format used by DECOY.

    Args:
        demo_path: Path to .dem file
        output_dir: Output directory for NPZ files
        parser: Which parser to use ("awpy" or "demoparser")
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Parse demo
    if parser == "awpy":
        game_data = parse_cs2_demo_awpy(demo_path)
    elif parser == "demoparser":
        game_data = parse_cs2_demo_demoparser(demo_path)
    else:
        raise ValueError(f"Unknown parser: {parser}")

    # Save intermediate JSON for debugging
    demo_name = Path(demo_path).stem
    json_output = output_dir / f"{demo_name}.json"

    with open(json_output, 'w') as f:
        json.dump(game_data, f, indent=2)

    print(f"Saved JSON to {json_output}")

    # Now the JSON can be processed by existing data_processing.py
    # Or we can convert directly to NPZ here

    # For now, just save the JSON - the existing trainer/data_processing.py
    # can read these JSON files and convert to NPZ format

    print(f"Converted {demo_path} -> {json_output}")
    print("To convert to NPZ training format, use trainer/data_processing.py")

    return json_output


def main():
    parser = argparse.ArgumentParser(
        description="Convert CS2 demo files to DECOY training format"
    )
    parser.add_argument(
        "demo_dir",
        type=str,
        help="Directory containing CS2 .dem files"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/cs2_demos_processed",
        help="Output directory for processed data"
    )
    parser.add_argument(
        "--parser",
        type=str,
        choices=["awpy", "demoparser"],
        default="awpy",
        help="Which parser to use"
    )
    parser.add_argument(
        "--map-filter",
        type=str,
        default=None,
        help="Only process demos from this map (e.g., de_dust2)"
    )

    args = parser.parse_args()

    # Find all .dem files
    demo_dir = Path(args.demo_dir)
    demo_files = list(demo_dir.glob("*.dem"))

    if not demo_files:
        print(f"No .dem files found in {demo_dir}")
        return

    print(f"Found {len(demo_files)} demo files")

    # Process each demo
    for demo_path in tqdm(demo_files):
        try:
            convert_demo_to_npz(demo_path, args.output, parser=args.parser)
        except Exception as e:
            print(f"Error processing {demo_path}: {e}")
            continue


if __name__ == "__main__":
    main()
