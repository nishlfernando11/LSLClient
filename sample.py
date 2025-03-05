from pylsl import resolve_byprop, StreamInlet

# Resolve streams by their properties (like name)
print("Resolving streams...")
ecg_streams = resolve_byprop('name', 'EQ_ECG_Stream')  # Replace with the actual name
hr_streams = resolve_byprop('name', 'EQ_HR_Stream')    # Replace with the actual name

# Create inlets for these streams
ecg_inlet = StreamInlet(ecg_streams[0])
hr_inlet = StreamInlet(hr_streams[0])

while True:
    ecg_sample, timestamp = ecg_inlet.pull_sample()
    hr_sample, timestamp = hr_inlet.pull_sample()

    print(f"ECG Sample: {ecg_sample}, HR Sample: {hr_sample}")