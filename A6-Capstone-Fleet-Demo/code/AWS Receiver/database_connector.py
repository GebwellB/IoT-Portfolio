import boto3
import json
from decimal import Decimal

# CONFIG
TABLE_NAME = "truck_data"
OUTPUT_FILE = "dynamodb_export.json"
REGION = "us-east-1"


# Convert Decimal objects returned by DynamoDB
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Convert Decimal to int or float
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def scan_table(table):
    items = []

    response = table.scan()
    items.extend(response.get("Items", []))

    # Handle pagination
    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response.get("Items", []))

    return items


def main():
    dynamodb = boto3.resource(
        "dynamodb",
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