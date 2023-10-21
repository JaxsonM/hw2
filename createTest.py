import consumer
import json
import boto3
from moto import mock_dynamodb2
from moto import mock_s3

class TestCreateOperation(unittest.TestCase):

    @mock_s3
    def test_create_operation(self):
        # Set up the mock S3 environment
        conn = boto3.client('s3', region_name='us-east-1')
        BUCKET_REQUESTS = 'sample_bucket_requests'
        BUCKET_WEB = 'sample_bucket_web'
        conn.create_bucket(Bucket=BUCKET_REQUESTS)
        conn.create_bucket(Bucket=BUCKET_WEB)

        # Sample widget request
        widget_request_content = {
            'type': 'create',
            'widgetId': 'sample_widget_id',
            'owner': 'sample_owner',
            'otherAttributes': [
                {'name': 'color', 'value': 'blue'},
                {'name': 'size', 'value': 'large'}
            ]
        }

        # Add the widget request to the bucket
        conn.put_object(Bucket=BUCKET_REQUESTS, Key='sample_key', Body=json.dumps(widget_request_content))

        # Call the process_requests function
        consumer.process_requests("bucket", BUCKET_REQUESTS, BUCKET_WEB, False)

        # Check if the widget was added to the BUCKET_WEB
        objects_in_web_bucket = conn.list_objects_v2(Bucket=BUCKET_WEB)
        self.assertEqual(objects_in_web_bucket['KeyCount'], 1)


class TestDynamoDBOperation(unittest.TestCase):

    @mock_dynamodb2
    def test_create_operation_dynamodb(self):
        # Set up the mock DynamoDB environment
        dynamo_client = boto3.client('dynamodb', region_name='us-east-1')
        
        # Define the table name
        TABLE_NAME = 'WidgetsTable'
        
        # Create a new table
        dynamo_client.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{'AttributeName': 'widgetId', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'widgetId', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        )
        
        # Sample widget request
        widget_request_content = {
            'type': 'create',
            'widgetId': 'sample_widget_id',
            'owner': 'sample_owner',
            'otherAttributes': [
                {'name': 'color', 'value': 'blue'},
                {'name': 'size', 'value': 'large'}
            ]
        }

        # Using the consumer method to process the request and save it to DynamoDB
        consumer.process_requests("dynamo", BUCKET_REQUESTS, TABLE_NAME, False)

        # Check if the widget was added to the DynamoDB table
        response = dynamo_client.get_item(TableName=TABLE_NAME, Key={'widgetId': {'S': 'sample_widget_id'}})
        self.assertIn('Item', response)

if __name__ == '__main__':
    unittest.main()
