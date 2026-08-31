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

    # Extract game data
    # awpy returns data in pandas/polars DataFrames
    # We need to convert to the JSON format expected by data_processing.py

    game_data = {
        "mapName": demo.header.get("map_name", "unknown"),
        "gameRounds": []
    }

    # TODO: Convert awpy output to DECOY format
    # This requires understanding awpy's data schema
    # and mapping it to the CS:GO JSON schema used in data_processing.py

    return game_data


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

    # Convert to NPZ format
    # TODO: Implement the conversion logic
    # This mirrors what data_processing.py does for CS:GO JSON files

    print(f"Converted {demo_path}")


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
