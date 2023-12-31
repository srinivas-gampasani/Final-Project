# utils/data_handler.py
import json

def read_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_data_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
