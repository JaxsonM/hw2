# HW2 - Widget Request Processor
---

## Overview
This Python script efficiently handles widget requests by processing them and storing the results in AWS S3 buckets or DynamoDB tables. Designed for an AWS services class, the project showcases my ability to integrate various AWS services using Python and Boto3. It provides valuable insight into the practical application of cloud services for data handling and storage, demonstrating skills that are critical in cloud software development.

## Technologies Used
- **Python**: Scripting language for the core application.
- **AWS S3**: Object storage service used for storing widget requests and processed data.
- **AWS DynamoDB**: NoSQL database service used for efficient data retrieval and management.
- **Boto3**: AWS SDK for Python, allowing Python developers to write software that uses services like Amazon S3 and Amazon DynamoDB.
- **Logging**: Utilization of Python's logging module to provide insight into the application's operation.

## Prerequisites
- AWS CLI installed and configured with appropriate permissions.
- Python 3.x installed.
- Boto3 library installed (`pip install boto3`).

## Setup and Execution
Clone the repository and navigate to the script's directory. Execute the script using the following command:

```bash
python consumer.py --requests_bucket [REQUESTS_BUCKET_NAME] --destination_flag [DESTINATION_FLAG] --destination_name [DESTINATION_NAME]
```

### Parameters:
- `--requests_bucket`: The name of the S3 bucket containing the widget requests.
- `--destination_flag`: Determines the storage destination (`wb` for S3 bucket, `dwt` for DynamoDB).
- `--destination_name`: The name of the S3 bucket or DynamoDB table for data storage.

#### Example Command:
```bash
python consumer.py --requests_bucket my-request-bucket --destination_flag wb --destination_name my-storage-bucket
```

## Functionality
The script continuously monitors the specified S3 bucket for new widget requests and processes them according to their type (create, update, or delete). Data storage is managed based on the specified destination flag, ensuring that each request is handled promptly and the source bucket is kept clean by removing processed requests.

## Unit Testing
Includes unit tests for S3 and DynamoDB operations using the `unittest` framework and `moto` library to mock AWS services, ensuring that functionality is verified without the need for actual AWS service interaction.

---
