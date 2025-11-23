import threading
import time
import json
import random
import os
from kafka import KafkaProducer, KafkaConsumer
from redis import Redis
from flask import Flask, jsonify

# CONFIG (We get these from docker-compose.yml)
# Note: 'kafka' and 'redis' are the hostnames defined in docker-compose
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
TOPIC = 'incidents'

app = Flask(__name__)
# Connect to Redis (The Database)
redis_client = Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# --- 1. THE PRODUCER (The Netskope Agent) ---
def generate_traffic():
    print("⏳ PRODUCER: Waiting for Kafka to boot...")
    time.sleep(15) # Give Kafka time to start up
    
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    print("🚀 PRODUCER: Connected! Starting traffic...")
    
    incident_id = 1000
    while True:
        # Simulate an incident
        incident = {
            "id": incident_id,
            "type": random.choice(["MALWARE", "DLP_LEAK", "PHISHING"]),
            "severity": random.choice(["High", "Critical"]),
            "timestamp": time.time()
        }
        
        # Send to Kafka (The Conveyor Belt)
        producer.send(TOPIC, json.dumps(incident).encode('utf-8'))
        print(f"➡️ SENT: Incident {incident_id}")
        
        incident_id += 1
        time.sleep(0.01) # <--- WE WILL CHANGE THIS LATER TO BREAK IT

# --- 2. THE CONSUMER (The Backend Processor) ---
def ingest_data():
    print("⏳ CONSUMER: Waiting for Kafka...")
    time.sleep(17) 
    
    # Connect to the "Conveyor Belt"
    consumer = KafkaConsumer(
        TOPIC, 
        bootstrap_servers=KAFKA_BROKER,
        group_id='ims-group' # This ID tracks what messages we've already read
    )
    
    print("✅ CONSUMER: Ready to process!")
    
    for msg in consumer:
        data = json.loads(msg.value.decode('utf-8'))

        # Simulate "Heavy Processing" (Database lookups, Logic, etc.)
        time.sleep(0.5) 
        # --------------------------
        
        # Pretend this takes work (Process the data)
        # Store in Redis
        redis_client.set(f"incident:{data['id']}", json.dumps(data))
        
        print(f"💾 SAVED to Redis: Incident {data['id']}")

# --- 3. THE DASHBOARD (API) ---
@app.route('/incidents')
def get_incidents():
    # Read everything from Redis
    keys = redis_client.keys("incident:*")
    results = [json.loads(redis_client.get(k)) for k in keys]
    return jsonify(results)

if __name__ == "__main__":
    # Run Producer in a background thread
    t1 = threading.Thread(target=generate_traffic)
    t1.start()
    
    # Run Consumer in a background thread
    t2 = threading.Thread(target=ingest_data)
    t2.start()
    
    # Run the Web Server (Main thread)
    app.run(host='0.0.0.0', port=5000)