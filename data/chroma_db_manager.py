import chromadb

from data.abstract_vector_db_manager import AbstractVectorDBManager

class ChromaVectorDBManager(AbstractVectorDBManager):
    def __init__(self):
        self.client = chromadb.PersistentClient()

    def create_db(self, db_name, metadata=None):
        self.client.get_or_create_collection(name=db_name, metadata=metadata)

    def get_row_count(self, db_name):
        collection = self.client.get_collection(db_name)
        return collection.count()

    def delete_db(self, db_name):
        self.client.delete_collection(name=db_name)


    def insert_data(self, db_name, parsed_data):
        '''
        파싱된 데이터를 vectorDB에 삽입합니다.
        '''
        documents, ids, metadatas = parsed_data

        collection = self.client.get_collection(db_name)
        if metadatas is None:
            collection.add(documents=documents,
                   ids=ids)
        else:
            collection.add(documents=documents,
                   metadatas=metadatas,
                   ids=ids)


    def query_vector(self, db_name, query_texts, n_results=10):
        '''
        벡터를 기반으로 데이터를 조회합니다.
        '''
        collection = self.client.get_collection(db_name)
        return collection.query(query_texts=query_texts, n_results=n_results)
