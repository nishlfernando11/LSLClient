# import time
# import pylsl
# from pylsl import StreamInlet, resolve_byprop, proc_ALL
# import json
# import pandas as pd
# from datetime import datetime
# import re
# import socketio
# import threading
# from collections import deque
# import argparse
# from dotenv import load_dotenv
# import os
# load_dotenv(dotenv_path="./.env")

# # from subscriber import on_start_ecg, on_stop_ecg

# # Load API key from env var (preferred)
# SERVER_IP = os.getenv("SERVER_IP")
# PORT = os.getenv("PORT")


# sio = socketio.Client()

def print_green(msg): print(f"\033[32m{msg}\033[0m")
def print_yellow(msg): print(f"\033[33m{msg}\033[0m")
def print_red(msg): print(f"\033[31m{msg}\033[0m")
def print_cyan(msg): print(f"\033[36m{msg}\033[0m")


# @sio.event
# def connect():
#     print("Connected to server")
#     # Start emitting after connection is confirmed
#     # i = 0
#     # while True:
#     #     explanation = f"test reason longer one two three four five nine ten words {i}"
#     #     sio.emit("adax", {"explanation": explanation})
#     #     print("Emitted:", explanation)
#     #     i += 1
#     #     time.sleep(1)

    
# @sio.on('start_ecg')
# def handle_start(data):
#     print_green("Start ecg data "+ json.dumps(data))
#     on_start_ecg(data)

# @sio.on('stop_ecg')
# def handle_stop():
#     print_green("Ending data collection ")
#     # print_green("Ending data collection "+ json.dumps(data))
#     on_stop_ecg()


# @sio.event
# def disconnect():
#     print("Disconnected from server")
    
    
# if __name__ == '__main__':
#     try:
#         # connect to the socket server
#         sio.connect(f'http://{SERVER_IP}:{PORT}')
#         # sio.wait()
    
#     except Exception as e:
#         print("Connection failed:", e)

#     while True:
#         time.sleep(1)  # Keep main thread alive
        
        
#==================#
import socketio
import threading
import time
import json
import os
from datetime import datetime
from LSLSubscriber import LSLSubscriber

from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="./.env")


SERVER_IP = os.getenv("SERVER_IP")
PORT = os.getenv("PORT")



sio = socketio.Client()

subscriber = None
resolution_event = threading.Event()
socket_connected = threading.Event()


stream_names = ['EQ_ECG_Stream', 'EQ_HR_Stream', 'EQ_Accel_Stream',
                'EQ_IR_Stream', 'EQ_RR_Stream', 'EQ_SkinTemp_Stream',
                'EQ_GSR_Stream', 'Eye_Tracker_Stream', 'OvercookedStream',
                'Emotiv_EEG', 'Emotiv_MET']

# Background thread to retry socket connection
def retry_socket_connection():
    while not socket_connected.is_set():
        try:
            sio.connect(f'http://{SERVER_IP}:{PORT}')
            socket_connected.set()
            print_green("Socket connection established.")
        except Exception as e:
            print(f"Socket connection failed, retrying: {e}")
            time.sleep(5)


# Background thread to resolve streams continuously
def resolve_streams_continuously():
    global subscriber
    while not resolution_event.is_set():
        subscriber.resolve_unresolved_streams()
        time.sleep(5)


@sio.event
def connect():
    print_green("Connected to server")


@sio.event
def disconnect():
    print("Disconnected from server")
    socket_connected.clear()
    threading.Thread(target=retry_socket_connection).start()


@sio.on('start_ecg')
def handle_start(data):
    global subscriber
    print(data)
    start_info = data.get('start_info', {})
    player_id = start_info.get('player_id', 'unknown')
    round_id = start_info.get('round_id', 'unknown')
    uid = start_info.get('uid', 'unknown')

    timestamp_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    folder_path = os.path.join('csvlogs', f'{uid}_{player_id}', str(round_id))
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{timestamp_str}__uid{uid}_round{round_id}.csv"
    csv_path = os.path.join(folder_path, filename)

    print_green(f"Starting data collection: {csv_path}")

    subscriber.set_csv_path(csv_path)
    subscriber.start_collection()


@sio.on('stop_ecg')
def handle_stop(data):
    global subscriber

    print_green("Stopping data collection")
    if subscriber:
        subscriber.stop_collection()


if __name__ == '__main__':
    subscriber = LSLSubscriber(csv_path='temp.csv', stream_names=stream_names)

    resolution_event.clear()
    threading.Thread(target=resolve_streams_continuously, daemon=True).start()

    socket_connected.clear()
    threading.Thread(target=retry_socket_connection).start()

    try:
        sio.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        resolution_event.set()
        # resolution_thread.join()
        if subscriber:
            subscriber.stop_collection()
