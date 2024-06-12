import json

def read_storage(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def write_storage(file_path, storage):
    with open(file_path, 'w') as file:
        json.dump(storage, file, indent=4)
