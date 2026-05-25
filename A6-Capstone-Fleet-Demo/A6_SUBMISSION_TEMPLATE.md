# Assessment Submission Portfolio

**Assessment A6: Capstone Fleet System**  
**Due:** Week 18 | **Weight:** 30%

---
## Version Control

| Field | Details |
|-------|---------|
| **Assessment Type** | Individual Portfolio Submission |
| **Assessment Code** | A6 |
| **Platform** | GitHub + Blackboard |
| **Document Version** | v1.0 |

---

## Introduction

This assessment submission form documents the completion of Assessment A6 (Capstone Fleet System). This is the final, comprehensive assessment integrating all course concepts: IoT hardware, AWS cloud services, analytics, and testing.

**Important:** This form is for submission evidence only. Your actual work stays on GitHub.

---

## Submission Instructions

### Assessment Overview

Demonstrate a complete IoT solution for a haul truck fleet monitoring system in a mining pit. Your system integrates:

**Hardware & Sensors:**
- Real ESP32 haul truck device with all A1-A5 sensors
- Continuous MQTT telemetry to AWS IoT Core
- Functional sensors: DHT11, GY-521, MPU

**AWS Cloud Integration:**
- IoT Core (Things, certificates, MQTT topics)
- IoT Rules Engine (routing to DynamoDB, SNS, Lambda)
- DynamoDB (time-series storage)
- SNS (alert notifications)

**Analytics & Visualization:**
- Grafana dashboard with 4+ visualizations
- Real-time data from actual truck

**Digital Twins & Industry Quest:**
- Real truck telemetry bound to digital model
- Anomaly detection with visual feedback
- Industry Quest labs integration (Weeks 15-17)
### How to Complete This Assessment

1. Ensure A4 device fully functional (all sensors/actuators)
2. Complete AWS integration from A5 (IoT Core, Shadows, Rules)
3. Implement anomaly detection and visual feedback
4. Create run down of the Capstone Project
5. Commit all files to GitHub
6. Fill out this form with your submission details
7. Copy completed form into Blackboard by the due date
### What to Submit on GitHub

- ✅ Complete `/A6-Capstone-Fleet-Demo/` folder with all code
- ✅ `/media` – Grafana Evidence
- ✅ Run down of Capstone Project

---
## Student Information

| Field               | Details                    |
| ------------------- | -------------------------- |
| **Student Name**    | Ben Timewell               |
| **Student ID**      | V093350                    |
| **Assessment**      | A6 – Capstone Fleet System |
| **Submission Date** | 25/05/2026                 |

---

## Assessment Summary

### GitHub Portfolio Repository

| Field                 | Details                                   |
| --------------------- | ----------------------------------------- |
| **Repository URL**    | https://github.com/GebwellB/IoT-Portfolio |
| **Assessment Folder** | `/A6-Capstone-Fleet-Demo/`                |
| **Last Commit Date**  | 25/05/2026                                |
### Work Completed

**Executive Summary (2-3 sentences):**  
Describe your complete fleet monitoring system: hardware, AWS services, and business value.

Given the amount of AWS services that are not enabled in the lab environment, my project ended up being:

- Single Truck Thing in AWS, receiving data from a physical MPU, RFID and Temperature sensor.
- The Truck Thing received MQTT data, which then passed into the AWS Lambda Function. This then saved the data into the DynamoDB as well as pass the data over to CloudWatch, which would then flag alerts if the temperate would get to high. Given how the custom namespace is implemented (inside the Lambda function), this system is not very robust. But, this is a limitation due to the lab environment.
- CloudWatch will send email alerts if the temperature is over 52.5 degrees, and return to normal operation when below.
- The Grafana dashboard is a very cobbled together solution, and by no means would EVER be used in the real world. It is only done this way, because of the lab environment restrictions. Ideally, I would just use AWS Grafana, IoT SiteWise and Athena to display my dashboard. But, none of those work in the lab, thanks to IAM permissions. (I also can't create a user, or adjust permissions, because that would mean Jeff Bezos would lose $0.05 while I test things, and we can't have that)
- How the data is displayed in Grafana:
	- The Lambda function mentioned earlier, dumps the entire database after saving the latest data received, to an S3 bucket. (This is horrible, and expensive in the long run. It also increases Lambda run time from 2ms to about 3 seconds.)
	- I then had to *manually* download the JSON file from the S3 bucket, as the lab environment cannot connect to the S3 bucket (due to IAM user creation and role assignment)
	- After I downloaded the JSON file, I uploaded it to GitHub [here](https://github.com/GebwellB/IoT-Portfolio/blob/main/A6-Capstone-Fleet-Demo/code/truck_data_export.json). This is the main data source used in Grafana. This is also horrible, as GitHub will *eventually* limit my access and block me from constantly pinging it for the latest info, not to mention constantly *adding* data to it.
	- Now that I have a data source, I used the Grafana plugin, "Infinity". This is slightly better than the inbuilt Grafana JSON plugin, as it allows filtering on the columns. Very handy given the JSON data is a mess.
	- From there, I just made 4 different graphs to show different data from the truck. Because it's only 1 single data point, date filtering does not work. To get around this, I would need to have several JSON files with different timestamps to show correctly. But due to the lab environment restrictions, this horrible hodge-podge of a solution *kinda works if you don't look at it*.
- The AWS Services I ended up using:
	- IoT Core
	- DynamoDB
	- Lambda Functions
	- CloudWatch
	- S3
---

## Assessment Evidence

### Code Organization

| Requirement        | Evidence Provided | Location in Repository                                |
| ------------------ | ----------------- | ----------------------------------------------------- |
| AWS Receiver Code  | ✅ Included        | `/A6-Capstone-Fleet-Demo/code/`                       |
| DynamoDB JSON Dump | ✅ Included        | `/A6-Capstone-Fleet-Demo/code/truck_data_export.json` |
### Hardware & Sensors

| Component                      | Status       | Verified                 |
| ------------------------------ | ------------ | ------------------------ |
| Real Raspberry Pi truck device | ✅ Functional | Sensors publishing MQTT  |
| DHT11 (temp/humidity)          | ✅ Working    | Values in telemetry      |
| GY-521 (vibration)             | ✅ Working    | Values in telemetry      |
| Touch sensor (cabin lock)      | ✅ Working    | State in telemetry       |
| RGB LED indicator              | ✅ Working    | Colour changes on alerts |

### AWS Cloud Services

| Service   | Configuration                     | Status     |
| --------- | --------------------------------- | ---------- |
| IoT Core  | Things, certificates, MQTT topics | ✅ Complete |
| IoT Rules | Routes to DynamoDB, SNS           | ✅ Complete |
| DynamoDB  | Time-series storage               | ✅ Complete |
| SNS       | Alert notifications               | ✅ Complete |
| Lambda    | Anomaly detection logic (if used) | ✅ Optional |
### Digital Twins & Analytics

| Component                 | Evidence                         | Status     |
| ------------------------- | -------------------------------- | ---------- |
| **Anomaly Visualisation** | Grafana shows anomalies          | ✅ Complete |
### Documentation

| Document              | Pages                            | Status     |
| --------------------- | -------------------------------- | ---------- |
| Architecture diagram  | Block diagram showing full flow  | ✅ Included |
| Setup guide           | Deployment instructions          | ☐ Included |

### Demonstration Evidence

Grafana Evidence:

All 4 graphs showing data:
![[grafana-all.png]](media/grafana-all.png)

MPU Data:
![[grafana-mpu.png]](media/grafana-mpu.png)

RFID Card Reader:
![[grafana-rfid.png]](media/grafana-rfid.png)

Last 20 Temperature readings:
![[grafana-temperature-last-20.png]](media/grafana-temperature-last-20.png)

All Temperature's recorded:
![[grafana-temperature-all.png]](media/grafana-temperature-all.png)

| Requirement             | Link/Location                                        | Status     |
| ----------------------- | ---------------------------------------------------- | ---------- |
| **GitHub Repository**   | URL with all code organized                          | ✅ Complete |
| **Grafana Screenshots** | Shows what information is being pulled from the JSON | ✅ Complete |

---

## Assessment Evidence Checklist

### Hardware & Sensors

| Requirement                                     | Completed |
| ----------------------------------------------- | --------- |
| Real Raspberry Pi truck device fully functional | ✅         |
| All A1-A3 sensors integrated and reading        | ✅         |
| Actuators functional (LED)                      | ✅         |
| Sensors publishing continuous telemetry         | ✅         |
| Data reaches AWS IoT Core successfully          | ✅         |

### AWS Cloud

| Requirement                              | Completed |
| ---------------------------------------- | --------- |
| IoT Core Thing created with X.509 certs  | ✅         |
| MQTT topics structured correctly         | ✅         |
| IoT Rules routing messages               | ✅         |
| DynamoDB storing telemetry               | ✅         |
| SNS sending alerts on anomalies          | ✅         |
### Analytics

| Requirement                           | Completed |
| ------------------------------------- | --------- |
| Anomaly detection rules implemented   | ✅         |
| 4+ visualizations in dashboard        | ✅         |
| Fleet health grid showing sensor data | ✅         |
### Testing & Scenarios

| Requirement                                | Completed |
| ------------------------------------------ | --------- |
| Scenario 1: Normal operation (all green)   | ✅         |
| Scenario 2: Sensor anomaly (trigger alert) | ✅         |
| Grafana & CloudWatch responds to anomalies | ✅         |
### Documentation

| Requirement                                | Completed |
| ------------------------------------------ | --------- |
| Setup guide with deployment steps          | ✅         |
| Unit mapping to ICTIOT503 criteria         | ✅         |
| GitHub repository organized and accessible | ✅         |
| All code clean and commented               | ✅         |

---

## Optional Notes

Due to the incredibly limiting parts of the AWS Learner Lab, A6 is only Grafana integration. And integration is a *strong* word, considering it was still *very* manual to get data from point A to point B. It works, but there's much better ways to do it than what I've done. I've only done it this way because I *had to*.

---

## Submission Declaration

By submitting this form, I confirm that:

- ✅ All code in my A6 folder is my own work
- ✅ System integrates all A1-A5 components
- ✅ AWS services are properly configured and secure
- ✅ Testing is comprehensive and documented
- ✅ Code follows ICTIOT502/503 assessment requirements
- ✅ I have not plagiarized or breached academic integrity

---

## For Assessor Use

| Field | Details |
|-------|---------|
| **Assessor Name** | [Assessor completes] |
| **Date Assessed** | [Assessor completes] |
| **Result** | ☐ Satisfactory ☐ Not Yet Satisfactory |
| **Portfolio Quality** | ☐ Excellent ☐ Good ☐ Acceptable |
| **System Integration** | ☐ Complete ☐ Mostly Complete ☐ Partial |
| **Feedback** | [Assessor completes] |

---

**Submission recorded by Blackboard:** [Auto-recorded]

**Your actual work is assessed on GitHub. This form provides proof of submission.**
