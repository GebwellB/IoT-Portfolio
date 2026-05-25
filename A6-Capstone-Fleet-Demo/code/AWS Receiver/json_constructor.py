import paho.mqtt.client as mqtt
import json
import time
from data_collector import get_mpu_reading, get_rfid_reading, get_temperature, build_payload

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)

aws_topic = "iot/sensors"

payload = build_payload(get_mpu_reading(), get_rfid_reading(), get_temperature())
json_payload = json.dumps(payload)

print(payload)
print(json_payload)

client.publish(
    aws_topic,
    json_payload
)