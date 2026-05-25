import json
import boto3
from decimal import Decimal

# this file is the saved file in AWS, for the lambda function.
# it will not run locally.

def lambda_handler(event, context):

    print("Received event:")
    print(json.dumps(event))

    timestamp = event.get("timestamp", "unknown")
    temperature = float(event.get("temperature", 0))
    mpu = event.get("mpu", "na")
    rfid = event.get("rfid", "na")

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("truck_data")

    cloudwatch = boto3.client("cloudwatch")

    item = {
        "timestamp": timestamp,
        "temperature": Decimal(str(temperature)),
        "mpu": mpu,
        "rfid": rfid
    }

    response = table.put_item(Item=item)

    cloudwatch.put_metric_data(
        Namespace="TruckMonitoring",
        MetricData=[
            {
                "MetricName": "Temperature",
                "Value": temperature,
                "Unit": "None"
            }
        ]
    )

    return {
        "statusCode": 200,
        "body": "Success"
    }