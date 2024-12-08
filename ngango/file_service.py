import os
from typing import List


def get_django_apps(path) -> List[str]:
    apps = []
    for root, dirs, files in os.walk(path):
        is_app = [file for file in files if file == 'models.py']
        if is_app:
            apps.append(os.path.basename(root))
    return apps
