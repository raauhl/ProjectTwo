import json


def create(data_json_blob, file_path):
    with open(file_path, 'w') as file:
        json.dump(data_json_blob, file)
    print(f'JSON object saved as {file_path}.')

def read(file_path):

    with open(file_path, 'r') as file:
        data = json.load(file)
    print(f'JSON object read as {file_path}.')
    return data


