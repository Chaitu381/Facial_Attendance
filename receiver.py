import os
import base64
import json
from paho.mqtt import client as mqtt_client

broker_address = "broker.hivemq.com"
port = 1883
topic = "folder_topic"

def connect_mqtt():
    client = mqtt_client.Client("Laptop")
    client.connect(broker_address, port)
    return client

def deserialize_folder(serialized_folder):
    deserialized_folder = json.loads(serialized_folder)
    for root, files in deserialized_folder.items():
        os.makedirs(root, exist_ok=True)
        for filename, content in files.items():
            file_path = os.path.join(root, filename)
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(content))

def on_message(client, userdata, message):
    serialized_folder = message.payload.decode()
    deserialize_folder(serialized_folder)
    print("Folder received and saved.")

def main():
    client = connect_mqtt()
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()

if __name__ == "__main__":
    main()
