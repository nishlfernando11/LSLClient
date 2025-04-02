from pylsl import StreamInlet, resolve_byprop, proc_ALL
import time
import pylsl
import json
import logging
import csv
import os
from datetime import datetime

# === Logging Setup ===
log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M') + '.log'
logging.basicConfig(filename=f'datalogs/{log_filename}', 
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# === CSV Setup ===
csv_dir = 'csvlogs'
os.makedirs(csv_dir, exist_ok=True)

unified_csv_path = f'{csv_dir}/all_streams_{log_filename}.csv'
unified_csv_file = open(unified_csv_path, mode='w', newline='')
unified_writer = csv.DictWriter(unified_csv_file, fieldnames=["stream", "timestamp", "data"])
unified_writer.writeheader()

stream_names = ['ECG', 'HR', 'Accel', 'IR', 'RR', 'SkinTemp', 'GSR', 'Eye', 'Overcooked']
csv_files = {}
csv_writers = {}

streams = pylsl.resolve_streams()
print(f"Found {len(streams)} streams!")

for name in stream_names:
    path = f'{csv_dir}/{name.lower()}_{log_filename}.csv'
    f = open(path, mode='w', newline='')
    writer = csv.DictWriter(f, fieldnames=["timestamp", "data"])
    writer.writeheader()
    csv_files[name] = f
    csv_writers[name] = writer

def save_to_csv(stream_name, timestamp, data_dict):
    try:
        row = {"timestamp": f"{timestamp:.6f}", "data": json.dumps(data_dict)}
        if stream_name in csv_writers:
            csv_writers[stream_name].writerow(row)
        unified_writer.writerow({"stream": stream_name, "timestamp": f"{timestamp:.6f}", "data": json.dumps(data_dict)})
    except Exception as e:
        logging.error(f"CSV write error for {stream_name}: {e}")

def print_data(data_sample, data_timestamp, data_offset, type):
    sample = str(data_sample[0])
    data_sample = json.loads(sample)
    cor_data_timestamp = data_timestamp + data_offset
    print(f"{type}_sample ", data_sample)
    print(f"---{type} timestamp: {cor_data_timestamp}")
    logging.debug(f"{type} {cor_data_timestamp}, {data_sample}")
    save_to_csv(type, cor_data_timestamp, data_sample)

def safe_resolve(name):
    streams = resolve_byprop('name', name)
    return StreamInlet(streams[0]) if streams else None

eye_inlet = safe_resolve('Eye_Tracker_Stream')
ecg_inlet = safe_resolve('EQ_ECG_Stream')
hr_inlet = safe_resolve('EQ_HR_Stream')
rr_inlet = safe_resolve('EQ_RR_Stream')
ir_inlet = safe_resolve('EQ_IR_Stream')
skinTemp_inlet = safe_resolve('EQ_SkinTemp_Stream')
accel_inlet = safe_resolve('EQ_Accel_Stream')
gsr_inlet = safe_resolve('EQ_GSR_Stream')
oc_inlet = safe_resolve('OvercookedStream')

lsl_start_time = pylsl.local_clock()
unix_start_time = time.time()
lsl_to_unix_offset = unix_start_time - lsl_start_time

def safe_time_correction(inlet, name):
    if inlet:
        return inlet.time_correction()
    print(f"Warning: {name} stream not available.")
    return 0.0

ecg_offset = safe_time_correction(ecg_inlet, "ECG")
hr_offset = safe_time_correction(hr_inlet, "HR")
rr_offset = safe_time_correction(rr_inlet, "RR")
ir_offset = safe_time_correction(ir_inlet, "IR")
accel_offset = safe_time_correction(accel_inlet, "Accel")
skinTemp_offset = safe_time_correction(skinTemp_inlet, "SkinTemp")
gsr_offset = safe_time_correction(gsr_inlet, "GSR")
eye_offset = safe_time_correction(eye_inlet, "Eye Tracker")
oc_offset = safe_time_correction(oc_inlet, "Overcooked")

def fix_timestamp(timestamp):
    if timestamp is None:
        return None
    return unix_start_time + (timestamp - lsl_start_time)

try:
    while True:
        ecg_sample, ecg_timestamp = ecg_inlet.pull_sample(timeout=0.0)
        if ecg_sample:
            sample = str(ecg_sample[0])
            ecg_sample = json.loads(sample)
            cor_ecg_timestamp = ecg_timestamp + ecg_offset
            logging.debug(f"ECG {cor_ecg_timestamp}, {ecg_sample}")
            save_to_csv("ECG", cor_ecg_timestamp, ecg_sample)

        hr_sample, hr_timestamp = hr_inlet.pull_sample(timeout=0.0)
        if hr_sample:
            sample = str(hr_sample[0])
            hr_sample = json.loads(sample)
            cor_hr_timestamp = hr_timestamp + hr_offset
            logging.debug(f"HR {cor_hr_timestamp}, {hr_sample}")
            save_to_csv("HR", cor_hr_timestamp, hr_sample)

        accel_sample, accel_timestamp = accel_inlet.pull_sample(timeout=0.0)
        if accel_sample:
            sample = str(accel_sample[0])
            accel_sample = json.loads(sample)
            cor_accel_timestamp = accel_timestamp + accel_offset
            logging.debug(f"Accel {cor_accel_timestamp}, {accel_sample}")
            save_to_csv("Accel", cor_accel_timestamp, accel_sample)

        ir_sample, ir_timestamp = ir_inlet.pull_sample(timeout=0.0)
        if ir_sample:
            sample = str(ir_sample[0])
            ir_sample = json.loads(sample)
            cor_ir_timestamp = ir_timestamp + ir_offset
            logging.debug(f"IR {cor_ir_timestamp}, {ir_sample}")
            save_to_csv("IR", cor_ir_timestamp, ir_sample)

        rr_sample, rr_timestamp = rr_inlet.pull_sample(timeout=0.0)
        if rr_sample:
            sample = str(rr_sample[0])
            rr_sample = json.loads(sample)
            cor_rr_timestamp = rr_timestamp + rr_offset
            logging.debug(f"RR {cor_rr_timestamp}, {rr_sample}")
            save_to_csv("RR", cor_rr_timestamp, rr_sample)

        skinTemp_sample, skinTemp_timestamp = skinTemp_inlet.pull_sample(timeout=0.0)
        if skinTemp_sample:
            sample = str(skinTemp_sample[0])
            skinTemp_sample = json.loads(sample)
            cor_skinTemp_timestamp = skinTemp_timestamp + skinTemp_offset
            logging.debug(f"SkinTemp {cor_skinTemp_timestamp}, {skinTemp_sample}")
            save_to_csv("SkinTemp", cor_skinTemp_timestamp, skinTemp_sample)

        gsr_sample, gsr_timestamp = gsr_inlet.pull_sample(timeout=0.0)
        if gsr_sample:
            sample = str(gsr_sample[0])
            gsr_sample = json.loads(sample)
            cor_gsr_timestamp = gsr_timestamp + gsr_offset
            logging.debug(f"GSR {cor_gsr_timestamp}, {gsr_sample}")
            save_to_csv("GSR", cor_gsr_timestamp, gsr_sample)

        eye_sample, eye_timestamp = eye_inlet.pull_sample(timeout=0.0)
        if eye_sample:
            print_data(eye_sample, eye_timestamp, eye_offset, "Eye")

        oc_sample, oc_timestamp = oc_inlet.pull_sample(timeout=0.0)
        if oc_sample:
            print_data(oc_sample, oc_timestamp, oc_offset, "Overcooked")

        time.sleep(0.001)

except KeyboardInterrupt:
    print("Shutting down...")
    for f in csv_files.values():
        f.close()
    unified_csv_file.close()
    print("Files closed.")