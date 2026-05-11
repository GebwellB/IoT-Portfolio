import serial
import time
import json
import paho.mqtt.client as mqtt

client = mqtt.Client()

client.connect("broker.hivemq.com", 1883, 60)

mpu_com_port = "COM10"
rfid_com_port = "COM7"

temperature_topic = "sensors/temperature"
mpu_topic = "sensors/mpu"
rfid_topic = "sensors/rfid"

print_data = True
mpu_detected = False
rfid_detected = False

try:
    mpu_com = serial.Serial(
        port=mpu_com_port,      
        baudrate=9600,    
        timeout=1)
    mpu_detected = True
except:
    print("MPU COM port not found. Check COM port")

try:
    rfid_com = serial.Serial(
        port=rfid_com_port,      
        baudrate=9600,    
        timeout=1)
    rfid_detected = True
except:
    print("RFID COM port not found. Check COM port")

temperature_data = []

starting_temp = 18
heating = True
for i in range(1000):
    if heating:
        starting_temp += 0.5
        if starting_temp >= 80:
            heating = False
    else:
        starting_temp -= 0.5
        if starting_temp <= 25:
            heating = True
    temperature_data.append(starting_temp)

mpu_data = []
rfid_data = []

try:
    print("Starting serial communication...")
    loop_count = 1
    for i in range(60):
        if mpu_detected:
            if mpu_com.in_waiting > 0:
                line = mpu_com.readline().decode('utf-8').rstrip()
                print(f"Received from MPU: {line}")
                mpu_data.append(line)
        if rfid_detected:
            if rfid_com.in_waiting > 0:
                line = rfid_com.readline().decode('utf-8').rstrip()
                print(f"Received from RFID: {line}")
                rfid_data.append(line)
        time.sleep(0.2)
        print(f"Loop count: {loop_count}")
        loop_count += 1
except KeyboardInterrupt:
    print("Closing connection...")
finally:
    if mpu_detected:
        mpu_com.close()
    if rfid_detected:
        rfid_com.close()

if(print_data):
    for i in range(len(temperature_data)):
        print(temperature_data[i])
    if mpu_detected:
        for i in range(len(mpu_data)):
            print(mpu_data[i])

    if rfid_detected:
        for i in range(len(rfid_data)):
            print(rfid_data[i])

client.publish(
    temperature_topic,
    json.dumps(temperature_data)
)

client.publish(
    mpu_topic,
    json.dumps(mpu_data)
)

client.publish(
    rfid_topic,
    json.dumps(rfid_data)
)

client.disconnect()