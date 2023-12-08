import abc
class AbstractVectorDBManager(abc.ABC):
    '''
    vectorDB와의 상호작용을 관리합니다.
    '''

    @abc.abstractmethod
    def insert_data(self, parsed_data):
        '''
        파싱된 데이터를 vectorDB에 삽입합니다.

        :param parsed_data:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def query_vector(self, vector):
        '''
        벡터를 기반으로 데이터를 조회합니다.

        :param vector:
        :return:
        '''
        raise NotImplementedError