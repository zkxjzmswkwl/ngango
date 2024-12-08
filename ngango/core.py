import os


class DjangoProject:
    def __init__(self, project_name: str, path: str):
        self._project_name = project_name
        self._path = path

    @property
    def project_name(self):
        return self._project_name

    @property
    def path(self):
        return self._path

    def get_settings(self):
        settings_path = os.path.join(self.path, 'settings.py')
        with open(settings_path) as f:
            return f.read()
