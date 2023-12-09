from collections import deque


class ConversationManager:
    def __init__(self, init_memory = None, max_memory_size=100):
        # 초기 대화 기억, 이 부분은 항상 기억되어야 합니다.
        if init_memory is None:
            self.init_memory = [
                {'role': 'system', 'content': '챗봇 환영 메시지'},
                # 여기에 더 많은 초기 시스템 메시지를 추가할 수 있습니다.
            ]
        else:
            self.init_memory = init_memory

        # 고정된 크기의 장기 기억 메모리 초기화, 여기에는 사용자와 시스템의 대화가 저장됩니다.
        self.long_term_memory = deque(self.init_memory, maxlen=max_memory_size)

    def manage_conversation(self, user_input, response):
        user_context = {'short_term_memory': []}

        # 현재 세션의 대화를 단기 기억에 저장 (user_context에 저장)
        user_context['short_term_memory'].append({
            'role': 'user',
            'content': user_input
        })

        # 응답을 단기 기억에 저장
        user_context['short_term_memory'].append({
            'role': 'assistant',
            'content': response
        })

        # 단기 기억 메모리의 내용을 장기 기억 메모리에 저장
        for message in user_context['short_term_memory']:
            if len(self.long_term_memory) < self.long_term_memory.maxlen or message in self.init_memory:
                self.long_term_memory.append(message)
            else:
                # 오래된 메모리 중 init_memory에 없는 것들만 제거
                self.long_term_memory.popleft()
                self.long_term_memory.append(message)

        # 단기 기억 메모리 초기화
        user_context['short_term_memory'].clear()

        return response

    def get_long_term_memory(self):
        # 장기 기억 메모리 내용을 리스트로 변환하여 반환
        return list(self.long_term_memory)

    def get_max_memory_size(self):
        return self.long_term_memory.maxlen

