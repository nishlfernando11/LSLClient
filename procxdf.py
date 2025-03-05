## Python (Environment Python 3.10)


import os
import pandas as pd
import json
import pyxdf
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def load_stream2_data(xdf_file):
    # Load the xdf file
    data, _ = pyxdf.load_xdf(xdf_file)
    print(data)
    # print(data.__dict__)
    # Extract Stream 2 (GameData)
    # stream1 = next(stream for stream in data if stream['info']['name'][0] == 'EQ_HR_Stream')
    stream2 = next(stream for stream in data if stream['info']['name'][0] == 'EQ_HR_Stream')
    
    # Extract time-stamped GameData
    timestamps = stream2['time_stamps']
    samples = stream2['time_series']
    
    # Parse samples (GameData JSON strings)
    # parsed_samples = [json.loads(sample[0]) for sample in samples]
    
    return timestamps, samples


timestamps, samples = load_stream2_data('sub-P001_ses-S001_task-Default_run-001_beh.xdf')
print(timestamps, samples)