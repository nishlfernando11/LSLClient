# # from mne_lsl.lsl import resolve_streams


# # # Resolve all available LSL streams
# # streams = resolve_streams()

# # from mne_lsl.stream import StreamLSL

# # # Initialize StreamLSL objects for each stream
# # stream_objects = [StreamLSL(name=stream.name(), stype=stream.type()) for stream in streams]

# # # Connect to each stream
# # for stream_obj in stream_objects:
# #     stream_obj.connect()


# # import matplotlib.pyplot as plt

# # # Acquire data from each stream
# # for stream_obj in stream_objects:
# #     data, timestamps = stream_obj.acquire()

# #     # Plot the data
# #     plt.plot(timestamps, data)
# #     plt.title(f"Stream: {stream_obj.name}")
# #     plt.xlabel('Time (s)')
# #     plt.ylabel('Amplitude')
# #     plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from pylsl import StreamInlet, resolve_streams

# # Resolve multiple LSL streams
# streams = resolve_streams()
# inlets = [StreamInlet(s) for s in streams]

# # Setup Matplotlib figure
# fig, ax = plt.subplots(len(inlets), 1, figsize=(10, 6))
# lines = [ax[i].plot([], [], label=streams[i].name())[0] for i in range(len(inlets))]

# # Update function for animation
# def update(frame):
#     for i, inlet in enumerate(inlets):
#         sample, timestamp = inlet.pull_sample(timeout=0.5)
#         if sample:
#             lines[i].set_data(timestamp, sample[0])
#             ax[i].relim()
#             ax[i].autoscale_view()
#     return lines

# ani = animation.FuncAnimation(fig, update, interval=1000)
# plt.show()

from pylsl import StreamInlet, resolve_streams

# Resolve all available LSL streams
streams = resolve_streams()
if not streams:
    print("No active LSL streams found.")
    exit()

# Connect to the first available stream
inlet = StreamInlet(streams[0])

# Try pulling a sample
sample, timestamp = inlet.pull_sample(timeout=2.0)
if sample:
    print(f"Sample received at {timestamp}: {sample}")
else:
    print("No data received from the stream.")


from pylsl import resolve_streams

streams = resolve_streams()
if streams:
    print("Available LSL Streams:", [s.name() for s in streams])
else:
    print("No active LSL streams found!")
