import chromadb

from data.abstract_vector_db_manager import AbstractVectorDBManager

class ChromaVectorDBManager(AbstractVectorDBManager):
    def __init__(self):
        self.client = chromadb.PersistentClient()

    def create_db(self, db_name, metadata=None):
        self.last_accessed_collection = self.client.get_or_create_collection(name=db_name, metadata=metadata)
        return self.last_accessed_collection

    def get_row_count(self, db_name=None):
        if db_name is None:
            return self.last_accessed_collection.count()

        collection = self.client.get_collection(db_name)
        return collection.count()

    def delete_db(self, db_name):
        self.client.delete_collection(name=db_name)


    def insert_data(self, parsed_data, db_name=None):
        '''
        파싱된 데이터를 vectorDB에 삽입합니다.
        '''
        if db_name is None:
            collection = self.last_accessed_collection
        else:
            collection = self.client.get_collection(db_name)

        documents, ids, metadatas = parsed_data
        if metadatas is None:
            collection.add(documents=documents,
                   ids=ids)
        else:
            collection.add(documents=documents,
                   metadatas=metadatas,
                   ids=ids)


    def query_vector(self, query_texts, db_name=None, n_results=10):
        '''
        벡터를 기반으로 데이터를 조회합니다.
        '''
        if db_name is None:
            collection = self.last_accessed_collection
        else:
            collection = self.client.get_collection(db_name)

        return collection.query(query_texts=query_texts, n_results=n_results)
