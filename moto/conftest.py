import boto3
import pytest
import os
from moto import mock_aws

# aws_credentials: A fixture to set up mocked AWS credentials using environment variables.
# s3_mock: A fixture that uses Moto's mock_s3 context manager to mock the S3 service. 
# It depends on the aws_credentials fixture to ensure mocked credentials are available.


@pytest.fixture(scope='function')
def aws_credentials():
    # Mocked AWS Credentials for Moto
    os.environ['AWS_ACCESS_KEY_ID'] = 'fake-access-key'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'fake-secret-key'
    os.environ['AWS_SECURITY_TOKEN'] = 'fake-security-token'
    os.environ['AWS_SESSION_TOKEN'] = 'fake-session-token'


@pytest.fixture(scope='function')
def s3_mock(aws_credentials):
    with mock_aws():
        yield boto3.client('s3')


@pytest.fixture(scope='function')
def create_bucket(aws_credentials, s3_mock):

    s3_mock.create_bucket(
        Bucket="your-s3-bucket", 
        CreateBucketConfiguration={"LocationConstraint": "us-east-2"})