# LSL Python Client  

This is a simple Python client for receiving data from an **LSL (LabStreamingLayer) stream**. It listens to an available LSL data stream and prints or processes the received data in real-time.  

## How It Works  

1. The client **searches for an active LSL stream**.  
2. It **connects to the first available stream** matching the specified type (e.g., EEG, ECG).  
3. It **receives and prints incoming data** with timestamps.  

## Installation  

Install dependencies with:  

```bash
pip install pylsl
```

## Run  


```bash
python main.py
```

### LSL important details:

Stream datatype flags: https://github.com/labstreaminglayer/pylsl/blob/21fbbc30811fe151992654cdc5fa62a9a0f4d0be/pylsl/pylsl.py#L55-78

```
# Value formats supported by LSL. LSL data streams are sequences of samples,
# each of which is a same-size vector of values with one of the below types.

# For up to 24-bit precision measurements in the appropriate physical unit (
# e.g., microvolts). Integers from -16777216 to 16777216 are represented
# accurately.
cf_float32 = 1
# For universal numeric data as long as permitted by network and disk budget.
#  The largest representable integer is 53-bit.
cf_double64 = 2
# For variable-length ASCII strings or data blobs, such as video frames,
# complex event descriptions, etc.
cf_string = 3
# For high-rate digitized formats that require 32-bit precision. Depends
# critically on meta-data to represent meaningful units. Useful for
# application event codes or other coded data.
cf_int32 = 4
# For very high bandwidth signals or CD quality audio (for professional audio
#  float is recommended).
cf_int16 = 5
# For binary signals or other coded data.
cf_int8 = 6
# For now only for future compatibility. Support for this type is not
# available on all languages and platforms.
cf_int64 = 7
# Can not be transmitted.
cf_undefined = 0
```

Stream post processing Flags: https://github.com/labstreaminglayer/pylsl/blob/21fbbc30811fe151992654cdc5fa62a9a0f4d0be/pylsl/pylsl.py#L80-86
```

# Post processing flags
proc_none = 0  # No automatic post-processing; return the ground-truth time stamps for manual post-processing.
proc_clocksync = 1  # Perform automatic clock synchronization; equivalent to manually adding the time_correction().
proc_dejitter = 2  # Remove jitter from time stamps using a smoothing algorithm to the received time stamps.
proc_monotonize = 4  # Force the time-stamps to be monotonically ascending. Only makes sense if timestamps are dejittered.
proc_threadsafe = 8  # Post-processing is thread-safe (same inlet can be read from by multiple threads).
proc_ALL = proc_none | proc_clocksync | proc_dejitter | proc_monotonize | proc_threadsafe
```