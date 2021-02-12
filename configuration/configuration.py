from pathlib import Path
import json
from typing import *

class aws_configuration:
    def __init__(self, config_file: str):
        self._config_file = config_file
        self.load()
    
    def load(self, config_file = None):
        if config_file is None:
            config_file = self._config_file
            path = Path(config_file)
        self.config = json.loads(path.read_text())
    
    def save(self, config_file = None):
        if config_file is None:
            config_file = self._config_file
        json_str = json.dumps(self.config)
        Path(config_file).write_text(json_str)
    
    def get_endpoint(self) -> str:
        return self.config["endpoint"]
    
    def set_endpoint(self, value: str):
        self.config["endpoint"] = value

    def get_client_id(self) -> str:
        return self.config["client_id"]
    
    def set_client_id(self, value: str):
        self.config["client_id"] = value

    def get_path_to_cert(self) -> str:
        return self.config["path_to_cert"]

    def get_path_to_key(self) -> str:
        return self.config["path_to_key"]
    
    def get_path_to_root(self) -> str:
        return self.config["path_to_root"]


