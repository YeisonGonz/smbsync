import json
import os
from src.Configuration import Configuration
cf = Configuration()

def get_key():
    with open(cf.config.KEY_PATH, 'r', encoding='utf-8') as f:
        json_content = json.load(f)
        return json_content['encryption_key']

def get_currentshell_path():
    # Like a 'pwd' command
    return os.getcwd()