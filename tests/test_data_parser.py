import unittest
from data.data_parser import DataParser
from data.chroma_db_manager import ChromaVectorDBManager
class TestDataParser(unittest.TestCase):

    def setUp(self):
        # 테스트에 필요한 DataParser 인스턴스를 초기화
        self.parser = DataParser()
        self.vector_db_manager = ChromaVectorDBManager()
        self.vector_db_manager.create_db('test_data_parser')

    def test_parse_valid_file_kakaotalk_channel(self):
        # 유효한 파일을 파싱하는 경우의 테스트
        valid_file_path = '../input/project_data_카카오톡채널.txt'
        parsed_data = self.parser.parse_file_for_kakao_channel(valid_file_path)
        self.vector_db_manager.insert_data(parsed_data)
        self.assertIsNotNone(parsed_data)
        # 추가적인 검증 로직 필요

    def test_parse_invalid_file_kakaotalk_channel(self):
        # 유효하지 않은 파일을 파싱하는 경우의 테스트
        invalid_file_path = 'path/to/invalid_data_file.txt'
        with self.assertRaises(Exception):
            self.parser.parse_file_for_kakao_channel(invalid_file_path)

    def test_parse_empty_file_kakaotalk_channel(self):
        # 비어있는 파일을 파싱하는 경우의 테스트
        empty_file_path = '../input/empty_data_file.txt'
        parsed_data = self.parser.parse_file_for_kakao_channel(empty_file_path)
        self.assertEqual(parsed_data, (None, None, None))
        # 또는 다른 예상 결과에 따른 검증 로직

    # 필요에 따라 추가 테스트 케이스 작성

if __name__ == '__main__':
    unittest.main()
