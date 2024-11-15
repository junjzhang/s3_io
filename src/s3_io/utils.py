import asyncio
import os
import sys
import threading
import time

from openxlab.dataset.commands.utility import ContextInfoNoLogin


def get_dataset_meta(dataset_repo):
    ctx = ContextInfoNoLogin()
    client = ctx.get_client()
    parsed_dateset_repo_name = dataset_repo.replace("/", ",")
    data_dict = client.get_api().get_dataset_files(dataset_name=parsed_dateset_repo_name, needContent=True)
    return data_dict

def create_sems(sems_info_dict: dict) -> dict:
    sems = {}
    for sem_name, sem_info in sems_info_dict.items():
        sems[sem_name] = asyncio.Semaphore(sem_info["max_instances"])
    return sems

class ProgressPercentage(object):
    def __init__(self, filename: str):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
        self._start_time = time.time()
        self._last_time = self._start_time
        self._last_seen_so_far = 0
        self._bandwidth = ""

    def _human_readable(self, amount: float, bandwidth: bool = False) -> str:
        if amount < 1024:
            return f"{amount:.2f}" + (" B" if not bandwidth else " B/s")
        elif amount < 1024 * 1024:
            return f"{amount / 1024:.2f}" + (" KB" if not bandwidth else " KB/s")
        elif amount < 1024 * 1024 * 1024:
            return f"{amount / 1024 / 1024:.2f}" + (" MB" if not bandwidth else " MB/s")
        else:
            return f"{amount / 1024 / 1024 / 1024:.2f}" + (" GB" if not bandwidth else " GB/s")

    def __call__(self, bytes_amount: int):
        """更新进度条和带宽"""
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100

            current_time = time.time()
            time_elapsed = current_time - self._last_time
            if time_elapsed >= 1:
                raw_bandwidth = (self._seen_so_far - self._last_seen_so_far) / time_elapsed
                self._bandwidth = self._human_readable(raw_bandwidth, bandwidth=True)
                self._last_time = current_time
                self._last_seen_so_far = self._seen_so_far
            sys.stdout.write(
                "\r%s  %.2f%%  %s / %s  (Bandwidth: %s)"
                % (
                    self._filename,
                    percentage,
                    self._human_readable(self._seen_so_far),
                    self._human_readable(self._size),
                    self._bandwidth,
                )
            )
            sys.stdout.flush()

