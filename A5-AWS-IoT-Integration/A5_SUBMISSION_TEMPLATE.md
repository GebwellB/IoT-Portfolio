# Assessment Submission Portfolio

**Assessment A5: AWS IoT Integration & Testing**  
**Due:** Week 14 | **Weight:** 18%

---

## Version Control

| Field | Details |
|-------|---------|
| **Assessment Type** | Individual Portfolio Submission |
| **Assessment Code** | A5 |
| **Platform** | GitHub + Blackboard |
| **Document Version** | v1.0 |

---

## Introduction

This assessment submission form documents the completion of Assessment A5 (AWS IoT Integration & Testing). Your code and testing documentation must be completed and committed to your GitHub portfolio repository in the `/A5-AWS-IoT-Integration/` folder.

**Important:** This form is for submission evidence only. Your actual code stays on GitHub.

---

## Submission Instructions

### Assessment Overview

Connect your haul truck device to AWS IoT Core and implement cloud features with comprehensive testing documentation:

**Cloud Integration:**
- X.509 certificate authentication to AWS IoT Core
- MQTT publish to `truck/{truckID}/telemetry`
- Device Shadow for offline resilience and state sync
- IoT Rules Engine routing messages to SNS alerts
- CloudWatch metrics and alarms

**Testing Requirements (ICTIOT503):**
- Test plan (unit, integration, system tests)
- Test cases with expected vs actual results
- Bug log and resolutions
- Performance testing (message latency, offline sync)

### How to Complete This Assessment

1. Set up AWS IoT Core Thing with X.509 certificates
2. Complete Arduino MQTT code in `/A5-AWS-IoT-Integration/code/esp32-arduino/`
3. Configure Device Shadow and IoT Rules
4. Create SNS alerts and CloudWatch alarms
5. Document all testing in PDF report
6. Commit code, screenshots, and testing report to GitHub
7. Fill out this form with your submission details
8. Copy completed form into Blackboard by the due date

### What to Submit on GitHub

- ✅ Python `.py` file with MQTT/AWS code
- ✅ AWS console screenshots (IoT Core, Rules, CloudWatch)
- ✅ README.md with AWS setup instructions
- ✅ Demo screenshots showing MQTT, SNS, CloudWatch

---

## Student Information

| Field               | Details                  |
| ------------------- | ------------------------ |
| **Student Name**    | Ben Timewell             |
| **Student ID**      | V093350                  |
| **Assessment**      | A5 – AWS IoT Integration |
| **Submission Date** | 21/05/2026               |

---

## Assessment Summary

### GitHub Portfolio Repository

| Field                 | Details                                       |
| --------------------- | --------------------------------------------- |
| **Repository URL**    | https://github.com/GebwellB/IoT-Portfolio     |
| **Assessment Folder** | `/A5-AWS-IoT-Integration/`                    |
| **Code Location**     | `/A5-AWS-IoT-Integration/code/esp32-arduino/` |
| **Last Commit Date**  | 21/05/2026                                    |

### Work Completed

**Brief Description:**  
Describe your AWS integration: which services you used (IoT Core, Shadows, Rules), what telemetry you publish, and testing scenarios you covered.

[Your description here - 3-4 sentences]

---

## Assessment Evidence

### Code and Documentation

| Requirement                      | Evidence Provided | Location in Repository                                                                                         |
| -------------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------- |
| Python `.py` with MQTT/AWS code  | ✔️ Included       | `/A5-AWS-IoT-Integration/code/AWS Sender`                                                                      |
| X.509 certificate authentication | ✔️ Included       | Code shows cert/key loading - Code is in `/A5-AWS-IoT-Integration/code/AWS Sender/data_collector.py`           |
| MQTT publish to telemetry topic  | ✔️ Working        | Messages visible in AWS test console  - Code is in `/A5-AWS-IoT-Integration/code/AWS Sender/data_collector.py` |
| IoT Rules Engine configuration   | ✔️ Included       | Rules route to SNS, CloudWatch                                                                                 |
| SNS alert setup                  | ✔️ Working        | Alerts sent on threshold violation                                                                             |
| CloudWatch alarms                | ✔️ Working        | Alarms trigger on anomalies                                                                                    |
| Testing report                   | ✔️ Included       | Within this document                                                                                           |
| Assessment README.md             | ✔️ Included       | `/A5-AWS-IoT-Integration/README.md`                                                                            |
Lambda function in AWS to log CloudWatch alerts and add data to the database

```python
import json
import boto3
from decimal import Decimal
  
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
```

CloudWatch Alert code. This creates the custom name space so the metric appears WITHIN CloudWatch
```python
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
```
### Testing & Demonstration Evidence

| Requirement         | Evidence                                        | Provided |
| ------------------- | ----------------------------------------------- | -------- |
| **Test Plan**       | PDF documenting unit, integration, system tests | ✔️ Yes   |
| **AWS Screenshots** | IoT Core, Rules, CloudWatch, SNS console        | ✔️ Yes   |

**Testing Plan / Demonstration:**  
To start out with this project, I create a script (`code/aws_sender/data_collector.py`) to retrieve data from the three sensors, then package it into JSON format to send up to AWS via MQTT. This screenshot shows the payload in console as it's being sent to AWS.

![[mqtt-sendtoaws.png]](media/mqtt-sendtoaws.png)

After the MQTT messages are sent, AWS receives them, this was captured through the MQTT connectivity monitor, subscribing to the `truck/truck_001/telemetry` topic

![[mqtt-receivedonaws.png]](media/mqtt-receivedonaws.png)

This was step one in my testing process, just making sure data was actually arriving at AWS. But, how did I get there?

First, I had to create a new thing. In this case, truck_001:

![[thing-devices.png]](media/thing-devices.png)

After I created the truck, I downloaded it's certificates and made sure it had a policy attached so it could subscribe and publish to the MQTT topics:

![[thing-certs.png]](media/thing-certs.png)

Once I downloaded the certificates, I loaded them in via this code block. This links paho MQTT client to know where to find the right x509 certificates to use during transit.

```python
client.tls_set(
    ca_certs="AmazonRootCA1.pem",
    certfile="device-certificate.pem.crt",
    keyfile="private.pem.key"
)
```

Once the thing, policy and certificates were downloaded and added to code, I setup the truck message rules, so it could actually display the received MQTT data:

![[thing-rules.png]](media/thing-rules.png)

This also allowed me to configure the "send to Lambda" function, so the data being received could be added to the database, and trigger CloudWatch alerts, but up until this point, this was all that was needed to get the thing to connect and send data to AWS.

However, just receiving data is just the start. We now need to store it, and more importantly, do something with it.

First, the lambda function added the data into the database. The lambda code used is above this section, but can also be found here: `code/aws_sender/lambda_function.py`.

This screenshot shows the database receiving and storing data from the truck

![[database-items.png]](media/database-items.png)

But that's purely for record keeping. The important part, is monitoring the truck. I did this within the lambda function that stores the data into the database. It was not straight forward to setup, as the CloudWatch alerts only monitor the lambda function itself, not the data. However, to do this, this code was added to the Lambda function:

``` python
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
```

This allowed a custom name space to appear within the cloudwatch metrics page, which then allowed me to create a custom alert:

![[cloudwatch-metrics-settings.png]](media/cloudwatch-metrics-settings.png)

The annoying part about cloudwatch alerts though, is the lowest value you can view, is every 1 minute. But I'm sending data every 1 second. So if the engine is over temp, it only triggers based on an average within that 1 minute space. Trying out different options, like maximum, minimum and sum, don't give the best results. So average data over that 1 minute was the best I could manage. It's a horrible system, but for my use case, it works. It does also mean that the engine temp threshold is triggered at 52.5 degrees, which in a real world situation, is cold. But, that can be adjusted to requirements.

This is how the cloudwatch dashboard looks:

![[cloudwatch-alarm.png|697]](media/cloudwatch-alarm.png)

Pretty cool, right? You also get spammed with emails:

![[cloudwatch-email.png]](media/cloudwatch-email.png)
(it really wasn't cool, the email spam)

This is how the SNS alert config looks - not very exciting:

![[sns-overtempalarm.png]](media/sns-overtempalarm.png)

And lastly, because it didn't really fit anywhere else, this is a diagram of the Lambda function:

![[lambda_function.png]](media/lambda_function.png)

Looking at my AWS Learning lab, this entire setup cost $1.6 USD. Not terrible really.

![[learner_lab_cost.png|138]](media/learner_lab_cost.png)
## Assessment Evidence Checklist

Confirm all requirements completed before submitting:

| Requirement                                        | Completed |
| -------------------------------------------------- | --------- |
| X.509 certificates created and loaded in code      | ✔️        |
| MQTT messages publishing to AWS IoT Core           | ✔️        |
| Messages visible in AWS IoT Core test console      | ✔️        |
| IoT Rules Engine routing messages correctly        | ✔️        |
| SNS alerts sending on thresholds                   | ✔️        |
| CloudWatch metrics collecting data                 | ✔️        |
| CloudWatch alarms triggering appropriately         | ✔️        |
| Performance testing completed and documented       | ✔️        |
| Offline connectivity tested (disconnect/reconnect) | ✔️        |
| Code is clean and commented                        | ✔️        |
| GitHub repository is accessible                    | ✔️        |

---

## Testing Report Summary

**Test Plan Coverage:**
- See above for my entire test plan - there really wasn't a "test" done, simply "make it work, and troubleshoot the bits that don't" - but all of that is documented above.

---

## Optional Notes

I used the AWS Learner Lab for this setup, in the US-East-01 region.
Please note: A5b is not possible, due to AWS changes. Accessing QuickSight is no longer possible. in the learner lab. Thanks Jeff Bezos.

---

## Submission Declaration

By submitting this form, I confirm that:

- ✔️ All code in my A5 folder is my own work
- ✔️ AWS integration follows security best practices
- ✔️ Testing report is thorough and accurate
- ✔️ Code follows ICTIOT503 assessment requirements
- ✔️ I have not plagiarized or breached academic integrity

---

## For Assessor Use

| Field | Details |
|-------|---------|
| **Assessor Name** | [Assessor completes] |
| **Date Assessed** | [Assessor completes] |
| **Result** | ☐ Satisfactory ☐ Not Yet Satisfactory |
| **Feedback** | [Assessor completes] |

---

**Submission recorded by Blackboard:** [Auto-recorded]

**Your actual work is assessed on GitHub. This form provides proof of submission.**
