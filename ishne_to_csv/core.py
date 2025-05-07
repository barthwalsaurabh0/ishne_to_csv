import struct
import pandas as pd
import datetime
from tqdm import tqdm
import os

def read_ishne(file_path, show_progress=True, verbose=True, chunk_size=1000, write_chunk_size=10000):
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

        # Calculate hours of recording
        hours_of_recording = total_samples / sampling_rate / 3600

        if verbose:
            print("\nISHNE File Info:")
            print(f"  Name        : {first_name} {last_name}")
            print(f"  Subject ID  : {subject_id}")
            print(f"  Sex         : {sex} | Race: {race}")
            print(f"  Record Date : {record_date[0]:02d}-{record_date[1]:02d}-{record_date[2]}")
            print(f"  Start Time  : {start_time[0]:02d}:{start_time[1]:02d}:{start_time[2]:02d}")
            print(f"  Leads       : {num_leads}")
            print(f"  Samples     : {total_samples} ({hours_of_recording:.2f} hours)")
            print(f"  Sampling Hz : {sampling_rate}")
            print()

        f.seek(offset_data)

        data = []
        iterator = tqdm(range(0, total_samples, chunk_size), disable=not show_progress, desc="Reading ECG Samples")

        # Prepare for CSV writing
        output_file = f"{os.path.splitext(file_path)[0]}.csv"  # Default output file is input file name with .csv extension
        header_written = False  # Check if header is written
        
        for i in iterator:
            # Calculate the number of remaining samples and adjust the chunk size for the last read
            remaining_samples = total_samples - i
            current_chunk_size = min(remaining_samples, chunk_size)

            # Read the chunk (account for all leads and samples)
            raw_data = f.read(current_chunk_size * num_leads * 2)  # 2 bytes per sample

            # If raw_data is shorter than expected, we have a problem
            if len(raw_data) != current_chunk_size * num_leads * 2:
                raise ValueError(f"Expected {current_chunk_size * num_leads * 2} bytes, but only {len(raw_data)} bytes were read.")

            # Unpack the raw data into chunks
            chunk = struct.unpack('<' + 'h' * (current_chunk_size * num_leads), raw_data)

            # Reshape the flat data to a list of rows, each row with data for all leads
            for j in range(current_chunk_size):
                row = chunk[j * num_leads: (j + 1) * num_leads]
                data.append(row)

            # Once we've processed enough chunks, write them to a CSV file in chunks
            if len(data) >= write_chunk_size:
                df = pd.DataFrame(data, columns=[f'Lead_{i+1}' for i in range(num_leads)])

                start_datetime = datetime.datetime(
                    year=record_date[2], month=record_date[1], day=record_date[0],
                    hour=start_time[0], minute=start_time[1], second=start_time[2]
                )
                base_epoch_ns = int(start_datetime.timestamp() * 1e9)
                interval_ns = int(1e9 / sampling_rate)
                df.insert(0, 'time', [base_epoch_ns + i * interval_ns for i in range(len(data))])

                if not header_written:
                    df.to_csv(output_file, index=False)
                    header_written = True  # Only write header once
                else:
                    df.to_csv(output_file, index=False, mode='a', header=False)

                data = []  # Reset data for next chunk

        # Final chunk write
        if data:
            df = pd.DataFrame(data, columns=[f'Lead_{i+1}' for i in range(num_leads)])

            start_datetime = datetime.datetime(
                year=record_date[2], month=record_date[1], day=record_date[0],
                hour=start_time[0], minute=start_time[1], second=start_time[2]
            )
            base_epoch_ns = int(start_datetime.timestamp() * 1e9)
            interval_ns = int(1e9 / sampling_rate)
            df.insert(0, 'time', [base_epoch_ns + i * interval_ns for i in range(len(data))])

            if not header_written:
                df.to_csv(output_file, index=False)
            else:
                df.to_csv(output_file, index=False, mode='a', header=False)

    print(f"CSV file written to {output_file}")


def ishne_to_csv(input_file, output_file=None, show_progress=True, verbose=True, chunk_size=1000, write_chunk_size=10000):
    read_ishne(input_file, show_progress, verbose, chunk_size, write_chunk_size)
