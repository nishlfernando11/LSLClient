from pylsl import StreamInlet, resolve_byprop, proc_ALL
import time
import pylsl
import json

# Resolve the ECG stream (name should match the stream name in your publisher)
ecg_streams = resolve_byprop('name', 'EQ_ECG_Stream')  

# Resolve the HR stream (name should match the stream name in your publisher)
hr_streams = resolve_byprop('name', 'EQ_HR_Stream')  

rr_streams = resolve_byprop('name', 'EQ_RR_Stream')  
ir_streams = resolve_byprop('name', 'EQ_IR_Stream')  
skinTemp_streams = resolve_byprop('name', 'EQ_SkinTemp_Stream')  
accel_streams = resolve_byprop('name', 'EQ_Accel_Stream')  
gsr_streams = resolve_byprop('name', 'EQ_GSR_Stream')  

# Create inlets to receive the streams
ecg_inlet = StreamInlet(ecg_streams[0])
hr_inlet = StreamInlet(hr_streams[0])
rr_inlet = StreamInlet(rr_streams[0])
ir_inlet = StreamInlet(ir_streams[0])
skinTemp_inlet = StreamInlet(skinTemp_streams[0])
accel_inlet = StreamInlet(accel_streams[0])
gsr_inlet = StreamInlet(gsr_streams[0])

# ecg_inlet.set_postprocessing(proc_ALL)
# hr_inlet.set_postprocessing(proc_ALL)
# rr_inlet.set_postprocessing(proc_ALL)
# ir_inlet.set_postprocessing(proc_ALL)
# skinTemp_inlet.set_postprocessing(proc_ALL)
# accel_inlet.set_postprocessing(proc_ALL)
# gsr_inlet.set_postprocessing(proc_ALL)

# Get current Unix timestamp to align LSL timestamps
lsl_start_time = pylsl.local_clock()  # LSL time reference
unix_start_time = time.time()  # System Unix time reference
print("lsl_start_time ", lsl_start_time)
print("unix_start_time ", unix_start_time)

lsl_to_unix_offset = unix_start_time - lsl_start_time  # Calculate offset
print(f"LSL to Unix Time Offset: {lsl_to_unix_offset:.6f} seconds")


ecg_offset = ecg_inlet.time_correction()
hr_offset = hr_inlet.time_correction()
rr_offset = rr_inlet.time_correction()
ir_offset = ir_inlet.time_correction()
accel_offset = accel_inlet.time_correction()
skinTemp_offset = skinTemp_inlet.time_correction()
gsr_offset = gsr_inlet.time_correction()
# Retrieve stream metadata
info = ecg_inlet.info()

print("\n--- Stream ECG Metadata ---")
print(f"Name: {info.name()}")
print(f"Type: {info.type()}")
print(f"Channel Count: {info.channel_count()}")
print(f"Sampling Rate: {info.nominal_srate()}")
print(f"Channel Format: {info.channel_format()}")

print("\nListening for data...")
 
info = hr_inlet.info()

print("\n--- Stream HR Metadata ---")
print(f"Name: {info.name()}")
print(f"Type: {info.type()}")
print(f"Channel Count: {info.channel_count()}")
print(f"Sampling Rate: {info.nominal_srate()}")
print(f"Channel Format: {info.channel_format()}")

print("\nListening for data...")


import logging
from datetime import datetime

# Get current date and time in the format YYYY-MM-DD_HH-MM-SS
log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M') + '.log'

# Configure logging
logging.basicConfig(filename=f'datalogs/{log_filename}', 
                    level=logging.DEBUG,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Example logging statements
logging.debug('This is a debug message')


def fix_timestamp(timestamp):
    if timestamp is None:
        return None
    unix_timestamp = unix_start_time + (timestamp - lsl_start_time)
    return unix_timestamp


while True:
    # Fetch ECG sample (array of 2 values: Lead 1, Lead 2)
    ecg_sample, ecg_timestamp = ecg_inlet.pull_sample(timeout=0.0)
    if ecg_sample:
        # 3Deserialize JSON String to Python Dictionary
        sample = str(ecg_sample[0]) 
        ecg_sample = json.loads(sample)
        print("ecg_sample ", ecg_sample)

         # Adjust LSL timestamp to match Unix time
        print("ecg_timestamp.", ecg_timestamp)
        print(f"Received Data at {fix_timestamp(ecg_timestamp):.6f} (Unix Time)")
        cor_ecg_timestamp = ecg_timestamp + ecg_offset
        print(f"ECG Data: {ecg_sample}")
        print(f"ECG timestamp: {cor_ecg_timestamp}")
        logging.debug(f"ECG {cor_ecg_timestamp}, {ecg_sample}")

        # print(f"ECG Data: Lead 1 = {ecg_sample[0]} mV, Lead 2 = {ecg_sample[1]} mV")
    
    # Fetch HR sample (array with 1 value: HR in BPM)
    hr_sample, hr_timestamp = hr_inlet.pull_sample(timeout=0.0)
    if hr_sample:
        # 3Deserialize JSON String to Python Dictionary
        sample = str(hr_sample[0]) 
        hr_sample = json.loads(sample)
        print("hr_sample ", hr_sample)

        cor_hr_timestamp = hr_timestamp + hr_offset
        print(f"\n\n---Heart Rate: {hr_sample} BPM")
        print(f"---Heart timestamp: {cor_hr_timestamp}")
        logging.debug(f"HR {cor_hr_timestamp}, {hr_sample}")

    # Fetch Accelerometer sample
    accel_sample, accel_timestamp = accel_inlet.pull_sample(timeout=0.0)
    if accel_sample:
        # 3Deserialize JSON String to Python Dictionary
        sample = str(accel_sample[0]) 
        accel_sample = json.loads(sample)
        print("accel_sample ", accel_sample)

        print(f"Received Data at {fix_timestamp(accel_timestamp):.6f} (Unix Time)")

        cor_accel_timestamp = accel_timestamp + accel_offset
        print(f"\n\n---Accelerometer: {accel_sample}")
        print(f"---Accelerometer timestamp: {cor_accel_timestamp}")
        logging.debug(f"Accelerometer {cor_accel_timestamp}, {accel_sample}")
        logging.debug(f"Accelerometer timestamp {accel_timestamp}, offset {accel_offset}")

    # Fetch Impedence rate sample
    ir_sample, ir_timestamp = ir_inlet.pull_sample(timeout=0.0)
    if ir_sample:
        # 3Deserialize JSON String to Python Dictionary
        sample = str(ir_sample[0]) 
        ir_sample = json.loads(sample)
        print("ir_sample ", ir_sample)

        cor_ir_timestamp = ir_timestamp + ir_offset
        print(f"\n\n---Impedence  Rate: {ir_sample}")
        print(f"---Impedence rate timestamp: {cor_ir_timestamp}")
        logging.debug(f"Impedence rate {cor_ir_timestamp}, {ir_sample}")

    # Fetch RR sample
    rr_sample, rr_timestamp = rr_inlet.pull_sample(timeout=0.0)
    if rr_sample:
        # 3Deserialize JSON String to Python Dictionary
        sample = str(rr_sample[0]) 
        rr_sample = json.loads(sample)
        print("rr_sample ", rr_sample)

        cor_rr_timestamp = rr_timestamp + rr_offset
        print(f"\n\n---RR Rate: {rr_sample}")
        print(f"---RR timestamp: {cor_rr_timestamp}")
        logging.debug(f"RR {cor_rr_timestamp}, {rr_sample}")

    # Fetch SkinTemp sample
    skinTemp_sample,skinTemp_timestamp = skinTemp_inlet.pull_sample(timeout=0.0)
    if skinTemp_sample:
        # 3Deserialize JSON String to Python Dictionary
        sample = str(skinTemp_sample[0]) 
        skinTemp_sample = json.loads(sample)
        print("skinTemp_sample ", skinTemp_sample)

        cor_skinTemp_timestamp = skinTemp_timestamp + skinTemp_offset
        print(f"\n\n---skinTemp: {skinTemp_sample}")
        print(f"---skinTemp timestamp: {cor_skinTemp_timestamp}")
        logging.debug(f"skinTemp {cor_skinTemp_timestamp}, {skinTemp_sample}")
    
    # Fetch GSR sample
    gsr_sample, gsr_timestamp = gsr_inlet.pull_sample(timeout=0.0)
    if gsr_sample:
        # 3Deserialize JSON String to Python Dictionary
        sample = str(gsr_sample[0]) 
        gsr_sample = json.loads(sample)
        print("gsr_sample ", gsr_sample)

        cor_gsr_timestamp = gsr_timestamp + gsr_offset
        print(f"\n\n---GSR Rate: {gsr_sample}")
        print(f"---GSR timestamp: {cor_gsr_timestamp}")
        logging.debug(f"GSR {cor_gsr_timestamp}, {gsr_sample}")
    # Sleep for a bit (simulate processing)
    time.sleep(0.001)  # Adjust as need

