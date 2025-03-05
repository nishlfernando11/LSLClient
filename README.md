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
python subscriber.py
 