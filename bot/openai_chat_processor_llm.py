import json
import os

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import SystemMessage
from langchain.chains import SequentialChain
#enc = tiktoken.encoding_for_model("gpt-3.5-turbo")


class OpenAIChatProcessorLanChain:
    def __init__(self, gpt_model,
                 temperature=0.7,
                 max_tokens=1024,
                 functions=None,
                 available_functions=None,
                 init_memory=None,
                 init_tag = None):

        self.gpt_model = gpt_model
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.init_concpet = init_tag
        self.functions = functions
        self.available_functions = available_functions

        self.llm = ChatOpenAI(model_name=self.gpt_model,
                              temperature=self.temperature,
                              max_tokens=self.max_tokens)

        template_path_list = [
            './functions/prompt_template/simple_kakao_sync_guides/1_parse_input.txt',
            './functions/prompt_template/simple_kakao_sync_guides/2_answer_output.txt'
        ]
        output_key_list = ['keywords', 'new_user_context']
        self.init_real_llm_chain(template_path_list, output_key_list)

    def init_real_llm_chain(self, template_path_list, output_key_list):
        self.llm_dict = {}
        for i, template_path in enumerate(template_path_list):
            dirname, basename = os.path.split(template_path)
            name, ext = os.path.splitext(basename)
            output_key = output_key_list[i]

            llm_chain = LLMChain(
                llm=self.llm,
                prompt=ChatPromptTemplate.from_template(
                    template=self.read_prompt_template(template_path),
                ),
                output_key=output_key,
                verbose=True,
            )
            self.llm_dict[output_key] = llm_chain

        self.preprocess_chain = SequentialChain(
            chains=[
                self.llm_dict['keywords'],
            ],
            input_variables=["tag", "user_input", "user_context", "functions"],
            output_variables=["keywords"],
            verbose=True,
        )

        self.answer_llm = self.llm_dict['new_user_context']
    def read_prompt_template(self, file_path: str) -> str:
        with open(file_path, "r") as f:
            prompt_template = f.read()

        return prompt_template


    def process_chat(self, message_log, functions=None, function_call=None):
        # 기본 매개변수 설정
        request_params = {
            "model": self.gpt_model,
            "messages": message_log,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        if functions:
            request_params["functions"] = functions
            request_params["function_call"] = 'auto' if function_call is None else function_call
        elif self.functions:
            request_params["functions"] = self.functions
            request_params["function_call"] = 'auto' if function_call is None else function_call

        # API 호출
        (user_input,
         user_context) = self.convert_input_to_txt(message_log)

        context = dict(tag=self.init_concpet,
                       user_input = user_input,
                       user_context = user_context,
                       functions = request_params["functions"])
        context = self.preprocess_chain(context)

        if 'NONE' in context['keywords']:
            context['context'] = user_context
            response_text = self.answer_llm(context)
            return self.convert_result_txt_to_response(response_text['new_user_context']), context
        else:
            return self.convert_result_txt_to_response(context, is_function=True), context

    def convert_input_to_txt(self, message_log):
        user_input = ""
        user_context = ""

        input_message_dict = message_log[-1]
        if input_message_dict['role'].lower() == 'user':
            user_input += f"{input_message_dict['content']}\n"
        else:
            pass

        uesr_memory = message_log[:-1]
        for message_dict in uesr_memory:
            if message_dict['role'].lower() == 'system':
                continue

            user_context += f"{message_dict['content']}\n"


        return user_input, user_context

    def convert_result_txt_to_response(self, response_text, is_function=False):
        response = {}
        content_dict = {'content' : response_text}
        message_dict = {'message': content_dict}

        response['choices'] = [
            message_dict
        ]
        if is_function:
            response['function_call'] = {}


        return response



    def process_chat_with_function(self, message_log, functions=None, function_call='auto', DETAIL_DEBUG=True):
        response, context = self.process_chat(message_log, functions, function_call)
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
            response_text = self.answer_llm(context)
            second_response =  self.convert_result_txt_to_response(response_text['new_user_context'])
            return second_response, True, function_name


