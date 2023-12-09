import unittest

from config.open_api_config import initialize_openai_api
from bot.openai_chat_processor import OpenAIChatProcessor
from data.chroma_db_manager import ChromaVectorDBManager
from old.kakao_channel_answer_query_functions import answer_kakao_channel_query

# OpenAI API 초기화
initialize_openai_api(key_file_path='../config/openai_key.txt')

class TestKakaoChannelQueriesReal(unittest.TestCase):
    def setUp(self):
        # OpenAI API 키 로드
        self.processor = OpenAIChatProcessor("gpt-3.5-turbo")  # 실제 모델 이름으로 대체
        self.db_manager = ChromaVectorDBManager()

    def test_answer_query_with_valid_keyword(self):
        # 유효한 키워드로 함수 호출
        self.db_manager.query_data.return_value = {'documents': [['doc1', 'doc2']]}
        result = answer_kakao_channel_query(self.db_manager, keyword='valid_keyword')
        self.assertIn('doc1', result)
        self.assertIn('doc2', result)

    def test_answer_query_with_no_keyword(self):
        # 키워드 없이 함수 호출
        self.db_manager.query_data.return_value = {'documents': [[]]}
        with self.assertRaises(ValueError):
            answer_kakao_channel_query(self.db_manager, keyword='')
    def test_kakao_channel_general_query(self):
        # 일반적인 '카카오톡 채널' 관련 질문
        message_log = [{'role': 'user', 'content': '카카오톡 채널이 무엇인가요?'}]
        response = self.processor.process_chat(message_log)
        self.assertIsNotNone(response)
        self.assertIn('choices', response)

    def test_kakao_channel_specific_query(self):
        # 특정 기능에 관한 '카카오톡 채널' 질문
        message_log = [{'role': 'user', 'content': '카카오톡 채널 API는 어떻게 사용하나요?'}]
        response = self.processor.process_chat(message_log)
        self.assertIsNotNone(response)
        self.assertIn('choices', response)

    def test_kakao_channel_negative_query(self):
        # 부정적인 문맥에서의 '카카오톡 채널' 질문
        message_log = [{'role': 'user', 'content': '카카오톡 채널을 사용하지 않으면 어떤 불이익이 있나요?'}]
        response = self.processor.process_chat(message_log)
        self.assertIsNotNone(response)
        self.assertIn('choices', response)

    # 여기에 더 많은 테스트 케이스를 추가할 수 있습니다.

if __name__ == '__main__':
    unittest.main()
