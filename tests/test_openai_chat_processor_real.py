import unittest
import timeit

from bot.openai_chat_processor import OpenAIChatProcessor
from data.db_initializer import init_database


class TestOpenAIChatProcessorReal(unittest.TestCase):
    def setUp(self):
        init_database()
        self.processor = OpenAIChatProcessor("gpt-3.5-turbo")  # 실제 모델 이름으로 대체

    def test_process_chat_real(self):
        # 실제 데이터로 process_chat 메서드 테스트
        message_log = [{'role': 'user', 'content': '안녕하세요'}]
        response = self.processor.process_chat(message_log)
        self.assertIsNotNone(response)
        self.assertIn('choices', response) #'choices' in response

    def test_process_chat_with_function_call(self):
        from functions import garbage_weather_functions

        # function_call을 사용하는 테스트
        message_log = [garbage_weather_functions.default_message_log_dict]
        self.processor = OpenAIChatProcessor("gpt-3.5-turbo",
                                             functions=garbage_weather_functions.functions,
                                             available_functions=garbage_weather_functions.available_functions)  # 실제 모델 이름으로 대체

        response, _, _ = self.processor.process_chat_with_function(message_log, functions=garbage_weather_functions.functions)
        print(response.choices[0].message.content)
        self.assertIsNotNone(response)
        self.assertIn('choices', response)
        # 추가적인 검증이 필요할 수 있음

    def test_process_chat_with_function_call_execution_time(self):
        # test_process_chat_with_function_call 함수의 실행 시간 측정
        from functions import garbage_weather_functions

        processor = OpenAIChatProcessor("gpt-3.5-turbo",
                                        functions=garbage_weather_functions.functions,
                                        available_functions=garbage_weather_functions.available_functions)  # 실제 모델 이름으로 대체

        def test_function():
            message_log = [garbage_weather_functions.default_message_log_dict]
            response, _, _= processor.process_chat_with_function(message_log,
                                                               functions=garbage_weather_functions.functions)
            assert response is not None
            assert 'choices' in response

        average_time, num_runs = measure_time(test_function)
        print(
            f"[num_runs={num_runs}] Average execution time for test_process_chat_with_function_call: {average_time} seconds")

    def test_kakao_channel_simple_query(self):
        from functions import simple_kakao_channel_guides_functions

        # function_call을 사용하는 테스트
        message_log = [simple_kakao_channel_guides_functions.default_message_log_dict_rev]
        self.processor = OpenAIChatProcessor("gpt-3.5-turbo",
                                             functions=simple_kakao_channel_guides_functions.functions,
                                             available_functions=simple_kakao_channel_guides_functions.available_functions)  # 실제 모델 이름으로 대체

        response, _, _= self.processor.process_chat_with_function(message_log, functions=simple_kakao_channel_guides_functions.functions)

        print(f"[input] message_log=", message_log)
        print(f"[output] simple_kakao_channel_guides_functions_anwer=", response.choices[0].message.content)

        self.assertIsNotNone(response)
        self.assertIn('choices', response)

def measure_time(function, *args, **kwargs):
    # 주어진 함수를 실행하고 실행 시간을 측정하는 함수
    total_time = 0
    num_runs = 3  # 테스트를 3회 실행
    for _ in range(num_runs):
        start_time = timeit.default_timer()
        function(*args, **kwargs)
        end_time = timeit.default_timer()
        total_time += (end_time - start_time)
    average_time = total_time / num_runs
    return average_time, num_runs

if __name__ == '__main__':
    unittest.main()
