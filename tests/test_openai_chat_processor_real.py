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

        response, _ = self.processor.process_chat_with_function(message_log, functions=garbage_weather_functions.functions)
        print(response.choices[0].message.content)
        self.assertIsNotNone(response)
        self.assertIn('choices', response)
        # 추가적인 검증이 필요할 수 있음

    '''
        def test_kakao_channel_general_query(self):
        from data.chroma_db_manager import ChromaVectorDBManager
        from data.data_parser import DataParser
        from functions import kakao_channel_answer_query_functions

        vector_db_manager = ChromaVectorDBManager()
        vector_db_manager.create_db('sample_kakao_channel_guides')

        # 유효한 파일 경로에서 데이터 파싱 및 삽입
        parser = DataParser()
        valid_file_path = '../input/project_data_카카오톡채널.txt'
        parsed_data = parser.parse_file_for_kakao_channel(valid_file_path)
        vector_db_manager.insert_data(parsed_data)



        # function_call을 사용하는 테스트
        message_log = [kakao_channel_answer_query_functions.default_message_log_dict]
        #message_log = kakao_channel_answer_query_functions.default_init_message_log

        self.processor = OpenAIChatProcessor("gpt-3.5-turbo",
                                             functions=kakao_channel_answer_query_functions.functions,
                                             available_functions=kakao_channel_answer_query_functions.available_functions)  # 실제 모델 이름으로 대체

        response = self.processor.process_chat_with_function(message_log, functions=kakao_channel_answer_query_functions.functions)
        print(response.choices[0].message.content)
        self.assertIsNotNone(response)
        self.assertIn('choices', response)
       
    '''

    def test_kakao_channel_simple_query(self):
        from functions import simple_kakao_channel_guides_functions

        # function_call을 사용하는 테스트
        message_log = [simple_kakao_channel_guides_functions.default_message_log_dict_rev]
        self.processor = OpenAIChatProcessor("gpt-3.5-turbo",
                                             functions=simple_kakao_channel_guides_functions.functions,
                                             available_functions=simple_kakao_channel_guides_functions.available_functions)  # 실제 모델 이름으로 대체

        response, _, _= self.processor.process_chat_with_function(message_log, functions=simple_kakao_channel_guides_functions.functions)

        print(f"[input] message_log=", message_log)
        print(f"[output] simple_kakao_channel_guides_functions_anwer=", response.choices[0].message.content)

        self.assertIsNotNone(response)
        self.assertIn('choices', response)

if __name__ == '__main__':
    unittest.main()
