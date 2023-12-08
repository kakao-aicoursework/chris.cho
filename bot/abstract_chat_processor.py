from abc import ABC, abstractmethod

class AbstractChatProcessor(ABC):
    """
    챗봇 프로세서를 위한 추상 기본 클래스.
    이 클래스는 모든 챗봇 프로세서가 따라야 하는 기본 인터페이스를 정의합니다.
    """

    @abstractmethod
    def process_chat(self, message_log):
        """
        주어진 메시지 로그를 처리하고 적절한 응답을 반환합니다.
        모든 하위 클래스는 이 메서드를 구현해야 합니다.

        :param message_log: 사용자의 메시지 로그
        :return: 처리된 응답
        """
        pass
