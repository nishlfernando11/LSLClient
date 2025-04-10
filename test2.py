from pylsl import resolve_streams, StreamInlet

# Use the discovered stream
print("Looking for LSL stream...")
streams = resolve_streams()

if streams:
    print("Stream found:", streams[0].name())
    inlet = StreamInlet(streams[0])

    print("Waiting for data...")
    for _ in range(5):
        sample, timestamp = inlet.pull_sample(timeout=5)
        if sample is None:
            print("No data received (timeout)")
        else:
            print(f"{timestamp}: {sample}")
else:
    print("No streams found.")
