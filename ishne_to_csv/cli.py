import argparse
import os
from .core import ishne_to_csv

def main():
    parser = argparse.ArgumentParser(description="Convert ISHNE file to CSV with timestamps.")
    parser.add_argument("input_file", help="Path to the input ISHNE file.")
    parser.add_argument("--output_file", help="Path to the output CSV file (optional).")
    parser.add_argument("--no_progress", action="store_false", default=True, help="Disable progress bar.")
    parser.add_argument("--verbose", action="store_true", default=True, help="Enable verbose output.")
    parser.add_argument("--chunk_size", type=int, default=1000, help="Samples per read chunk.")
    parser.add_argument("--write_chunk_size", type=int, default=10000, help="Samples before writing to CSV.")

    args = parser.parse_args()
    output_file = args.output_file or f"{os.path.splitext(args.input_file)[0]}.csv"

    ishne_to_csv(
        args.input_file,
        output_file,
        args.no_progress,
        args.verbose,
        args.chunk_size,
        args.write_chunk_size
    )
