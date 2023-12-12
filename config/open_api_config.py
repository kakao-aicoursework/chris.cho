import openai
import os

def initialize_openai_api(key_file_path = './config/openai_key.txt' ):
    # 파일에서 API 키 읽기
    with open(key_file_path, 'r') as file:
        openai_api_key = file.read().strip()

    # OpenAI 라이브러리에 API 키 설정
    openai.api_key = openai_api_key
    os.environ["OPENAI_API_KEY"] = openai_api_key