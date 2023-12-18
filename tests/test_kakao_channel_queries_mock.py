import unittest
from unittest.mock import Mock
from data.abstract_vector_db_manager import AbstractVectorDBManager
from functions.simple_kakao_channel_guides_functions import get_kakao_channel_info # your_module은 해당 함수가 정의된 모듈

class TestKakaoChannelQueriesMock(unittest.TestCase):

    def test_answer_query_with_valid_keyword(self):
        # 유효한 키워드로 함수 호출
        result = get_kakao_channel_info(topic='카카오 채널')
        self.assertIn('채널', result)
        self.assertIn('카카오', result)

    def test_answer_query_with_no_keyword(self):
        # 키워드 없이 함수 호출
        with self.assertRaises(ValueError):
            get_kakao_channel_info(topic='')

    # 여기에 더 많은 테스트 케이스를 추가할 수 있습니다.

if __name__ == '__main__':
    unittest.main()
