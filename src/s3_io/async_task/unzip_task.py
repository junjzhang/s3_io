import asyncio
import logging

from .utils import read_stream


async def unzip_locally(zip_file_path: str, unzip_dir: str, sem: asyncio.Semaphore, logger: logging.Logger):
    async with sem:
        cmd = f"7z x {zip_file_path} -o{unzip_dir}"
        print(cmd)
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        # monitor the process
        await asyncio.gather(read_stream(proc.stdout, logger), read_stream(proc.stderr, logger, is_error=True))

        return_code = await proc.wait()
        if return_code == 0:
            logger.info(f"unzipping {zip_file_path} to {unzip_dir} completed")
        else:
            logger.error(f"unzipping {zip_file_path} to {unzip_dir} failed")
        return return_code
