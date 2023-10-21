import boto3
import json
import uuid
import time
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize a session using Amazon Simple Storage Service (S3)
session = boto3.session.Session()
s3 = session.client('s3')

# Define your buckets
BUCKET_REQUESTS = 'usu-cs5260-percy-requests'
BUCKET_WEB = 'usu-cs5250-percy-web'


def flatten_attributes(widget_request):
    # Start with the existing widget_request (excluding 'otherAttributes')
    flattened_data = {key: value for key, value in widget_request.items() if key != "otherAttributes"}

    # Flatten 'otherAttributes'
    for attribute in widget_request.get("otherAttributes", []):
        flattened_data[attribute["name"]] = attribute["value"]

    return flattened_data


def process_requests(destination):
   while True:  # This is the outer loop that will keep the function running indefinitely
        try:
            # List the objects within the specified bucket
            response = s3.list_objects_v2(Bucket=BUCKET_REQUESTS)

            # Check if the bucket is empty
            if response['KeyCount'] == 0:
                print("No requests to process. Waiting for new requests...")
                time.sleep(0.1)  # Wait for 100ms
                continue  # This will skip the rest of the loop and start from the beginning

            # If there are objects, we'll only handle the first one
            first_object = response['Contents'][0]
            file_key = first_object['Key']

            # Get the object based on the key and bucket name
            file_object = s3.get_object(Bucket=BUCKET_REQUESTS, Key=file_key)
            request_content = file_object['Body'].read().decode('utf-8')
            widget_request = json.loads(request_content)
            #print(widget_request)
            print(f"Working on: {widget_request['widgetId']} Type: {widget_request['type']}")
            time.sleep(1)
            if destination == "bucket":
                # Perform the operation based on the request type
                if widget_request['type'] == 'create':
                    widget_id = str(uuid.uuid4())  # Create a new UUID for the widget
    
                    # Incorporate all data from the widget request into the widget_object
                    widget_object = widget_request.copy()
                    widget_object["widget_id"] = widget_id
    
                    # Compute the owner key
                    owner_key = widget_request['owner'].replace(" ", "-").lower()
    
                    # Upload the new widget object to the web bucket
                    s3.put_object(Body=json.dumps(widget_object), Bucket=BUCKET_WEB, Key=f'widgets/{owner_key}/{widget_id}')
                    print(f"UPLOADED with key: widgets/{owner_key}/{widget_id}")
                    time.sleep(1)
    
                elif widget_request['type'] == 'update':
                    widget_id = widget_request['widgetId']
                    new_data = widget_request['otherAttributes']
    
                elif widget_request['type'] == 'delete':
                    widget_id = widget_request['widgetId']
                    # Delete the specified widget object
                    #s3.delete_object(Bucket=BUCKET_WEB, Key=f'widgets/{widget_id}')
    
                else:
                    print(f"Unknown request type: {widget_request['type']}")
            elif destination == "dynamo":
                dynamodb = session.resource('dynamodb')
                table = dynamodb.Table('widgets') 

                if widget_request['type'] == 'create':
                    widget_id = str(uuid.uuid4())  # Create a new UUID for the widget
                    widget_request["id"] = widget_id  # Change here
                    flattened_widget = flatten_attributes(widget_request)
                    table.put_item(Item=flattened_widget)  # Store the flattened widget in the DynamoDB table
                    print(f"Widget {widget_id} added to DynamoDB.")
    
                elif widget_request['type'] == 'update':
                    widget_id = widget_request['widgetId']
                    new_data = widget_request['otherAttributes']
    
                elif widget_request['type'] == 'delete':
                    widget_id = widget_request['widgetId']
                    # Delete the specified widget object
                    #s3.delete_object(Bucket=BUCKET_WEB, Key=f'widgets/{widget_id}')
    
                else:
                    print(f"Unknown request type: {widget_request['type']}")

            # Delete the request object from the bucket
            s3.delete_object(Bucket=BUCKET_REQUESTS, Key=file_key)
            print("Deleted Request\n")
            time.sleep(1)

        except NoCredentialsError:
            print("Credentials not available")
            break
        except PartialCredentialsError:
            print("Incomplete credentials")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    destination = "dynamo"
    #destination = "bucket"
    process_requests(destination)
