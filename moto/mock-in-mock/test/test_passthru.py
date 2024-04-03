import moto
import boto3
import pytest
import os
from mypy_boto3_s3 import S3Client

import requests
import requests_mock

from moto.core.models import override_responses_real_send

# https://requests-mock.readthedocs.io/en/latest/adapter.html#adapter
session = requests.Session()
adapter = requests_mock.Adapter()
session.mount('mock://', adapter)

# Creates the mock message
adapter.register_uri('GET', 'mock://test.com', text='Message from the mock service')

def create_bucket(name, location):
    s3_client = boto3.client("s3", region_name="us-east-2")
    s3_client.create_bucket(
        Bucket=name, 
        CreateBucketConfiguration={"LocationConstraint": location})


@pytest.fixture(scope='function')
def aws_credentials():
    # Mocked AWS Credentials for Moto
    os.environ['AWS_ACCESS_KEY_ID'] = 'fake-access-key'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'fake-secret-key'
    os.environ['AWS_SECURITY_TOKEN'] = 'fake-security-token'
    os.environ['AWS_SESSION_TOKEN'] = 'fake-session-token'


@pytest.fixture(scope="function")
def create_moto_client(aws_credentials):
    with moto.mock_aws():
        yield boto3.client("s3")


def test_use_of_mock(create_moto_client: S3Client ):
    create_bucket("bucket1", "us-east-2")
    create_bucket("bucket2", "us-east-2")
    create_bucket("bucket3", "us-east-2")

    data_to_upload = "Hello, Moto!"
    s3_bucket = "bucket1"
    s3_key = "example.txt"
    response = create_moto_client.put_object(Body=data_to_upload, Bucket=s3_bucket, Key=s3_key)

    objects = create_moto_client.list_objects(Bucket=s3_bucket)
    print(objects)
    assert objects["Contents"][0]["Key"] == "example.txt"

    buckets = create_moto_client.list_buckets()
    print(buckets)

    resp = session.get('mock://test.com')
    print(resp.text)

    # Trying to mock via moto
    my_own_mock = responses.RequestsMock(assert_all_requests_are_fired=True)
    override_responses_real_send(my_own_mock)
    my_own_mock.start()
    my_own_mock.add_passthru("http://some-website.com")