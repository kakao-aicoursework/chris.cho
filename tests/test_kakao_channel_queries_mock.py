import unittest
from unittest.mock import Mock
from data.abstract_vector_db_manager import AbstractVectorDBManager
from old.kakao_channel_answer_query_functions import answer_kakao_channel_query  # your_module은 해당 함수가 정의된 모듈

class TestKakaoChannelQueriesMock(unittest.TestCase):

    def setUp(self):
        # Mock 객체 생성
        self.mock_db_manager = Mock(spec=AbstractVectorDBManager)

    def test_answer_query_with_valid_keyword(self):
        # 유효한 키워드로 함수 호출
        self.mock_db_manager.query_data.return_value = {'documents': [['doc1', 'doc2']]}
        result = answer_kakao_channel_query(self.mock_db_manager, keyword='valid_keyword')
        self.assertIn('doc1', result)
        self.assertIn('doc2', result)

    def test_answer_query_with_no_keyword(self):
        # 키워드 없이 함수 호출
        self.mock_db_manager.query_data.return_value = {'documents': [[]]}
        with self.assertRaises(ValueError):
            answer_kakao_channel_query(self.mock_db_manager, keyword='')

    # 여기에 더 많은 테스트 케이스를 추가할 수 있습니다.

if __name__ == '__main__':
    unittest.main()
