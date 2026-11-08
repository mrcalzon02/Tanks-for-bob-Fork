#!/usr/bin/env python3
"""Portable Factorio Output CLI: native Blender -> four-way Factorio sprite package.

Examples:
    python3 factorio-output/run.py --job factorio-output/examples/demo-job.json
    python3 factorio-output/run.py --job jobs/my-model.json --publish
    python3 factorio-output/run.py --job jobs/my-model.json --deploy
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from produce_factorio_asset import main

if __name__ == "__main__":
    main()
