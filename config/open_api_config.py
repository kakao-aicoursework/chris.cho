import openai
import os

def initialize_openai_api(key_file_path = 'config/openai_key.txt' ):
    try:
        with open(key_file_path, 'r') as file:
            openai_api_key = file.read().strip()

        # OpenAI 라이브러리에 API 키 설정
        openai.api_key = openai_api_key
        os.environ["OPENAI_API_KEY"] = openai_api_key
    except FileNotFoundError:
        if os.path.isabs(key_file_path):
            raise FileNotFoundError(f"key_file_path={key_file_path}")

        parent_path = os.path.join("..", key_file_path)
        with open(parent_path, 'r') as file:
            openai_api_key = file.read().strip()

        # OpenAI 라이브러리에 API 키 설정
        openai.api_key = openai_api_key
        os.environ["OPENAI_API_KEY"] = openai_api_key