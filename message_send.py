import os
import base64
import json
import time
from paho.mqtt import client as mqtt_client

broker_address = "broker.hivemq.com"
port = 1883
topic = "folder_topic"

def connect_mqtt():
    client = mqtt_client.Client("RaspberryPi")
    client.connect(broker_address, port)
    return client

def serialize_folder(folder_path):
    serialized_folder = {}
    for root, dirs, files in os.walk(folder_path):
        serialized_files = {}
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                file_content = base64.b64encode(f.read()).decode()
            serialized_files[file] = file_content
        serialized_folder[root] = serialized_files
    return json.dumps(serialized_folder)

def publish_folder(client, folder_path):
    serialized_folder = serialize_folder(folder_path)
    client.publish(topic, serialized_folder)

def main():
    client = connect_mqtt()
    client.loop_start()
    while True:
        folder_path = "present"  # Path to your folder
        publish_folder(client, folder_path)
        time.sleep(300)  # Sleep for 5 minutes

if __name__ == "__main__":
    main()
