import unittest
from data.chroma_db_manager import ChromaVectorDBManager
from data.data_parser import DataParser
from functions.simple_kakao_channel_guides_functions import get_kakao_channel_info

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
        result = get_kakao_channel_info(topic='카카오톡 채널이 무엇인가요?')
        self.assertTrue('채널' in result)

    def test_answer_query_with_no_keyword(self):
        # 키워드 없이 함수 호출
        with self.assertRaises(ValueError):
            get_kakao_channel_info(topic='')

    def test_answer_query_with_invalid_keyword(self):
        # 잘못된 키워드로 함수 호출
        with self.assertRaises(ValueError):
            result = get_kakao_channel_info(topic=None)

    def test_answer_query_with_empty_database(self):
        # 데이터베이스가 비어있는 경우
        try:
            self.vector_db_manager.delete_collection('sample_kakao_channel_guides')
        except ValueError:
            pass
        with self.assertRaises(ValueError):
            result = get_kakao_channel_info(topic='카카오톡 채널 관련 정보')



if __name__ == '__main__':
    unittest.main()
