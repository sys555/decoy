#!/usr/bin/env python3
"""
Download and extract CS2 map geometry for DECOY simulation.

CS2 uses Source 2 engine with different map formats than CS:GO.
This script helps extract map geometry from CS2 game files.
"""

import os
import sys
import subprocess
from pathlib import Path

def find_cs2_install():
    """Try to locate CS2 installation directory."""
    common_paths = [
        Path.home() / ".steam/steam/steamapps/common/Counter-Strike Global Offensive",
        Path.home() / ".local/share/Steam/steamapps/common/Counter-Strike Global Offensive",
        Path("C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive"),
        Path("C:/Program Files/Steam/steamapps/common/Counter-Strike Global Offensive"),
    ]

    for path in common_paths:
        if path.exists():
            print(f"Found CS2 installation at: {path}")
            return path

    return None


def extract_map_with_valve_resource_format(map_name="de_dust2"):
    """
    Extract CS2 map using ValveResourceFormat (Decompiler).

    Requires: https://github.com/ValveResourceFormat/ValveResourceFormat
    Install: Download latest release from GitHub
    """
    cs2_path = find_cs2_install()
    if not cs2_path:
        print("CS2 installation not found.")
        print("Please install CS2 from Steam or specify the path manually.")
        return False

    map_path = cs2_path / "game/csgo/maps" / f"{map_name}.vpk"

    if not map_path.exists():
        print(f"Map not found: {map_path}")
        return False

    # TODO: Call ValveResourceFormat Decompiler to extract map
    # This requires the VRF tool to be installed
    print(f"Map found: {map_path}")
    print("\nTo extract the map:")
    print("1. Download ValveResourceFormat from:")
    print("   https://github.com/ValveResourceFormat/ValveResourceFormat/releases")
    print("2. Run: Decompiler.exe --input <map_file> --output env/assets/")
    print("3. Export geometry as FBX or glTF format")

    return True


def download_community_map(map_name="de_dust2"):
    """
    Download pre-extracted CS2 map from community sources.

    Note: You may need to find or create these yourself.
    The CS2 community may have shared resources.
    """
    print(f"\nCommunity map download for {map_name}:")
    print("CS2 map extraction is still evolving in the community.")
    print("\nOptions:")
    print("1. Check gamebanana.com for CS2 map exports")
    print("2. Use Blender Source Tools with CS2 support")
    print("3. Extract from game files using ValveResourceFormat")

    # TODO: Add actual download logic when community resources are established

    return False


def convert_to_fbx(input_file, output_file):
    """Convert extracted map to FBX format for Panda3D."""
    # TODO: Implement conversion if needed
    # May require Blender automation
    pass


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Download/extract CS2 map geometry for DECOY"
    )
    parser.add_argument(
        "--map",
        type=str,
        default="de_dust2",
        help="Map name (e.g., de_dust2, de_inferno)"
    )
    parser.add_argument(
        "--method",
        type=str,
        choices=["auto", "valve-tool", "community"],
        default="auto",
        help="Extraction method"
    )

    args = parser.parse_args()

    print(f"=== CS2 Map Downloader for {args.map} ===\n")

    if args.method in ["auto", "valve-tool"]:
        if extract_map_with_valve_resource_format(args.map):
            return

    if args.method in ["auto", "community"]:
        download_community_map(args.map)

    print("\n=== Manual Instructions ===")
    print("For now, CS2 map extraction requires manual steps:")
    print("\n1. Install ValveResourceFormat:")
    print("   https://github.com/ValveResourceFormat/ValveResourceFormat/releases")
    print("\n2. Locate your CS2 installation")
    print("   (usually in Steam/steamapps/common/Counter-Strike Global Offensive)")
    print("\n3. Extract map:")
    print(f"   Decompiler.exe --input game/csgo/maps/{args.map}.vpk")
    print("\n4. Export geometry as FBX and place in env/assets/")


if __name__ == "__main__":
    main()
