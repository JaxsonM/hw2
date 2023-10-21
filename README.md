# hw2
---
# Widget Request Processor

This script is designed to process widget requests and either stores the result in an S3 bucket or a DynamoDB table, based on the provided parameters. It reads the requests from a designated S3 bucket and takes action depending on the type of request (create, update, or delete).

## Prerequisites

- AWS CLI installed and configured with appropriate permissions.
- Python 3.x
- Boto3 installed (`pip install boto3`).

## Logging

The program provides both console and file logging. Logs are written to `consumer.log` in the same directory where the script is executed.

## How to Use

1. Clone the repository or download the `consumer.py` script.
2. Navigate to the script's directory using your terminal.
3. Execute the script using the following command format:

```
python consumer.py --requests_bucket [REQUESTS_BUCKET_NAME] --destination_flag [DESTINATION_FLAG] --destination_name [DESTINATION_NAME]
```

### Parameters:

- `--requests_bucket` : Name of the S3 bucket that contains the widget requests. This is a required parameter.
  
- `--destination_flag` : Determines where the processed data will be stored. The options are:
  - `wb` : Data will be stored in an S3 bucket.
  - `dwt` : Data will be stored in a DynamoDB table.
  
  This is a required parameter.

- `--destination_name` : Name of the S3 bucket or DynamoDB table where the processed data will be stored. This is a required parameter.

#### Example:

```
python consumer.py --requests_bucket usu-cs5260-percy-requests --destination_flag -wb --destination_name usu-cs5250-percy-web
```

## Functionality

The script continuously polls the provided `--requests_bucket` to check for any new widget requests. If a new request is found, it processes the request as per its type (`create`, `update`, or `delete`). 

If the `--destination_flag` is set to `wb`, the processed data is stored in the specified S3 bucket (`--destination_name`). If the flag is set to `dwt`, the processed data is stored in the specified DynamoDB table.

Once the request is processed, it is deleted from the `--requests_bucket`.

---

Feel free to adjust the content as needed or add additional sections for any extra details or configurations you might have.