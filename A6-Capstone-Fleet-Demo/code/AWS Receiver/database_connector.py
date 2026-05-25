import boto3
import json
from decimal import Decimal

# AWS credentials
AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_KEY"

# Optional if using temporary credentials
AWS_SESSION_TOKEN = None

REGION = "us-east-1"

TABLE_NAME = "truck_data"
OUTPUT_FILE = "dynamodb_export.json"


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return super().default(obj)


def scan_table(table):
    items = []

    response = table.scan()
    items.extend(response.get("Items", []))

    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response.get("Items", []))

    return items


def main():
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        region_name=REGION
    )

    table = dynamodb.Table(TABLE_NAME)

    print(f"Scanning table: {TABLE_NAME}")

    items = scan_table(table)

    print(f"Retrieved {len(items)} items")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(items, f, cls=DecimalEncoder, indent=2)

    print(f"Exported to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()