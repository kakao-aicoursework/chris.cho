import openai
import json
from bot.abstract_chat_processor import AbstractChatProcessor
from config.open_api_config import initialize_openai_api
initialize_openai_api()

class OpenAIChatProcessor(AbstractChatProcessor):
    def __init__(self, gpt_model, temperature=0.7, max_tokens = 1024, functions = None, available_functions=None):
        self.gpt_model = gpt_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.functions = functions
        self.available_functions = available_functions

    def process_chat(self, message_log, functions=None, function_call=None):
        # 기본 매개변수 설정
        request_params = {
            "model": self.gpt_model,
            "messages": message_log,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        # 'functions' 매개변수 처리
        if functions:
            request_params["functions"] = functions
            request_params["function_call"] = 'auto' if function_call is None else function_call
        elif self.functions:
            request_params["functions"] = self.functions
            request_params["function_call"] = 'auto' if function_call is None else function_call

        # API 호출
        response = openai.ChatCompletion.create(**request_params)
        return response

    def process_chat_with_function(self, message_log, functions=None, function_call='auto', DETAIL_DEBUG=True):
        response = self.process_chat(message_log, functions, function_call)
        response_message = response["choices"][0]["message"]
        # 함수 호출 처리
        if not response_message.get("function_call"):
            if DETAIL_DEBUG:
                print(
                    f"[*] not function call!!! response_message_len = {len(response_message['content'])}\n content={response_message['content']}")

            return response, False, None
        else:
            function_name = response_message["function_call"]["name"]
            if DETAIL_DEBUG:
                print(f"[***] <function_call({function_name}) !!!!")

            function_to_call = self.available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            try:
                function_response = function_to_call(**function_args)
            except ValueError as err:
                print(f"ValueError({str(err)})")
                function_response = ""

            if DETAIL_DEBUG:
                print(f"[***] <function_call({function_name}), result len = {len(function_response)}>\n function_response={function_response}\n************* <function_call result len = {len(function_response)}/>")

            # 함수 응답을 대화에 추가
            message_log.append(response_message)
            message_log.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )

            # 두 번째 응답 생성
            second_response = openai.ChatCompletion.create(
                model=self.gpt_model,
                messages=message_log,
            )
            return second_response, True, function_name


