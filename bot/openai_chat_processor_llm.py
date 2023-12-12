from langchain.llms import OpenAI
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import SystemMessage

#enc = tiktoken.encoding_for_model("gpt-3.5-turbo")


class OpenAIChatProcessorLanChain:
    def __init__(self, gpt_model, temperature=0.7, max_tokens=1024, functions=None, available_functions=None):
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
        openai = ChatOpenAI(model_name=request_params['model'],
            temperature=request_params['temperature'],
            max_tokens=request_params['max_tokens'])

        input_text = self.convert_input_to_txt(message_log)
        response_text = openai.predict(input_text)
        #response = openai.ChatCompletion.create(**request_params)

        return self.convert_result_txt_to_response(response_text)


    def convert_input_to_txt(self, message_log):
        input_text = ""
        for message_dict in message_log:
            input_text += f"<role>{message_dict['role']}</role>\n"
            input_text += f"<prompt>{message_dict['content']}</prompt>\n\n"
        return input_text

    def convert_result_txt_to_response(self, response_text):
        response = {}
        content_dict = {'content' : response_text}
        message_dict = {'message': content_dict}

        response['choices'] = [
            message_dict
        ]

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
            function_response = function_to_call(**function_args)
            if DETAIL_DEBUG:
                print(
                    f"[***] <function_call({function_name}), result len = {len(function_response)}>\n function_response={function_response}\n************* <function_call result len = {len(function_response)}/>")

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