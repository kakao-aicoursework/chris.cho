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
                 init_memory=None):
        self.gpt_model = gpt_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.functions = functions
        self.available_functions = available_functions

        self.llm = ChatOpenAI(model_name=self.gpt_model,
                              temperature=self.temperature,
                              max_tokens=self.max_tokens)

        self.init_llm_chain(init_memory)
        template_path_list = [
            './functions/prompt_template/simple_kakao_sync_guides/1_parse_input.txt',
            './functions/prompt_template/simple_kakao_sync_guides/2_parse_user_input.txt',
            './functions/prompt_template/simple_kakao_sync_guides/3_answer_output.txt'
        ]
        self.init_real_llm_chain(template_path_list)

    def read_prompt_template(self, file_path: str) -> str:
        with open(file_path, "r") as f:
            prompt_template = f.read()

        return prompt_template

    def init_real_llm_chain(self, template_path_list):
        self.llm_dict = {}
        output_key_list = ['in','keywords', 'final_context']
        for i, template_path in enumerate(template_path_list):

            dirname, basename = os.path.split(template_path)
            name, ext = os.path.splitext(basename)
            #output_key = name
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
                self.llm_dict['in'],
                self.llm_dict['keywords']
            ],
            input_variables=["tag", "user_input"],
            output_variables=["keywords"],
            verbose=True,
        )
        self.answer_llm = self.llm_dict['final_context']




    def init_llm_chain(self, init_memory):
        role = init_memory[0]['role']
        if role.lower() != 'system':
            raise ValueError(f"role={role}")

        content = init_memory[0]['content']

        system_message_prompt = SystemMessage(content=content)

        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt,
                                                        human_message_prompt])

        chain = LLMChain(llm=self.llm, prompt=chat_prompt)
        self.chain = chain

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
        input_text = self.convert_input_to_txt(message_log)

        context = dict(tag="카카오톡 싱크",
                       user_input = input_text)
        context = self.preprocess_chain(context)
        if 'NONE' in context['keywords']:
            response_text = self.answer_llm(context)
            return self.convert_result_txt_to_response(response_text['final_context'])
        else:
            return self.convert_result_txt_to_response(response_text['final_context'], is_function=True)

    def convert_input_to_txt(self, message_log):
        input_text = ""
        for message_dict in message_log:
            if message_dict['role'].lower() == 'system':
                continue

            input_text += f"{message_dict['content']}\n"
        return input_text

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


