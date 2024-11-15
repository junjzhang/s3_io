import os

import boto3


# Initialize a boto3 client for listing the buckets
s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('FSSPEC_S3_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('FSSPEC_S3_KEY'),
    aws_secret_access_key=os.getenv('FSSPEC_S3_SECRET'),
    region_name=os.getenv('AWS_REGION')
)

try:
    # List all buckets
    response = s3_client.list_buckets()
    print("Available Buckets:")
    for bucket in response['Buckets']:
        print(bucket['Name'])
except Exception as e:
    print(f"Error accessing buckets: {e}")
