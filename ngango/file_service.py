import os
from typing import List


def folders_containing_file(path: str, file_name: str) -> List[str]:
    apps = []
    for root, _, files in os.walk(path):
        is_app = [file for file in files if file == file_name]
        if is_app:
            apps.append(os.path.basename(root))
    return apps


def get_file_handle(path: str, mode: str):
    try:
        return open(path, mode)
    except Exception:
        # Not found, likely.
        return None
