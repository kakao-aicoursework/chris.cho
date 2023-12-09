import abc
class AbstractVectorDBManager(abc.ABC):
    '''
    vectorDB와의 상호작용을 관리합니다.
    '''

    @abc.abstractmethod
    def __init__(self, db_name=None):
        raise NotImplementedError

    @abc.abstractmethod
    def insert_data(self, parsed_data):
        raise NotImplementedError

    @abc.abstractmethod
    def query_data(self, query_texts, n_results):
        raise NotImplementedError