import pyxdf
import json
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import argparse

def extract_numeric_values(json_data):
    """
    Extracts only numeric values from a JSON object.
    Ignores strings like 'session_id' and keeps timestamps & numerical values.
    """
    try:
        parsed_data = json.loads(json_data)  # Parse JSON string
        return {key: float(value) for key, value in parsed_data.items() if isinstance(value, (int, float))}
    except json.JSONDecodeError:
        return {}  # Return empty if JSON parsing fails

def load_xdf_data(xdf_file):
    """
    Loads an XDF file and extracts numeric values from all streams.
    Uses `time_stamps` as the primary timestamps for synchronization.
    """
    data, _ = pyxdf.load_xdf(xdf_file)
    stream_data = {}

    for stream in data:
        stream_name = stream['info']['name'][0]
        timestamps = np.array(stream['time_stamps'])  # Use time_stamps directly
        samples = [extract_numeric_values(sample[0]) for sample in stream['time_series']]

        if len(samples) == 0 or len(timestamps) == 0:
            print(f"Skipping empty stream: {stream_name}")
            continue  # Skip streams with no valid data

        # Convert samples list to a DataFrame
        df_samples = pd.DataFrame(samples)
        df_samples.insert(0, "time_stamps", timestamps)  # Insert LSL timestamps

        stream_data[stream_name] = df_samples

    return stream_data

def synchronize_streams(stream_data):
    """
    Synchronizes all streams by interpolating them to a common `time_stamps` axis.
    """
    if not stream_data:
        raise ValueError("No valid streams found to synchronize.")

    # Choose the stream with the earliest start time as the reference
    ref_stream = min(stream_data.keys(), key=lambda s: stream_data[s]["time_stamps"].min())
    ref_timestamps = stream_data[ref_stream]["time_stamps"].values

    synced_data = {"time_stamps": ref_timestamps}

    for stream_name, df in stream_data.items():
        for col in df.columns:
            if col == "time_stamps":
                continue  # Skip timestamp column

            # Interpolate each numeric column to match the reference timestamps
            f_interp = interp1d(df["time_stamps"], df[col], kind="linear", fill_value="extrapolate")
            synced_data[f"{stream_name}_{col}"] = f_interp(ref_timestamps)

    # Convert synchronized data to a DataFrame
    df_synced = pd.DataFrame(synced_data)
    return df_synced



# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an XDF file and save JSON output.")
    parser.add_argument("file_path", type=str, help="Path to the XDF file")
    
    args = parser.parse_args()

    # **Step 1: Load & Extract Data**
    xdf_file = args.file_path or "sub-P001_ses-S001_task-Default_run-001_eeg"
    if args.file_path:
        filename = args.file_path.split("/")[-1]
        stream_data = load_xdf_data(xdf_file)

        # **Step 2: Synchronize Data by `time_stamps`**
        synced_df = synchronize_streams(stream_data)

        print(synced_df.head())  # Show the first few rows

        synced_df.to_csv(f"data_csv/{filename.split('.')[0]}.csv", index=False)
        print("Synchronized data saved to synced_data.csv")
    else:
        print("Error: file name is missing.")

