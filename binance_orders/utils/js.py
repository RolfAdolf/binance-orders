import json
from pathlib import Path
from typing import Dict


def load_request(js_file_path: str | Path) -> Dict:
    with open(js_file_path) as json_file:
        request = json.load(json_file)
    return request
