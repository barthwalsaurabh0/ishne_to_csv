# ISHNE to CSV Converter

This Python package provides a utility to convert ISHNE Holter ECG files (.ISHNE) into CSV format with timestamped entries in Unix epoch nanoseconds.

## Features

- Reads large ISHNE ECG binary files efficiently in chunks
- Converts all lead samples with accurate timestamps
- Outputs data in CSV format with `time` as the first column (in nanoseconds)
- Displays progress bar for large files
- Automatically extracts metadata (e.g., patient info, recording start time, sampling rate)
- Includes a CLI for easy usage

## Installation

You can install directly from your local copy:

```bash
pip install .
```

To use as a module:

```python
from ishne_to_csv import ishne_to_csv

ishne_to_csv("example.ISHNE")
```

## CLI Usage

```bash
python -m ishne_to_csv <input_file.ISHNE> [--output_file OUTPUT.csv] [--no_progress] [--verbose] [--chunk_size N] [--write_chunk_size M]
```

### Parameters

- `input_file`: Path to the input ISHNE file (required)
- `--output_file`: Optional output path (default: same name with `.csv`)
- `--no_progress`: Disable the progress bar
- `--verbose`: Show ISHNE metadata
- `--chunk_size`: Number of samples per read chunk (default 1000)
- `--write_chunk_size`: Number of samples before writing to file (default 10000)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Developed by [Your Name].
