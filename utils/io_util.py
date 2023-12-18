import os

def read_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        if os.path.isabs(file_path):
            raise FileNotFoundError(f"file_path={file_path}")
        with open(os.path.join("..", file_path), 'r') as f:
            return f.read()