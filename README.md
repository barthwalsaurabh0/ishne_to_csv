# ISHNE to CSV Converter

This Python package provides a utility to convert ISHNE Holter ECG files (`.ISHNE`) into CSV format with timestamped entries in Unix epoch nanoseconds.

## ISHNE Format

| Description | Data Type | No. of Bytes |
|-------------|-----------|--------------|
| Size (in bytes) of variable-length block | long int | 4 |
| Size (in samples) of ECG | long int | 4 |
| Offset of variable-length block (from beginning of file) | long int | 4 |
| Offset of ECG block (from beginning of file) | long int | 4 |
| Version of the file | short int | 2 |
| Subject First Name | char[40] | 40 |
| Subject Last Name | char[40] | 40 |
| Subject ID | char[20] | 20 |
| Subject Sex (0: unknown, 1: male, 2: female) | short int | 2 |
| Race (0: unknown, 1: Caucasian, 2: Black, 3: Oriental, 4–9: Reserved) | short int | 2 |
| Date of Birth (day, month, year) | 3 × short int | 6 |
| Date of Recording (day, month, year) | 3 × short int | 6 |
| Date of Output File Creation (day, month, year) | 3 × short int | 6 |
| Start Time (hour [0–23], minute, second) | 3 × short int | 6 |
| Number of Stored Leads | short int | 2 |
| Lead Specification (see lead specification table) | 12 × short int | 24 |
| Lead Quality (see lead quality table) | 12 × short int | 24 |
| Amplitude Resolution (integer number of nV) | 12 × short int | 24 |
| Pacemaker Code (see description) | short int | 2 |
| Type of Recorder (analog or digital) | char[40] | 40 |
| Sampling Rate (in Hz) | short int | 2 |
| Proprietary Information (if any) | char[80] | 80 |
| Copyright & Restriction of Diffusion (if any) | char[80] | 80 |
| Reserved | char[88] | 88 |

For complete details of the ISHNE format, please refer to [The ISHNE Holter Standard Output File Format](https://www.amps-llc.com/uploads/2017-12-7/The_ISHNE_Format.pdf).

## Features

- Efficient chunked reading of large ISHNE binary ECG files
- Converts all leads with correct timestamp for each sample
- Timestamps are calculated using the start time and sampling rate
- Progress bar to track conversion of large datasets
- Metadata printed in a readable format (name, date, time, leads, etc.)
- CLI support for direct command-line use
- Output CSV includes `time` column as the first column (nanoseconds)

## Installation

Install from PyPI:

```bash
pip install ishne_to_csv
```

## Usage

### As a Python Module

```python
from ishne_to_csv import ishne_to_csv

# Basic usage
ishne_to_csv("example.ISHNE")

# With parameters
ishne_to_csv("example.ISHNE", output_file="example.csv", show_progress=True, verbose=True, chunk_size=1000, write_chunk_size=10000)
```

### CLI Usage

```bash
python -m ishne_to_csv <input_file.ISHNE> [--output_file OUTPUT.csv] [--no_progress] [--verbose] [--chunk_size N] [--write_chunk_size M]
```

## CLI Parameters

| Argument | Description |
|----------|-------------|
| `input_file` | Path to the input ISHNE file (required) |
| `--output_file` | Optional output file path (default: same as input file but with `.csv`) |
| `--no_progress` | Disable progress bar |
| `--verbose` | Print ISHNE file metadata |
| `--chunk_size` | Number of samples per read chunk (default: 1000) |
| `--write_chunk_size` | Number of samples to accumulate before writing to CSV (default: 10000) |


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full license text.