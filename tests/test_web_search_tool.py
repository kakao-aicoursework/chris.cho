import unittest
from utils.web_search_tool import query_web_search
from bot.langchain_chat_processor import LanChainChatProcessor
from config import open_api_config

open_api_config.initialize_openai_api(key_file_path = '../config/openai_key.txt')
class TestWebSearchTool(unittest.TestCase):
    def setUp(self):
        # OpenAI API 키 로드
        self.processor = LanChainChatProcessor("gpt-3.5-turbo")  # 실제 모델 이름으로 대체

    def test_query_result(self):
        # 테스트를 위한 더미 함수를 정의합니다.
        user_message = "Obama's first name?"
        # 실제 웹 검색 도구를 사용하지 않고, 예상 결과를 모의합니다.
        expected_result = "Barack"
        # query_web_search 함수의 결과를 확인합니다.
        result = query_web_search(self.processor, user_message)
        # 결과가 예상과 일치하는지 확인합니다.
        self.assertTrue(expected_result in result)

# 유닛 테스트를 실행합니다.
if __name__ == '__main__':
    unittest.main()
