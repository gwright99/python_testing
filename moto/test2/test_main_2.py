import sys
sys.path.insert(0, '../')

from moto import mock_aws
from src.main import lambda_handler
import boto3

def test_lambda_handler2(s3_mock, aws_credentials, create_bucket):
    # Event and Context are not used in this example
    event = {}
    context = {}

    # Invoke the Lambda function
    # with mock_aws():
    response = lambda_handler(event, context)

    # Check if the S3 object was created successfully
    assert response["statusCode"] == 200

    # Check if the object exists in S3
    objects = s3_mock.list_objects(Bucket='your-s3-bucket')
    assert objects["Contents"][0]["Key"] == "example.txt"
    print(objects)

# def test_lambda_handler(aws_credentials, s3_mock):

#     event = {}
#     context = {}
#     with mock_aws():
#         response = lambda_handler(event, context)

#         assert response["statusCode"] == 200
#         objects = s3_mock.list_objects(Bucket='your-s3-bucket')
#         assert objects["Contents"][0]["Key"] == "example.txt"

# @mock_aws
# def test_my_model_save():
#     conn = boto3.client("s3", region_name="us-east-1")

#     conn.create_bucket(
#         Bucket="your-s3-bucket", 
#         CreateBucketConfiguration={"LocationConstraint": "us-east-2"})

#     data_to_upload = "Hello, Moto!"
#     s3_bucket = "your-s3-bucket"
#     s3_key = "example.txt"
#     response = conn.put_object(Body=data_to_upload, Bucket=s3_bucket, Key=s3_key)

#     # assert response["statusCode"] == 200
#     objects = conn.list_objects(Bucket='your-s3-bucket')
#     assert objects["Contents"][0]["Key"] == "example.txt"
