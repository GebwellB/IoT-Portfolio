import serial
import time
import json
from datetime import datetime
import paho.mqtt.client as mqtt

client = mqtt.Client()

client.tls_set(
    ca_certs="AmazonRootCA1.pem",
    certfile="device-certificate.pem.crt",
    keyfile="private.pem.key"
)

client.connect("a3u3txwiv4fhou-ats.iot.us-east-1.amazonaws.com", 8883, 60)

client.loop_start()

aws_topic = "truck/truck_001/telemetry"

mpu_com_port = "COM10"
rfid_com_port = "COM7"
loops_to_run = 9999

mpu_detected = False
rfid_detected = False

try:
    mpu_com = serial.Serial(
        port=mpu_com_port,
        baudrate=9600,
        timeout=1
    )
    mpu_detected = True
    print("MPU connected")

except:
    print("MPU COM port not found")

try:
    rfid_com = serial.Serial(
        port=rfid_com_port,
        baudrate=9600,
        timeout=1
    )
    rfid_detected = True
    print("RFID connected")

except:
    print("RFID COM port not found")

current_temp = 48
temp_change = 0.5
heating = True

def get_temperature():
    global current_temp
    global heating

    if heating:
        current_temp += temp_change

        if current_temp >= 80:
            heating = False

    else:
        current_temp -= temp_change

        if current_temp <= 25:
            heating = True

    return round(current_temp, 2)


def get_mpu_reading():
    if not mpu_detected:
        return "na"

    if mpu_com.in_waiting > 0:
        try:
            return mpu_com.readline().decode("utf-8").rstrip()
        except:
            return "na"

    return "na"


def get_rfid_reading():
    if not rfid_detected:
        return "na"

    if rfid_com.in_waiting > 0:
        try:
            return rfid_com.readline().decode("utf-8").rstrip()
        except:
            return "na"

    return "na"


def build_payload(temp, mpu, rfid):
    payload = {
        "timestamp": datetime.now().isoformat(),
        "temperature": temp,
        "mpu": mpu,
        "rfid": rfid
    }

    return payload

try:

    print("Starting sensor loop...")

    for i in range(loops_to_run):

        # Read sensors
        temperature = get_temperature()
        mpu_value = get_mpu_reading()
        rfid_value = get_rfid_reading()

        # Build JSON object
        payload = build_payload(
            temperature,
            mpu_value,
            rfid_value
        )

        # Convert to JSON string
        json_payload = json.dumps(payload)

        # Print locally
        print(json_payload)

        # Send to AWS IoT / MQTT
        client.publish(
            aws_topic,
            json_payload
        )

        time.sleep(1)

finally:

    if mpu_detected:
        mpu_com.close()

    if rfid_detected:
        rfid_com.close()

    client.disconnect()