import asyncio
import logging

from .utils import read_stream


async def download_from_openxlab(dataset_repo: str, file_name: str, target_dir: str, sem: asyncio.Semaphore, logger: logging.Logger):
    async with sem:
        proc = await asyncio.create_subprocess_exec(
            "stdbuf", "-oL",
            "openxlab", "dataset", "download",
            "--dataset-repo", dataset_repo,
            "--source-path", file_name,
            "--target-path", target_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        # monitor the process
        await asyncio.gather(read_stream(proc.stdout, logger), read_stream(proc.stderr, logger, is_error=True))
        return_code = await proc.wait()
        if return_code == 0:
            logger.info(f"downloading {file_name} from {dataset_repo} completed")
        else:
            logger.error(f"downloading {file_name} from {dataset_repo} failed")
        return proc.returncode
