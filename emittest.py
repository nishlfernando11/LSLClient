

from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="./.env")

# Load API key from env var (preferred)
SERVER_IP = os.getenv("SERVER_IP")
PORT = os.getenv("PORT")

import socketio
import time
import json

def print_green(msg): print(f"\033[32m{msg}\033[0m")
def print_yellow(msg): print(f"\033[33m{msg}\033[0m")
def print_red(msg): print(f"\033[31m{msg}\033[0m")
def print_cyan(msg): print(f"\033[36m{msg}\033[0m")


sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to server")
    # Start emitting after connection is confirmed
    i = 0
    while True:
        explanation = f"test reason {i}"
        sio.emit("xai_message", {"explanation": explanation})
        print("Emitted:", explanation)
        i += 1
        time.sleep(5)


@sio.event
def connect():
    print("Connected to server")
    # Start emitting after connection is confirmed
    # i = 0
    # while True:
    #     explanation = f"test reason longer one two three four five nine ten words {i}"
    #     sio.emit("xai_message", {"explanation": explanation})
    #     print("Emitted:", explanation)
    #     i += 1
    #     time.sleep(1)

running=False
@sio.on('start_ecg')
def on_start_ecg(data):
    global xai_agent_type, running
    running=True
    print_green("Starting data collection: "+str(running))
    start_info = data.get('start_info', {})
    print_green("Start ecg data "+ json.dumps(data))
    if start_info["xaiAgentType"] == "AdaX":
        xai_agent_type = 'AdaX'
        i = 0
        while running:
            explanation = f"test reason adapted {i}"
            sio.emit("xai_message", {"explanation": explanation})
            print("Emitted:", explanation)
            i += 1
            time.sleep(5)
    elif start_info["xaiAgentType"] == "StaticX":
        xai_agent_type = 'StaticX'
        i = 0
        while running:
            explanation = f"test reason static {i}"
            sio.emit("xai_message", {"explanation": explanation})
            print("Emitted:", explanation)
            i += 1
            time.sleep(5)
    else:
        xai_agent_type = 'NoX'
    
    print_green(f"{xai_agent_type} agent type detected")
    # eeg_inlet = safe_resolve('Emotiv_EEG')
    # print("eeg_inlet", eeg_inlet)
    # buffer_eeg_data(eeg_inlet)
    
@sio.on('stop_ecg')
def on_end_ecg(data):
    global running
    running=False
    print_green("Ending data collection ")
    # print_green("Ending data collection "+ json.dumps(data))
    

@sio.event
def disconnect():
    print("Disconnected from server")
    
@sio.event
def disconnect():
    print("❌ Disconnected from server")
    

if __name__ == '__main__':
    try:
        sio.connect(f'http://{SERVER_IP}:{PORT}')
        sio.wait()
    except Exception as e:
        print("Connection failed:", e)




