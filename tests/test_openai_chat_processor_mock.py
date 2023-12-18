import unittest
from unittest.mock import patch
from bot.openai_chat_processor import OpenAIChatProcessor

class TestOpenAIChatProcessorMock(unittest.TestCase):
    def setUp(self):
        self.processor = OpenAIChatProcessor("test-model", 0.7)

    @patch('openai.ChatCompletion.create')
    def test_process_chat_default(self, mock_create):
        # OpenAI API 호출 모의 설정 (기본값 사용)
        mock_create.return_value = {'choices': [{'text': '테스트 응답 (기본값)'}]}
        message_log = [{'role': 'user', 'content': '테스트 메시지'}]

        # process_chat 메서드 테스트 (기본값 사용)
        response = self.processor.process_chat(message_log)
        mock_create.assert_called_once()
        self.assertEqual(response['choices'][0]['text'], '테스트 응답 (기본값)')


if __name__ == '__main__':
    unittest.main()
