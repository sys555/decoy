#!/usr/bin/env python3
"""
Test script to verify CS2 parsing setup.

Usage:
    python test_cs2_parsing.py /path/to/demo.dem
"""

import sys
from pathlib import Path

def test_imports():
    """Test that required packages are installed."""
    print("Testing imports...")

    try:
        import awpy
        print(f"✓ awpy installed (version: {awpy.__version__ if hasattr(awpy, '__version__') else 'unknown'})")
        awpy_ok = True
    except ImportError:
        print("✗ awpy not installed. Run: pip install awpy")
        awpy_ok = False

    try:
        import demoparser2
        print(f"✓ demoparser2 installed")
        dp2_ok = True
    except ImportError:
        print("✗ demoparser2 not installed. Run: pip install demoparser2")
        dp2_ok = False

    return awpy_ok or dp2_ok


def test_parse_demo(demo_path):
    """Test parsing a CS2 demo file."""
    print(f"\nTesting demo parsing: {demo_path}")

    if not Path(demo_path).exists():
        print(f"✗ Demo file not found: {demo_path}")
        return False

    try:
        from awpy import Demo

        print("Parsing demo with awpy...")
        demo = Demo(demo_path)
        demo.parse()

        print(f"✓ Demo parsed successfully")
        print(f"  Map: {demo.header.get('map_name', 'unknown')}")
        print(f"  Rounds: {len(demo.rounds) if hasattr(demo, 'rounds') else 'N/A'}")

        if hasattr(demo, 'rounds') and len(demo.rounds) > 0:
            round0 = demo.rounds[0]
            print(f"\n  Round 0 info:")

            if hasattr(round0, 'frames') and round0.frames is not None:
                print(f"    Frames: {len(round0.frames)}")
                print(f"    Frame columns: {round0.frames.columns.tolist()[:10]}...")

                # Show sample frame
                if len(round0.frames) > 0:
                    sample = round0.frames.iloc[0]
                    print(f"\n    Sample frame data:")
                    for col in ['tick', 'player_name', 'team_name', 'x', 'y', 'z', 'health']:
                        if col in sample:
                            print(f"      {col}: {sample[col]}")

            if hasattr(round0, 'round_end_reason'):
                print(f"    End reason: {round0.round_end_reason}")

            if hasattr(round0, 'winner_team'):
                print(f"    Winner: {round0.winner_team}")

        return True

    except Exception as e:
        print(f"✗ Error parsing demo: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_conversion():
    """Test the conversion script."""
    print("\nTesting conversion script...")

    try:
        from convert_cs2_demos import convert_awpy_round_to_decoy_format
        print("✓ Conversion functions imported successfully")
        return True
    except Exception as e:
        print(f"✗ Error importing conversion functions: {e}")
        return False


def main():
    print("=" * 60)
    print("CS2 Parsing Setup Test")
    print("=" * 60)

    # Test imports
    if not test_imports():
        print("\n✗ Required packages not installed")
        print("Run: pip install -r requirements.txt")
        return 1

    # Test conversion script
    test_conversion()

    # Test demo parsing if path provided
    if len(sys.argv) > 1:
        demo_path = sys.argv[1]
        if test_parse_demo(demo_path):
            print("\n✓ All tests passed!")
            print("\nNext steps:")
            print("1. Run: python convert_cs2_demos.py <demo_dir> --output data/cs2_parsed")
            print("2. Check output JSON files")
            print("3. Process with trainer/data_processing.py")
            return 0
        else:
            print("\n✗ Demo parsing failed")
            return 1
    else:
        print("\n⚠ No demo file provided for parsing test")
        print("Usage: python test_cs2_parsing.py /path/to/demo.dem")
        print("\nTo download CS2 demos:")
        print("  - Visit https://www.hltv.org/results")
        print("  - Click on a match and download GOTV demo")
        return 0


if __name__ == "__main__":
    sys.exit(main())
