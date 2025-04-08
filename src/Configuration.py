from dataclasses import dataclass
import os

@dataclass
class ConfigurationData:
    DATABASE_FILE_PATH: str
    KEY_PATH: str
    DEFAULT_REMOTE_FOLDER: str


class Configuration:
    def __init__(self):
        data_home = os.getenv("XDG_DATA_HOME", os.path.join(os.path.expanduser("~"), ".local", "share"))
        app_data_dir = os.path.join(data_home, "smbsync")
        default_folder = "SambaRemoteFolder"
        os.makedirs(app_data_dir, exist_ok=True)

        self.config = ConfigurationData(
            DATABASE_FILE_PATH=os.path.join(app_data_dir, "base.db"),
            KEY_PATH=os.path.join(app_data_dir, "config.json"),
            DEFAULT_REMOTE_FOLDER=default_folder
        )
