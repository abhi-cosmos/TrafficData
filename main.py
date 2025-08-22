import os
import gzip
import time
import logging
import datetime
from google.cloud import pubsub_v1
from fastapi import FastAPI, Query
from google.oauth2 import service_account
import json
import random
import base64

from random import randint
app = FastAPI(title="Lime Mini Project API", version="1.0")

credentials = service_account.Credentials.from_service_account_file("yourqm-d5aaf58e0a44.json")

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TOPIC = "opensky-stream"
INPUT = "sensor_obs2008.csv.gz"
SPEED_FACTOR = float("60")
PROJECT_ID = "yourqm"

publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC)


def publish_batch(events):
    for e in events:
        parts = e.decode("utf-8").strip().split(",")
        
        # Generate unique ID per event
        event_id = int(datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")) % (10 ** 18)
        
        
        record = {
            "event_id": event_id,
            "timestamp": parts[0],
            "sensor_id": randint(1000, 9999),
            "speed": float(parts[-1]),
            "location": f"POINT({float(parts[2])} {float(parts[1])})"
        }
        
        print(f"Publishing record: {record}")
        publisher.publish(topic_path, json.dumps(record).encode("utf-8"))



def get_timestamp(line):
    line = line.decode("utf-8")
    return datetime.datetime.strptime(line.split(",")[0], TIME_FORMAT)


@app.post("/simulate-traffic")
async def simulate(speed_factor: float = Query(60.0, description="Speed multiplier for replay")):
    program_start = datetime.datetime.utcnow()
    with gzip.open(INPUT, "rb") as f:
        header = f.readline()  # skip header
        first_obs_time = get_timestamp(f.readline())
        f.seek(0)
        f.readline()  # skip header again

        topublish = []
        for line in f:
            obs_time = get_timestamp(line)
            sim_time_elapsed = ((obs_time - first_obs_time).total_seconds()) / SPEED_FACTOR
            real_time_elapsed = (datetime.datetime.utcnow() - program_start).total_seconds()

            if sim_time_elapsed > real_time_elapsed + 1:
                publish_batch(topublish)
                topublish = []
                time.sleep(max(0, sim_time_elapsed - real_time_elapsed))
            
            topublish.append(line)

        publish_batch(topublish)
    
    return {"status": "Simulation completed"}


