from collections import deque


class ConversationManager:
    def __init__(self, init_memory = None, max_memory_size=100, init_preserve_count=3):
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
        self.init_preserve_count = init_preserve_count

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
            if not self.is_important_message(message):
                continue

            if len(self.long_term_memory) < self.long_term_memory.maxlen or message in self.init_memory:
                self.long_term_memory.append(message)
            else:
                # long_term_memory가 가득 차 있고, message가 init_memory에 없는 경우
                # 첫 두 개를 제외하고 가장 오래된 메시지부터 제거
                temp = list(self.long_term_memory)[:self.init_preserve_count]  # 처음 두 메시지 보존
                self.long_term_memory.clear()  # long_term_memory 초기화
                self.long_term_memory.extend(temp)  # 처음 두 메시지 다시 추가
                self.long_term_memory.append(message)  # 새 메시지 추가

        # 단기 기억 메모리 초기화
        user_context['short_term_memory'].clear()

        return response

    def is_important_message(self, message):
        # 여기서 중요한 메시지를 식별하는 로직을 추가할 수 있습니다.
        # 예: 특정 키워드가 포함된 메시지, 사용자의 질문 등
        # 현재 예시에서는 모든 메시지를 중요하다고 가정합니다.
        return True

    def get_long_term_memory(self):
        # 장기 기억 메모리 내용을 리스트로 변환하여 반환
        return list(self.long_term_memory)

    def get_max_memory_size(self):
        return self.long_term_memory.maxlen

    '''
    def get_total_conetent_len(self):
        total = 0
        for message in list(self.long_term_memory):
            total+=message['content']

        return total
    '''
    def get_total_content_len(self):
        return sum(len(message['content']) for message in self.long_term_memory)




