#!/usr/bin/env python3
"""
Simple demo script to analyse a CSV file using the cluster_maker package.

Usage:
    python demo/analyse_from_csv.py path/to/input.csv

If the number of command line arguments is not exactly 2 the script prints
an error message, a short usage line and exits without a traceback.
"""
from __future__ import annotations

import os
import sys

import pandas as pd

from cluster_maker.data_analyser import numeric_statistics
from cluster_maker.data_exporter import export_summary


USAGE = "Usage: python demo/analyse_from_csv.py path/to/input.csv"


def main(argv: list[str]) -> None:
    # Expect exactly two entries in argv: script name and input path
    if len(argv) != 2:
        print("ERROR: Incorrect number of arguments provided.")
        print(USAGE)
        # Exit cleanly without a traceback
        sys.exit(1)

    input_path = argv[1]
    print(f"Reading input CSV: {input_path}")

    if not os.path.exists(input_path):
        print(f"ERROR: The file '{input_path}' does not exist.")
        sys.exit(1)

    try:
        df = pd.read_csv(input_path)
    except Exception as exc:
        print(f"ERROR: Failed to read CSV file: {exc}")
        sys.exit(1)

    print("Computing numeric summary (mean, sd, min, max, n_missing)...")
    try:
        summary = numeric_statistics(df)
    except Exception as exc:
        print(f"ERROR: Failed to compute numeric summary: {exc}")
        sys.exit(1)

    # Ensure output directory exists
    out_dir = os.path.join(os.getcwd(), "demo_output")
    os.makedirs(out_dir, exist_ok=True)

    csv_out = os.path.join(out_dir, "numeric_summary.csv")
    text_out = os.path.join(out_dir, "numeric_summary.txt")

    print(f"Writing summary CSV to: {csv_out}")
    print(f"Writing human-readable summary to: {text_out}")

    try:
        export_summary(summary, csv_out, text_out)
    except Exception as exc:
        print(f"ERROR: Failed to export summary: {exc}")
        sys.exit(1)

    print("Done. Files saved to 'demo_output' directory.")


if __name__ == "__main__":
    main(sys.argv)
