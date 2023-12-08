import unittest
import json

from config.open_api_config import initialize_openai_api
from bot.openai_chat_processor import OpenAIChatProcessor
# OpenAI API 초기화
initialize_openai_api(key_file_path = '../config/openai_key.txt' )

class TestOpenAIChatProcessorReal(unittest.TestCase):
    def setUp(self):
        # OpenAI API 키 로드
        self.processor = OpenAIChatProcessor("gpt-3.5-turbo")  # 실제 모델 이름으로 대체

    def test_process_chat_real(self):
        # 실제 데이터로 process_chat 메서드 테스트
        message_log = [{'role': 'user', 'content': '안녕하세요'}]
        response = self.processor.process_chat(message_log)
        self.assertIsNotNone(response)
        self.assertIn('choices', response) #'choices' in response

    def test_process_chat_with_function_call(self):
        from functions import garbage_weather_functions

        # function_call을 사용하는 테스트
        message_log = [garbage_weather_functions.default_message_log_dict]
        self.processor = OpenAIChatProcessor("gpt-3.5-turbo",
                                             functions=garbage_weather_functions.functions,
                                             available_functions=garbage_weather_functions.available_functions)  # 실제 모델 이름으로 대체

        response = self.processor.process_chat_with_function(message_log, functions=garbage_weather_functions.functions)
        print(response.choices[0].message.content)
        self.assertIsNotNone(response)
        self.assertIn('choices', response)
        # 추가적인 검증이 필요할 수 있음

if __name__ == '__main__':
    unittest.main()
