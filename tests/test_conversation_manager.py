import unittest
from bot.conversation_manager import ConversationManager

class TestConversationManager(unittest.TestCase):
    def test_conversation_memory_storage(self):
        manager = ConversationManager()

        init_long_term_memory = manager.get_long_term_memory()
        # 최초 기억 메모리의 role이 'system'인지 확인
        self.assertTrue(init_long_term_memory[0]['role'] == 'system')

        # 사용자 입력을 시뮬레이션
        user_input = '안녕하세요, 어떻게 도와드릴까요?'
        response_contents = "성심성의로 대응하겠습니다!"

        # 대화 관리 메서드 호출
        manager.manage_conversation(user_input, response_contents)

        long_term_memory = manager.get_long_term_memory()
        # 장기 기억 메모리에 사용자 입력과 응답이 올바르게 저장되었는지 확인
        self.assertTrue(user_input == long_term_memory[1]['content'])
        self.assertTrue(response_contents == long_term_memory[2]['content'])

        # 장기 기억 메모리 업데이트 후에도 최초 기억 메모리의 role이 'system'인지 확인
        self.assertTrue(long_term_memory[0]['role'] == 'system')
        self.assertTrue(3 == len(long_term_memory))


if __name__ == '__main__':
    unittest.main()
