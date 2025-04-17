import pylsl
print("Looking for LSL streams...")

streams = pylsl.resolve_streams()
print(f"Found {len(streams)} streams!")

if streams:
    inlet = pylsl.StreamInlet(streams[0])
    info = inlet.info()
    print("\n--- Stream Metadata ---")
    print(f"Name: {info.name()}")
    print(f"Type: {info.type()}")
    print(f"Channel Count: {info.channel_count()}")
    print(f"Sampling Rate: {info.nominal_srate()}")
    print(f"Channel Format: {info.channel_format()}")
    print("\nListening for data...")
    while True:
        sample, timestamp = inlet.pull_sample(timeout=1.0)
        if sample:
            print(sample)
            print(f"Received: {sample} at {timestamp:.6f}")
        else:
            print("No sample received.")
            
else:
    print("No streams found. Check network settings.")
