import pylsl
import json
import logging
import csv
import os
import threading
import time
from datetime import datetime

class LSLSubscriber:
    def __init__(self, csv_path, stream_names=None):
        self.csv_path = csv_path
        self.stream_names = stream_names or ['EQ_ECG_Stream', 'EQ_HR_Stream', 'EQ_Accel_Stream', 
                                             'EQ_IR_Stream', 'EQ_RR_Stream', 'EQ_SkinTemp_Stream', 
                                             'EQ_GSR_Stream', 'Eye_Tracker_Stream', 'OvercookedStream', 
                                             'Emotiv_EEG', 'Emotiv_MET']
        self.inlets = {}
        self.resolved_streams = set()
        self.running = False
        self.collection_thread = None
        self.collection_lock = threading.Lock()

        self.setup_logging()
        self.csv_writer = None
        self.csv_file = None

    def setup_logging(self):
        log_dir = 'datalogs'
        os.makedirs(log_dir, exist_ok=True)
        log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M') + '.log'
        logging.basicConfig(filename=f'{log_dir}/{log_filename}', 
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def set_csv_path(self, csv_path):
        self.csv_path = csv_path

    def setup_csv(self):
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        self.csv_file = open(self.csv_path, mode='w', newline='')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=["stream", "timestamp", "data"])
        self.csv_writer.writeheader()

    def resolve_stream(self, name):
        try:
            streams = pylsl.resolve_byprop('name', name, timeout=2)
            if streams:
                with self.collection_lock:
                    self.inlets[name] = pylsl.StreamInlet(streams[0])
                    self.resolved_streams.add(name)
                    logging.info(f"Resolved stream {name}")
                    print(f"Resolved stream {name}")
            else:
                logging.warning(f"Could not resolve stream {name}")
                print(f"Could not resolve stream {name}")
        except Exception as e:
            logging.error(f"Error resolving stream {name}: {e}")

    def resolve_unresolved_streams(self):
        unresolved = [name for name in self.stream_names if name not in self.resolved_streams]
        for name in unresolved:
            self.resolve_stream(name)

    def start_collection(self):
        if not self.csv_writer:
            self.setup_csv()

        self.running = True
        self.collection_thread = threading.Thread(target=self.collect_data)
        self.collection_thread.start()

    # def stop_collection(self):
    #     self.running = False
    #     if self.collection_thread:
    #         self.collection_thread.join()
    #     if self.csv_file:
    #         self.csv_file.close()
    def stop_collection(self):
        self.running = False
        if self.collection_thread:
            self.collection_thread.join()
            self.collection_thread = None
        if self.csv_file and not self.csv_file.closed:
            try:
                self.csv_file.close()
            except Exception as e:
                logging.warning(f"Error closing CSV file: {e}")
        self.csv_writer = None


    # def collect_data(self):
    #     while self.running:
    #         with self.collection_lock:
    #             for name, inlet in self.inlets.items():
    #                 print(f"Collecting data from {name}...")
    #                 try:
    #                     sample, timestamp = inlet.pull_sample(timeout=0.0)
    #                     if sample:
    #                         print(f"Received sample from {name}: {sample}")
    #                         data_sample = json.loads(str(sample[0]))
    #                         row = {"stream": name, "timestamp": f"{timestamp:.6f}", "data": json.dumps(data_sample)}
    #                         print("row => " + str(row))
    #                         self.csv_writer.writerow(row)
    #                 except Exception as e:
    #                     logging.error(f"Error collecting data from {name}: {e}")
    #         time.sleep(0.001)
            
    def collect_data(self):
        try:
            while self.running:
                with self.collection_lock:
                    for name, inlet in self.inlets.items():
                        try:
                            sample, timestamp = inlet.pull_sample(timeout=0.0)
                            if sample:
                                data_sample = json.loads(str(sample[0]))
                                row = {
                                    "stream": name,
                                    "timestamp": f"{timestamp:.6f}",
                                    "data": json.dumps(data_sample)
                                }

                                if self.csv_writer and self.csv_file and not self.csv_file.closed:
                                    self.csv_writer.writerow(row)
                                else:
                                    logging.warning(f"Writer closed. Skipping row from {name}")
                        except Exception as e:
                            logging.error(f"Error collecting data from {name}: {e}")
                time.sleep(0.001)
        except Exception as e:
            logging.critical(f"Fatal error in data collection: {e}")

