import json
from pathlib import Path

def load_json(path:Path, default:dict={}):
    if not path.is_file():
        with open(path, "w") as f:
            json.dump(default, f, indent=4)
        return default
    
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default
    return default
