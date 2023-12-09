import unittest
from data.chroma_db_manager import ChromaVectorDBManager
from data.data_parser import DataParser
from old.kakao_channel_answer_query_functions import answer_kakao_channel_query

class TestKakaoChannelQueriesReal(unittest.TestCase):
    def setUp(self):
        # 데이터베이스 매니저 초기화
        self.vector_db_manager = ChromaVectorDBManager()
        self.vector_db_manager.init_and_get_create_collection('sample_kakao_channel_guides')


        # 유효한 파일 경로에서 데이터 파싱 및 삽입
        self.parser = DataParser()
        valid_file_path = '../input/project_data_카카오톡채널.txt'
        parsed_data = self.parser.parse_file_for_kakao_guide_text(valid_file_path)
        self.vector_db_manager.insert_data(parsed_data)

    def test_answer_query_with_valid_keyword(self):
        # 유효한 키워드로 함수 호출
        result = answer_kakao_channel_query(self.vector_db_manager, keyword='카카오톡 채널이 무엇인가요?')
        self.assertTrue('채널' in result)

    def test_answer_query_with_no_keyword(self):
        # 키워드 없이 함수 호출
        with self.assertRaises(ValueError):
            answer_kakao_channel_query(self.vector_db_manager, keyword='')

    def test_answer_query_with_invalid_keyword(self):
        # 잘못된 키워드로 함수 호출
        result = answer_kakao_channel_query(self.vector_db_manager, keyword='invaild')
        self.assertEqual(result, 'No relevant documents found.')

    def test_answer_query_with_empty_database(self):
        # 데이터베이스가 비어있는 경우
        try:
            self.vector_db_manager.init_and_get_create_collection('empty')
        except ValueError:
            pass
        with self.assertRaises(ValueError):
            result = answer_kakao_channel_query(self.vector_db_manager, keyword='카카오톡 채널 관련 정보')



if __name__ == '__main__':
    unittest.main()
