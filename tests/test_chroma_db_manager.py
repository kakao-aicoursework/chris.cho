import unittest
import pandas as pd

from data.chroma_db_manager import ChromaVectorDBManager

class TestVectorDBManager(unittest.TestCase):

    def setUp(self):
        # 테스트를 위한 VectorDBManager 인스턴스 초기화
        self.vector_db_manager = ChromaVectorDBManager()
        self.vector_db_manager.get_or_create_collection('kdrama')




    def test_insert_data(self):
        # input_path = "/content/drive/MyDrive/datas/kdrama.csv"
        input_path = "../input/kdrama.csv"

        df = pd.read_csv(input_path)

        test_df = df.drop(["Aired Date", "Aired On", "Duration", "Content Rating", "Production companies", "Rank"],
                               axis=1)

        ids = []
        doc_meta = []
        documents = []
        for i, row in test_df.iterrows():
            row_name = row['Name']

            unique_id = row_name.lower().replace(' ', '-')

            document = f"{row_name}: {str(row['Cast']).strip().lower()} : {str(row['Genre']).strip().lower()}"
            meta = {
                "rating": row['Rating']
            }

            ids.append(unique_id)
            doc_meta.append(meta)
            documents.append(document)

        parsed_data = documents, ids, None

        # 데이터 삽입 시도
        self.vector_db_manager.insert_data(parsed_data, 'kdrama')

        row_count = self.vector_db_manager.get_row_count('kdrama')

        # 삽입 결과가 성공적인지 확인
        self.assertTrue(row_count == len(documents))


    def test_query_vector(self):
        # 쿼리할 벡터
        test_query_vector = ["romantic comedy drama"]

        # 벡터 쿼리 시도
        results = self.vector_db_manager.query_data(test_query_vector, 'kdrama', )
        # 결과가 예상대로 나오는지 확인
        self.assertIsNotNone(results)
        self.assertIsInstance(results, dict)



if __name__ == '__main__':
    unittest.main()
