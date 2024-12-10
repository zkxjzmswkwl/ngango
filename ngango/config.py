import json


class Config:
    def __init__(self, config_path: str):
        self._config_path = config_path
        self._blob = None
        self._frontend_path: str = ""
        self._output_destinations: dict = {}
        self._load_config()

    @property
    def frontend_path(self) -> str:
        return self._frontend_path

    @property
    def output_destinations(self) -> dict:
        return self._output_destinations

    def _load_config(self):
        with open(self._config_path, "r") as f:
            self._blob = json.load(f)
        frontend = self._blob.get("frontend", None)
        if not frontend:
            raise ValueError("frontend not found in config.")
        self._frontend_path = frontend.get("path", None)
        self._output_destinations = frontend.get("output_destinations", None)
        if not self._frontend_path:
            raise ValueError("frontend_path not found in config.")
        if not self._output_destinations:
            raise ValueError("output_destinations not found in config.")

    def __str__(self):
        return f"Config(frontend_path={self.frontend_path}, output_destinations={self.output_destinations})"