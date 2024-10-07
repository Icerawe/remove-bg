# test_lambda_function.py
import pytest
from lambda_function import handler

def test_handler():
    # Simulate the request object
    request = {
        "body": {
            "url": "https://plandee-image-transform.s3.ap-southeast-1.amazonaws.com/test/werabhat.jpeg"
        }
    }

    # Call the handler
    response = handler(request, None)

    # Assert the response
    assert response['statusCode'] == 200