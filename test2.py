import pylsl

print("Looking for LSL streams...")

# ✅ Try resolving by stream name
streams = pylsl.resolve_byprop('name', 'Your_LSL_Stream_Name', timeout=10)

if streams:
    print(f"Found {len(streams)} streams!")
    inlet = pylsl.StreamInlet(streams[0])
    
    while True:
        sample, timestamp = inlet.pull_sample()
        print(f"Received: {sample} at {timestamp:.6f}")
else:
    print("Stream not found. Check network settings.")


# import pylsl

# print("Looking for LSL streams...")

# # ✅ Try resolving by stream name
# streams = pylsl.resolve_byprop('name', 'Eye_Tracker_Stream', timeout=10)

# if streams:
#     print(f"Found {len(streams)} streams!")
#     inlet = pylsl.StreamInlet(streams[0])
    
#     while True:
#         sample, timestamp = inlet.pull_sample()
#         print(f"Received: {sample} at {timestamp:.6f}")
# else:
#     print("Stream not found. Check network settings.")


# import pylsl

# print("Looking for C# LSL streams...")

# # ✅ Resolve LSL stream by source_id
# streams = pylsl.resolve_byprop('source_id', 'Equivital', timeout=100)

# if streams:
#     print(f"Found {len(streams)} streams!")
#     inlet = pylsl.StreamInlet(streams[0])
    
#     while True:
#         sample, timestamp = inlet.pull_sample()
#         print(f"Received: {sample} at {timestamp:.6f}")
# else:
#     print("C# LSL stream not found. Check network settings.")
