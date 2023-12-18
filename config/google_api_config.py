import os
def initialize_google_api(key_file_path = 'config/google_key.txt'):
    # 파일에서 API 키 읽기
    try:
        with (open(key_file_path, 'r') as file):
            session = file.read()
            google_api_key, google_cse_id = session.split(";")
            os.environ["GOOGLE_API_KEY"] = google_api_key
            os.environ["GOOGLE_CSE_ID"] = google_cse_id
            return session.split(";")
    except FileNotFoundError:
        if os.path.isabs(key_file_path):
            raise FileNotFoundError(f"key_file_path={key_file_path}")

        parent_path = os.path.join("..", key_file_path)
        with (open(parent_path, 'r') as file):
            session = file.read()
            google_api_key, google_cse_id = session.split(";")
            os.environ["GOOGLE_API_KEY"] = google_api_key
            os.environ["GOOGLE_CSE_ID"] = google_cse_id
            return session.split(";")
