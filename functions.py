import os

def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0


def validate_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'{file_path} is not found')

    if not os.path.isfile(file_path):
        raise IsADirectoryError(f'{file_path} is not file')

    if not file_path.endswith('.csv'):
        raise ValueError(f'{file_path} is not .csv file')

    if is_file_empty(file_path):
        print(f'Warning: {file_path} is empty')

    return True