
import asyncio
import logging

from .utils import read_stream


async def upload_to_s3(bucket_name: str, file_path: str, key: str, sem, logger: logging.Logger, max_concurrency: int=16):
    async with sem:
        cmd = f"python -m s3_io.worker_scripts.upload_to_s3 --bucket_name {bucket_name} --file_path {file_path} --key {key} --max_concurrency {max_concurrency}"
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        # monitor the process
        await asyncio.gather(read_stream(proc.stdout, logger), read_stream(proc.stderr, logger, is_error=True))

        return_code = await proc.wait()
        if return_code == 0:
            logger.info(f"uploading {file_path} to {bucket_name} completed")
        else:
            logger.error(f"uploading {file_path} to {bucket_name} failed")
        return return_code
