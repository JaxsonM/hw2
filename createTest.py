import unittest
from unittest.mock import patch, Mock
import consumer
import json

class TestCreateOperation(unittest.TestCase):

    @patch('consumer.boto3.session.Session')  # Mock the boto3 session
    def test_create_operation(self, mock_session):
    # Mocking the s3 client creation
        mock_s3_client = Mock()

    # This ensures that when session.client('s3') is called, it returns mock_s3_client.
        mock_session.return_value.client.return_value = mock_s3_client
        
        widget_request_content = {
            'type': 'create',
            'widgetId': 'sample_widget_id',
            'otherAttributes': [
                {'name': 'color', 'value': 'blue'},
                {'name': 'size', 'value': 'large'}
            ]
        }

        # Mocking the response of s3.list_objects_v2 to simulate having 1 object
        mock_s3_client.list_objects_v2.return_value = {
            'KeyCount': 1,
            'Contents': [{'Key': 'sample_key'}]
        }

        # Mocking the response of s3.get_object to simulate retrieving our sample widget request
        mock_s3_client.get_object.return_value = {
            'Body': Mock(read=lambda: json.dumps(widget_request_content).encode('utf-8'))
        }

        # Call the process_requests function
        consumer.process_requests("bucket", "sample_bucket_requests", "sample_bucket_web")

        # Check if the s3.put_object method was called, indicating a successful create operation
        self.assertTrue(mock_s3_client.put_object.called)

if __name__ == '__main__':
    unittest.main()
