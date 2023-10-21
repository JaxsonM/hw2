import unittest
import boto3
import consumer  # Assuming 'consumer' is the name of your module
import json
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
        #print("HELLO")

        # Call the process_requests function
        consumer.process_requests("bucket", BUCKET_REQUESTS, BUCKET_WEB, False)

        # Check if the widget was added to the BUCKET_WEB
        objects_in_web_bucket = conn.list_objects_v2(Bucket=BUCKET_WEB)
        self.assertEqual(objects_in_web_bucket['KeyCount'], 1)

        # Further checks can be done based on your expectations, e.g., checking the content of the uploaded widget, etc.

if __name__ == '__main__':
    unittest.main()
