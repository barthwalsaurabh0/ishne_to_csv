import struct
import pandas as pd
import datetime
from tqdm import tqdm
import argparse
import os
import sys

def read_ishne(file_path, show_progress=True, verbose=True):
    with open(file_path, 'rb') as f:
        magic = f.read(8).decode('ascii')
        if magic != 'ISHNE1.0':
            raise ValueError("Not a valid ISHNE file")

        f.read(2)  # Checksum
        variable_header_size = struct.unpack('<I', f.read(4))[0]
        total_samples = struct.unpack('<I', f.read(4))[0]
        offset_variable_header = struct.unpack('<I', f.read(4))[0]
        offset_data = struct.unpack('<I', f.read(4))[0]
        version = struct.unpack('<H', f.read(2))[0]

        first_name = f.read(40).decode('ascii').strip('\x00')
        last_name = f.read(40).decode('ascii').strip('\x00')
        subject_id = f.read(20).decode('ascii').strip('\x00')
        sex = struct.unpack('<H', f.read(2))[0]
        race = struct.unpack('<H', f.read(2))[0]

        birth_date = struct.unpack('<HHH', f.read(6))
        record_date = struct.unpack('<HHH', f.read(6))
        file_date = struct.unpack('<HHH', f.read(6))
        start_time = struct.unpack('<BBB', f.read(3))
        f.read(3)  # Reserved

        num_leads = struct.unpack('<H', f.read(2))[0]
        lead_spec = struct.unpack('<' + 'H' * 12, f.read(24))[:num_leads]
        f.read(24)  # Lead quality
        f.read(24)  # Amplitude resolution
        f.read(2)   # Pacemaker code
        f.read(40)  # Recorder type
        sampling_rate = struct.unpack('<H', f.read(2))[0]

        if sampling_rate == 0:
            raise ValueError("Invalid sampling rate read from file")

        if verbose:
            print("\nISHNE File Info:")
            print(f"  Name        : {first_name} {last_name}")
            print(f"  Subject ID  : {subject_id}")
            print(f"  Sex         : {sex} | Race: {race}")
            print(f"  Record Date : {record_date[0]:02d}-{record_date[1]:02d}-{record_date[2]}")
            print(f"  Start Time  : {start_time[0]:02d}:{start_time[1]:02d}:{start_time[2]:02d}")
            print(f"  Leads       : {num_leads}")
            print(f"  Samples     : {total_samples}")
            print(f"  Sampling Hz : {sampling_rate}")
            print()

        f.seek(offset_data)
        data = []
        iterator = tqdm(range(total_samples), disable=not show_progress, desc="Reading ECG Samples")

        for _ in iterator:
            data.append([struct.unpack('<h', f.read(2))[0] for _ in range(num_leads)])

        df = pd.DataFrame(data, columns=[f'Lead_{i}' for i in range(num_leads)])

        start_datetime = datetime.datetime(
            year=record_date[2], month=record_date[1], day=record_date[0],
            hour=start_time[0], minute=start_time[1], second=start_time[2]
        )
        base_epoch_ns = int(start_datetime.timestamp() * 1e9)
        interval_ns = int(1e9 / sampling_rate)
        df.insert(0, 'time', [base_epoch_ns + i * interval_ns for i in range(total_samples)])

        return df


def ishne_to_csv(input_file, output_file=None, show_progress=True, verbose=True):
    if not output_file:
        base, _ = os.path.splitext(input_file)
        output_file = base + '.csv'

    df = read_ishne(input_file, show_progress=show_progress, verbose=verbose)
    df.to_csv(output_file, index=False)
    if verbose:
        print(f"CSV file written to: {output_file}")

# CLI interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert ISHNE ECG file to CSV with timestamp in UNIX epoch nanoseconds."
    )
    parser.add_argument("input", help="Input ISHNE file path (.ISHNE)")
    parser.add_argument("-o", "--output", help="Output CSV file path (optional)")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress bar")
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")

    args = parser.parse_args()

    try:
        ishne_to_csv(
            input_file=args.input,
            output_file=args.output,
            show_progress=not args.no_progress,
            verbose=not args.quiet
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
