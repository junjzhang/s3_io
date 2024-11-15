import asyncio
import logging
import shutil

from pathlib2 import Path

from s3_io.async_task import download_from_openxlab, unzip_locally, upload_to_s3
from s3_io.logger import create_logger
from s3_io.utils import create_sems, get_dataset_meta


async def data_task(s3_bucket: str, dataset_repo:str, file_name: str, local_dir: Path, loggers: dict, sems: dict):
    parsed_dataset_repo = dataset_repo.replace("/", "___")
    scheduler_logger = loggers["scheduler"]
    scheduler_logger.info(f"downloading {file_name} from {dataset_repo}")
    await download_from_openxlab(dataset_repo=dataset_repo, file_name=file_name, target_dir=local_dir.absolute(), logger=loggers["downloader"], sem=sems["downloader"])
    if file_name[0] == "/":
        file_name = file_name[1:]
    original_local_dir = local_dir
    local_dir = local_dir / parsed_dataset_repo
    local_file_path = local_dir / file_name
    if local_file_path.suffix == ".zip":
        scheduler_logger.info(f"unziping {file_name}")
        await unzip_locally(zip_file_path=local_file_path.absolute(), unzip_dir=local_dir.absolute(), logger=loggers["unzipper"], sem=sems["unzipper"])
        uploading_file_path = local_dir / file_name.replace(".zip", "")
        uploading_key = uploading_file_path.relative_to(original_local_dir).as_posix()
    else:
        uploading_file_path = local_file_path
        uploading_key = uploading_file_path.relative_to(original_local_dir).as_posix()
    scheduler_logger.info(f"uploading {file_name} to {s3_bucket}")
    await upload_to_s3(bucket_name=s3_bucket, file_path=uploading_file_path.absolute(), key=str(uploading_key), logger=loggers["uploader"], sem=sems["uploader"])


async def main(s3_bucket: str, dataset_repo: str, file_lists: list[str], local_dir: Path, loggers: dict, sems: dict):
    tasks = []
    for file_name in file_lists:
        tasks.append(asyncio.create_task(data_task(s3_bucket, dataset_repo, file_name, local_dir, loggers, sems)))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # constants
    log_dir = Path('./log')
    dataset_repo = "vd-foundation/InternVid-10M-FLT"
    local_dir = Path('/datasets/test')
    s3_bucket = "datasets"
    sems_info_dict = {
        "downloader": {"max_instances": 2},
        "unzipper": {"max_instances": 8},
        "uploader": {"max_instances": 1}
    }

    # handle dirs
    if log_dir.exists():
        # remove the log directory
        shutil.rmtree(log_dir)
    log_dir.mkdir(exist_ok=True)
    local_dir.mkdir(exist_ok=True)

    # set up logger
    loggers_info_dict = {
        "scheduler": {
            "name": "scheduler",
            "level": logging.INFO,
            "logging_file": str(log_dir / "scheduler.log")
        },
        "downloader": {
            "name": "downloader",
            "level": logging.INFO,
            "logging_file": str(log_dir / "downloader.log")
        },
        "unzipper": {
            "name": "unzipper",
            "level": logging.INFO,
            "logging_file": str(log_dir / "unzipper.log")
        },
        "uploader": {
            "name": "uploader",
            "level": logging.INFO,
            "logging_file": str(log_dir / "uploader.log")
        }
    }
    loggers = create_logger(loggers_info_dict)

    # set up semaphores
    sems = create_sems(sems_info_dict)

    dataset_meta = get_dataset_meta(dataset_repo)
    file_list = [file["path"] for file in dataset_meta["list"]]
    loggers["scheduler"].info(f"will download \n {"\n".join(file_list)}")
    asyncio.run(main(s3_bucket, dataset_repo, file_list, local_dir, loggers, sems))
