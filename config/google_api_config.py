import os
from utils import io_util

def initialize_google_api(key_file_path = 'config/google_key.txt'):
    session = io_util.read_file(key_file_path)
    google_api_key, google_cse_id = session.split(";")
    os.environ["GOOGLE_API_KEY"] = google_api_key
    os.environ["GOOGLE_CSE_ID"] = google_cse_id

