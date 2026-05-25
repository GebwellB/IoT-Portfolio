import json
import boto3
from decimal import Decimal
from botocore.exceptions import ClientError

# CONFIG
TABLE_NAME = "truck_data"
BUCKET_NAME = "databasedump-4821751"
EXPORT_FILE_KEY = "exports/truck_data_export.json"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

s3 = boto3.client("s3")
cloudwatch = boto3.client("cloudwatch")


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return super().default(obj)


def file_exists_in_s3(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        raise


def scan_table():
    items = []

    response = table.scan()
    items.extend(response.get("Items", []))

    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response.get("Items", []))

    return items


def export_dynamodb_to_s3():

    # Check if export file already exists
    if file_exists_in_s3(BUCKET_NAME, EXPORT_FILE_KEY):
        print("Export file already exists. Skipping export.")
        return

    print("Export file not found. Creating export...")

    items = scan_table()

    json_data = json.dumps(
        items,
        cls=DecimalEncoder,
        indent=2
    )

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=EXPORT_FILE_KEY,
        Body=json_data,
        ContentType="application/json"
    )

    print(f"Export uploaded to s3://{BUCKET_NAME}/{EXPORT_FILE_KEY}")


def lambda_handler(event, context):

    print("Received event:")
    print(json.dumps(event))

    timestamp = event.get("timestamp", "unknown")
    temperature = float(event.get("temperature", 0))
    mpu = event.get("mpu", "na")
    rfid = event.get("rfid", "na")

    item = {
        "timestamp": timestamp,
        "temperature": Decimal(str(temperature)),
        "mpu": mpu,
        "rfid": rfid
    }

    # Insert into DynamoDB
    response = table.put_item(Item=item)

    # Send CloudWatch metric
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

    # Export database only if file doesn't exist
    export_dynamodb_to_s3()

    return {
        "statusCode": 200,
        "body": "Success"
    }