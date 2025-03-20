import pylsl
import csv
import time

# List of streams to record
stream_names = [
    "EQ_ECG_Stream", "EQ_HR_Stream", "EQ_RR_Stream", 
    "EQ_IR_Stream", "EQ_SkinTemp_Stream", "EQ_Accel_Stream", 
    "EQ_GSR_Stream", "Eye_Tracker_Stream"
]

# Open CSV file for writing
with open("lsl_recorded_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "stream_name", "data"])  # Header

    print("Looking for LSL streams...")
    streams = [pylsl.resolve_byprop("name", name) for name in stream_names]
    inlets = {name: pylsl.StreamInlet(stream[0]) for name, stream in zip(stream_names, streams) if stream}

    print(f"Recording {len(inlets)} streams... Press Ctrl+C to stop.")

    try:
        while True:
            for name, inlet in inlets.items():
                sample, timestamp = inlet.pull_sample(timeout=0.1)
                if sample:
                    writer.writerow([timestamp, name, sample])
            time.sleep(0.01)  # Prevent CPU overuse
    except KeyboardInterrupt:
        print("Recording stopped.")
