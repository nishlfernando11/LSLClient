import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import StreamInlet, resolve_byprop, proc_ALL
from scipy.interpolate import interp1d
import time

# 1️⃣ Resolve HR and ECG LSL streams
streams = resolve_byprop('name', 'EQ_HR_Stream')
hr_inlet = StreamInlet(streams[0], processing_flags=proc_ALL)

streams = resolve_byprop('name', 'EQ_ECG_Stream')
ecg_inlet = StreamInlet(streams[0], processing_flags=proc_ALL)

# Data storage
hr_timestamps, hr_data = [], []
ecg_timestamps, ecg_data = [], []

# Setup Matplotlib figure
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlabel("Time (s)")
ax.set_ylabel("Signal Amplitude")
ax.set_title("Real-Time HR & ECG Synchronization")
hr_line, = ax.plot([], [], 'bo-', label="HR (0.2 Hz)")
ecg_line, = ax.plot([], [], 'r--', label="ECG (256 Hz)")
ax.legend()

# 2️⃣ Real-time data collection function
def update(frame):
    global hr_timestamps, hr_data, ecg_timestamps, ecg_data

    # Get HR data (every 5 sec)
    # sample, timestamp = hr_inlet.pull_sample(timeout=5.5)
    # if sample:
    #     hr_timestamps.append(timestamp)
    #     hr_data.append(sample[0])
    
    # Get ECG data (continuously at 256 Hz)
    for _ in range(256):  
        sample, timestamp = ecg_inlet.pull_sample(timeout=0.5)
        if sample:
            ecg_timestamps.append(timestamp)
            ecg_data.append(sample[0])
    
    # Keep last 60 sec of data for plotting
    time_window = 60  # seconds

    # 🛠 FIX: Only filter timestamps if they are non-empty
    # if hr_timestamps and hr_data:
    #     filtered_hr = [(t, d) for t, d in zip(hr_timestamps, hr_data) if t > time.time() - time_window]
    #     if filtered_hr:  # Ensure there's at least one sample
    #         hr_timestamps, hr_data = zip(*filtered_hr)
    #     else:
    #         hr_timestamps, hr_data = [], []  # Reset to empty if no valid samples

    if ecg_timestamps and ecg_data:
        filtered_ecg = [(t, d) for t, d in zip(ecg_timestamps, ecg_data) if t > time.time() - time_window]
        if filtered_ecg:
            ecg_timestamps, ecg_data = zip(*filtered_ecg)
        else:
            ecg_timestamps, ecg_data = [], []

    # # Interpolate ECG to match HR timestamps
    # if len(ecg_timestamps) > 2 and len(hr_timestamps) > 2:
    #     ecg_interpolator = interp1d(ecg_timestamps, ecg_data, kind='linear', fill_value="extrapolate")
    #     aligned_ecg = ecg_interpolator(hr_timestamps)
    # else:
    #     aligned_ecg = np.zeros(len(hr_timestamps))  # Placeholder if not enough data

    # Update plots
    # hr_line.set_data(hr_timestamps, hr_data)
    ecg_line.set_data(hr_timestamps, ecg_data)
    ax.relim()
    ax.autoscale_view()

    return ecg_line

# 3️⃣ Start real-time animation (Fix: add `cache_frame_data=False`)
ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
plt.show()
