## Python (Environment Python 3.10)


import os
import pandas as pd
import json
import pyxdf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import argparse

def load_stream2_data(xdf_file):
    # Load the xdf file
    data, _ = pyxdf.load_xdf(xdf_file)
    # print(data)
    # print(data.__dict__)
    # Extract Stream 2 (GameData)
    # stream1 = next(stream for stream in data if stream['info']['name'][0] == 'EQ_HR_Stream')
    # stream2 = next(stream for stream in data if stream['info']['name'][0] == 'EQ_GSR_Stream')
    alldata = {}
    for stream in data:
        # stream2 = next(stream for stream in data)
        # print(stream2)
        # Extract time-stamped GameData
        timestamps = stream['time_stamps']
        samples = stream['time_series']
    
    # Parse samples (GameData JSON strings)
        parsed_samples = [json.loads(sample[0]) for sample in samples]
        # print(parsed_samples)
        # print(timestamps, parsed_samples)
        stream_name = stream['info']['name'][0]  # Ensure this is a string
        alldata[stream_name] = {
            "timestamps": timestamps.tolist(),
            "samples": parsed_samples
        }
    # Save JSON
    filename = args.file_path.split("/")[-1]
    save_filename = f"data/{filename.split('.')[0]}.json"
    with open(save_filename, "w") as file:
        json.dump(alldata, file, indent=4)  # Added indent for readability

    return timestamps, samples

# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an XDF file and save JSON output.")
    parser.add_argument("file_path", type=str, help="Path to the XDF file")
    
    args = parser.parse_args()

    # **Step 1: Load & Extract Data**
    xdf_file = args.file_path or "block_.xdf"
    if args.file_path:
        filename = args.file_path
        print(filename)
        load_stream2_data(filename) #sub-P001_ses-S001_task-Default_run-001_beh #oaiET_AF1001




# def inspect_xdf(xdf_file):
#     # Load XDF file
#     data, header = pyxdf.load_xdf(xdf_file)
    
#     # Print stream names and their expected sampling rates
#     for stream in data:
#         stream_name = stream['info']['name'][0]
#         nominal_rate = stream['info']['nominal_srate'][0]
#         num_samples = len(stream['time_stamps'])
        
#         print(f"Stream: {stream_name}")
#         print(f"  - Expected Sampling Rate: {nominal_rate} Hz")
#         print(f"  - Recorded Samples: {num_samples}")
        
#         if num_samples > 0:
#             duration = stream['time_stamps'][-1] - stream['time_stamps'][0]
#             effective_rate = num_samples / duration if duration > 0 else 0
#             print(f"  - Effective Sampling Rate: {effective_rate:.4f} Hz\n")
#         else:
#             print("  - No Data Recorded!\n")

# Run the function to inspect the XDF file
# inspect_xdf('sub-P001_ses-S002_task-Default_run-001_eeg.xdf')

# import pyxdf
# import numpy as np
# import pandas as pd
# import json
# from scipy.interpolate import interp1d

# def extract_numeric_values(sample):
#     """
#     Extract only numeric values from a sample.
#     Supports arrays and JSON strings.
#     """
#     if isinstance(sample, str):  # Handle JSON string case
#         try:
#             sample_dict = json.loads(sample)  # Convert JSON to dictionary
#             return [float(value) for value in sample_dict.values() if isinstance(value, (int, float))]
#         except json.JSONDecodeError:
#             return []  # Skip non-JSON strings
#     elif isinstance(sample, (list, np.ndarray)):
#         return [float(value) for value in sample if isinstance(value, (int, float))]
#     else:
#         return []  # Skip unexpected types

# def load_synced_xdf(xdf_file):
#     """
#     Load an XDF file, extract numeric values from all streams, and synchronize them using timestamp interpolation.
#     """
#     # Load the XDF file
#     data, _ = pyxdf.load_xdf(xdf_file)

#     # Extract available streams
#     streams = {stream['info']['name'][0]: stream for stream in data}

#     # Ensure at least two streams exist
#     if len(streams) < 2:
#         raise ValueError("XDF file must contain at least two LSL streams for synchronization.")

#     # Extract timestamps & samples for all streams
#     stream_data = {}
#     max_channels = 0  # Track max number of channels in any stream

#     for stream_name, stream in streams.items():
#         timestamps = np.array(stream['time_stamps'])
#         raw_samples = stream['time_series']

#         if len(timestamps) == 0 or len(raw_samples) == 0:
#             print(f"Warning: Stream '{stream_name}' has no data!")
#             continue  # Skip empty streams

#         # Process samples, extracting only numeric values
#         samples = np.array([extract_numeric_values(sample) for sample in raw_samples])

#         # Ensure consistent dimensions
#         if samples.ndim == 1:
#             samples = samples.reshape(-1, 1)  # Convert 1D data to 2D

#         if samples.shape[1] == 0:
#             print(f"Skipping stream '{stream_name}' due to lack of numeric data.")
#             continue

#         max_channels = max(max_channels, samples.shape[1])  # Track max channels

#         # Store processed numeric data
#         stream_data[stream_name] = {"timestamps": timestamps, "samples": samples}

#     # Determine the reference stream (earliest start time)
#     ref_stream = min(stream_data, key=lambda s: stream_data[s]["timestamps"][0])
#     ref_timestamps = stream_data[ref_stream]["timestamps"]

#     # Initialize DataFrame with timestamps
#     synced_data = {"timestamps": ref_timestamps}

#     # Interpolate all streams to match the reference timestamps
#     for stream_name, data in stream_data.items():
#         for ch in range(data["samples"].shape[1]):  # Handle multi-channel data
#             column_name = f"{stream_name}_Ch{ch+1}"  # Name each channel separately
#             f_interp = interp1d(
#                 data["timestamps"], data["samples"][:, ch], axis=0, kind="linear", fill_value="extrapolate"
#             )
#             synced_data[column_name] = f_interp(ref_timestamps)  # Interpolate to match reference timestamps

#     # Convert to DataFrame for easier handling
#     df = pd.DataFrame(synced_data)

#     return df

# # Load and process the XDF file
# xdf_file = "sub-P001_ses-S001_task-Default_run-001_beh.xdf"
# synced_df = load_synced_xdf(xdf_file)

# # Display the synchronized data
# import ace_tools as tools
# tools.display_dataframe_to_user(name="Synchronized XDF Data", dataframe=synced_df)

# synced_df.to_csv("synced_data.csv", index=False)
