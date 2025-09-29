# Event-Driven Sales Data Processing Project

## Overview
This project demonstrates an **event-driven data processing pipeline** using **AWS services** like Lambda, Step Functions, S3, DynamoDB, and SQS. The pipeline automates the ingestion, validation, and storage of sales orders data in near real-time.

---

## Architecture
          +----------------+
          |   S3 Bucket    |  <-- Upload JSON orders
          | orders-data-p  |
          +--------+-------+
                   |
                   v
          +----------------+
          | Step Functions |
          |  State Machine |
          +--------+-------+
                   |
                   v
         +-------------------+
         |       Map State    |  <-- Iterates over orders
         +--------+----------+
                  |
      +-----------+------------+
      |                        |
      v                        v
+------------+           +----------------+
|  Lambda    |           | SQS DLQ        |
| orders-data|           | order-data-dlq |
| Validate   |           | (Failed Orders)|
+-----+------+           +----------------+
      |
      v
+----------------+
|  DynamoDB      |
|  ecom-orders   |
+----------------+

1. **S3 Bucket (`orders-data-p`)**: Stores incoming orders JSON files.
2. **Step Functions**: Orchestrates the workflow:
   - Retrieves S3 objects.
   - Iterates through orders using a Map state.
   - Validates orders via Lambda.
   - Stores valid orders in DynamoDB.
   - Sends failed orders to SQS DLQ.
3. **Lambda (`orders-data`)**: Validates orders, checks for required fields like `contact-info`.
4. **DynamoDB (`ecom-orders`)**: Stores validated order details.
5. **SQS DLQ (`order-data-dlq`)**: Captures failed orders for further inspection.

---

## Features

- Event-driven architecture with **Step Functions and Lambda**.
- Scalable Map state for processing multiple orders concurrently.
- Automatic failure handling using **SQS Dead Letter Queue**.
- AWS best practices: IAM roles, retries, and result selectors.
- Real-time ingestion from S3 and storage in DynamoDB.

---

## Sample Input & Output

**S3 Sample Order:**

```json
{
  "orders": [
    {
      "order-info": {"OrderId": "1", "item-id": "101", "item-desc": "Item One", "qty": "1"},
      "contact-info": {"name": "Foo Bar", "email": "foobar@test.com"}
    }
  ]
}
DynamoDB Output:

OrderId	item-id	qty	contact-name	contact-email
1	101	1	Foo Bar	foobar@test.com
--------------------------

How to Run Locally
Upload sample JSON files to the S3 bucket orders-data-p.
Trigger the Step Functions state machine event_driven_sales_data_processing.
Monitor Lambda logs in CloudWatch.
Check DynamoDB table ecom-orders for inserted orders.
Failed orders will appear in the SQS DLQ order-data-dlq.
------------------------------------------------------------

AWS Services Used
S3 – Storage for incoming orders
Lambda – Order validation
Step Functions – Workflow orchestration
DynamoDB – Persistent storage for valid orders
SQS – Dead Letter Queue for failures
CloudWatch – Monitoring logs
---------------------------------------------------------------
Author
Prateek Shaw
