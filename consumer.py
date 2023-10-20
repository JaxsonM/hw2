import boto3
import json
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize a session using Amazon Simple Storage Service (S3)
session = boto3.session.Session()
s3 = session.client('s3')

# Define your buckets
BUCKET_REQUESTS = 'usu-cs5260-percy-requests'
BUCKET_WEB = 'usu-cs5250-percy-web'

def process_requests():
    while True:
        try:
            # List the objects within the specified bucket
            response = s3.list_objects_v2(Bucket=BUCKET_REQUESTS)

            # Check if the bucket is empty
            if response['KeyCount'] == 0:
                print("No requests to process. Waiting for new requests...")
                # Here, you should implement a waiting mechanism (like time.sleep or a more complex scheduler)
                continue

            # If there are objects, we'll only handle the first one as specified
            first_object = response['Contents'][0]
            file_key = first_object['Key']

            # Get the object based on the key and bucket name
            file_object = s3.get_object(Bucket=BUCKET_REQUESTS, Key=file_key)
            request_content = file_object['Body'].read().decode('utf-8')
            widget_request = json.loads(request_content)

            # Perform the operation based on the request type
            if widget_request['type'] == 'create':
                widget_id = str(uuid.uuid4())  # create a new UUID for the widget
                widget_object = {"widget_id": widget_id}  # This would be your actual widget object

                # Upload the new widget object to the web bucket
                s3.put_object(Body=json.dumps(widget_object), Bucket=BUCKET_WEB, Key=f'widgets/{widget_id}')

            elif widget_request['type'] == 'update':
                # Assuming the request contains an 'id' field specifying which widget to update
                widget_id = widget_request['id']
                new_data = widget_request['data']  # This would contain new data for the widget

                # Here, you would generally want to retrieve the object first, update fields, then put it back
                # For simplicity, we're assuming we're just replacing it with new data
                s3.put_object(Body=json.dumps(new_data), Bucket=BUCKET_WEB, Key=f'widgets/{widget_id}')

            elif widget_request['type'] == 'delete':
                widget_id = widget_request['id']
                # Delete the specified widget object
                s3.delete_object(Bucket=BUCKET_WEB, Key=f'widgets/{widget_id}')

            else:
                print(f"Unknown request type: {widget_request['type']}")

            # After processing, delete the request object from the bucket
            s3.delete_object(Bucket=BUCKET_REQUESTS, Key=file_key)

        except NoCredentialsError:
            print("Credentials not available")
            break
        except PartialCredentialsError:
            print("Incomplete credentials")
            break
        except KeyError:
            print("Waiting for new requests...")  # Handles the case of an empty bucket
            # Implement waiting mechanism here
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    process_requests()
