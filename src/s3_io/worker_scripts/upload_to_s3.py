import argparse
import concurrent.futures
import os

import boto3
from boto3.s3.transfer import TransferConfig
from pathlib2 import Path

from s3_io.utils import ProgressPercentage


def upload_to_s3(bucket_name: str, file_path: str, key: str, max_concurrency: int = 16):
    s3_client = boto3.client(
        "s3",
        endpoint_url=os.getenv("FSSPEC_S3_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("FSSPEC_S3_KEY"),
        aws_secret_access_key=os.getenv("FSSPEC_S3_SECRET"),
        region_name=os.getenv("AWS_REGION"),
    )
    config = TransferConfig(max_concurrency=max_concurrency)
    try:
        print(f"uploading {file_path} to {bucket_name} with key {key}")
        s3_client.upload_file(file_path, bucket_name, key, Config=config, Callback=ProgressPercentage(file_path))
    except Exception as e:
        print(f"uploading {file_path} to {bucket_name} failed: {e}")
        return False
    return True

def upload_to_s3_parallelly(bucket_name: str, file_paths: list[str], keys: list[str], max_concurrency: int = 16, max_instances: int = 4):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(file_paths), max_instances)) as executor:
        futures = [executor.submit(upload_to_s3, bucket_name, file_path, key, max_concurrency) for file_path, key in zip(file_paths, keys)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results


def arg_parser():
    parser = argparse.ArgumentParser(description="upload file to s3")
    parser.add_argument("--bucket_name", type=str, required=True, help="bucket name")
    parser.add_argument("--file_path", type=str, required=True, help="file path")
    parser.add_argument("--key", type=str, required=True, help="key")
    parser.add_argument("--max_concurrency", type=int, default=16, help="max concurrency")
    parser.add_argument("--max_instances", type=int, default=32, help="max instances")
    return parser.parse_args()


if __name__ == "__main__":
    args = arg_parser()
    # check file or directory
    if os.path.isdir(args.file_path):
        file_dir = Path(args.file_path)
        file_paths = [file.absolute() for file in file_dir.glob("**/*")]
        keys = [args.key + "/" + file.relative_to(file_dir).as_posix() for file in file_paths]
        upload_to_s3_parallelly(args.bucket_name, file_paths, keys, args.max_concurrency, args.max_instances)
    else:
        upload_to_s3(args.bucket_name, args.file_path, args.key, args.max_concurrency)
