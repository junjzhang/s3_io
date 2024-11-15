# s3_io

This repo aims to provide an asyncio-based tool for downloading and processing datasets and uploading them to S3 to maximize the throughput.

## Usage

### installation

```bash
pixi install
## the latest version of openxlab cannot be install from pixi, using pip
pixi shell && pip install openxlab
```

### prepare s3 credentials
* write your access key and secret key to [setup_env.sh](./scripts/setup_env.sh)
* run `source ./scripts/setup_env.sh && pixi r hello_world` to test the connection

### Example
A example of downloading openxlab dataset to local and unzip, then upload to s3 is provided. You can run the following command to launch it:

```bash
bash ./scripts/download_internvid_to_s3.sh
```
