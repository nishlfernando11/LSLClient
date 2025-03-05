import pylsl
import numpy as np
import time
import neurokit2 as nk
from scipy.signal import butter, filtfilt

# --- LSL Setup ---
print("Looking for ECG stream...")
streams = pylsl.resolve_stream('name', 'EQ_ECG_Stream')
inlet = pylsl.StreamInlet(streams[0])

# Create an LSL stream for computed HR & HRV
hr_stream = pylsl.StreamInfo('Computed_HR', 'HR', 1, 1, pylsl.cf_float32, 'hr123')
hr_outlet = pylsl.StreamOutlet(hr_stream)

# --- Filtering Function ---
def bandpass_filter(signal, lowcut=0.5, highcut=50.0, fs=256, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

# --- Storage for RR Intervals ---
rr_intervals = []
ecg_buffer = []  # Buffer to store ECG samples
fs = 256  # Sampling rate in Hz

print("\n--- Receiving ECG data & Computing HR ---")

while True:
    # Get ECG sample
    sample, timestamp = inlet.pull_sample(timeout=1.0)
    
    if sample:
        ecg_buffer.append(sample[0])  # Store latest ECG value

        # Process in windows (2s of data)
        if len(ecg_buffer) >= fs * 2:
            ecg_signal = np.array(ecg_buffer)

            # --- Step 1: Apply Noise Filtering ---
            ecg_filtered = bandpass_filter(ecg_signal)

            # --- Step 2: Detect R-Peaks ---
            try:
                rpeaks = nk.ecg_peaks(ecg_filtered, sampling_rate=fs)['ECG_R_Peaks']
                rpeaks = np.where(rpeaks == 1)[0]  # Get indices of R-peaks

                # Compute RR intervals (time between beats)
                if len(rpeaks) > 1:
                    rr_times = np.diff(rpeaks) / fs  # Convert to seconds
                    
                    if len(rr_times) > 0:
                        hr = 60.0 / rr_times[-1]  # Compute HR in BPM
                        rr_intervals.append(rr_times[-1])  # Store for HRV

                        # --- Step 3: Compute HRV Metrics ---
                        if len(rr_intervals) > 2:
                            sdnn = np.std(rr_intervals) * 1000  # Convert to ms
                            rmssd = np.sqrt(np.mean(np.diff(rr_intervals) ** 2)) * 1000  # Convert to ms

                            print(f"HR: {hr:.2f} BPM | SDNN: {sdnn:.2f} ms | RMSSD: {rmssd:.2f} ms")
                        
                        # Send HR as LSL stream
                        hr_outlet.push_sample([hr])

                # Keep buffer small
                ecg_buffer = ecg_buffer[-fs:]  # Keep only last second of data

            except Exception as e:
                print(f"ECG Processing Error: {e}")

    time.sleep(0.01)  # Prevent CPU overload
 