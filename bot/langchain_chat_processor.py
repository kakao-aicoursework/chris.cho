import json

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)


from bot.abstract_chat_processor import AbstractChatProcessor
from config.open_api_config import initialize_openai_api
from utils import io_util

initialize_openai_api()


_DEBUG_MODE=False #디버그 정보 표시 유무
class LanChainChatProcessor(AbstractChatProcessor):
    def __init__(self, gpt_model,
                 temperature=0.1,
                 max_tokens=2048,
                 functions=None,
                 available_functions=None,
                 init_memory=None,
                 init_tag = None):

        self.gpt_model = gpt_model
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.init_concept = init_tag
        self.functions = functions
        self.available_functions = available_functions

        self.llm = ChatOpenAI(model_name=self.gpt_model,
                              temperature=self.temperature,
                              max_tokens=self.max_tokens)


        template_prompt_path_dict = {
            #'intent': 'prompt_template/misson2/0_intent_list.txt',
            'extract_keywords': 'prompt_template/misson2/1_parse_input.txt',
            'result_answer': 'prompt_template/misson2/2_answer_final_output.txt',
            'default_answer': 'prompt_template/misson2/2_answer_default_output.txt',
            'is_vaild_search_result': 'prompt_template/misson3/search_value_check.txt',
            'compressed_search_result': 'prompt_template/misson3/search_compress.txt',
            'chat_compression' : 'prompt_template/misson3/chat_compress_summary.txt'
        }

        self.extract_keywords_chain = self.create_chain(
            llm=self.llm, template_path=template_prompt_path_dict['extract_keywords'], output_key="extract_keywords"
        )
        self.result_answer_chain = self.create_chain(
            llm=self.llm, template_path=template_prompt_path_dict['result_answer'], output_key="result_answer"
        )
        self.default_answer_chain = self.create_chain(
            llm=self.llm, template_path=template_prompt_path_dict['default_answer'], output_key="result_answer"
        )

        self.answer_compression_chain = self.create_chain(
            llm=self.llm,
            template_path=template_prompt_path_dict['chat_compression'],
            output_key="comp_result_answer",
        )

        self.search_value_check_chain = self.create_chain(
            llm=self.llm,
            template_path=template_prompt_path_dict['is_vaild_search_result'],
            output_key="output",
        )

        self.search_compression_chain = self.create_chain(
            llm=self.llm,
            template_path=template_prompt_path_dict['compressed_search_result'],
            output_key="output",
        )
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
        (user_message,
         chat_history) = self.convert_message_log_to_text(message_log)

        context = dict(tag=self.init_concept,
                       user_message = user_message,
                       chat_history = chat_history,
                       functions = request_params["functions"])

        str_extract_keywords = self.extract_keywords_chain.run(context)
        extract_keywords = self.convert_str_to_dict(str_extract_keywords)
        context.update(extract_keywords)

        try:
            if extract_keywords['is_related'] == 0:
                default_answer = self.default_answer_chain(context)
                context.update(default_answer)
                return self.convert_langchaine_to_openai_response(context)
            else:
                return self.convert_langchaine_to_openai_response(context)
        except TypeError as err:
            raise TypeError(f"extract_keywords={extract_keywords}")

    def process_chat_with_function(self,
                                   message_log,
                                   functions=None,
                                   function_call='auto',
                                   DETAIL_DEBUG=_DEBUG_MODE):
        response = self.process_chat(message_log, functions, function_call)
        context_dict = response['context']

        response_message = response["choices"][0]["message"]
        # 함수 호출 처리
        try:
            if not response_message.get("function_call"):
                if DETAIL_DEBUG:
                    print(
                        f"[*] not function call!!! response_message_len = {len(response_message['content'])}\n content={response_message['content']}")

                return response, False, None, context_dict
            else:
                function_name = response_message["function_call"]["name"]
                if DETAIL_DEBUG:
                    print(f"[***] <function_call({function_name}) !!!!")

                function_to_call = self.available_functions[function_name]
                arguments = response_message["function_call"]["arguments"]
                if type(arguments) is str:
                    function_args = json.loads(arguments)
                else:
                    function_args = arguments

                try:
                    function_response = function_to_call(**function_args)
                except ValueError as err:
                    print(f"ValueError({str(err)})")
                    function_response = ""
                    
                if DETAIL_DEBUG:
                    print(
                        f"[***] <function_call({function_name}), result len = {len(function_response)}>\n function_response={function_response}\n************* <function_call result len = {len(function_response)}/>")

                # 함수 응답을 대화에 추가
                context_dict['function_response'] = function_response
                # 두 번째 응답 생성
                response_dict = self.result_answer_chain(context_dict)
                second_response = self.convert_langchaine_to_openai_response(response_dict)

                return second_response, True, function_name, context_dict
        except Exception as err:
            raise err(f"response={response}, context_dict={context_dict}")



    def compress_result_answer(self, chat_context_dict, response_content, min_char_size=32, max_char_size=64):
        if len(response_content) <= min_char_size:
            return response_content

        chat_context_dict['min_char_size'] = min_char_size
        chat_context_dict['max_char_size'] = max_char_size
        chat_context_dict['result_answer'] = response_content
        chat_context_dict = self.answer_compression_chain(chat_context_dict)
        return chat_context_dict['comp_result_answer']

    def create_chain(self, llm, template_path, output_key, verbose=_DEBUG_MODE):
        return LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_template(
                template=self.read_prompt_template(template_path)
            ),
            output_key=output_key,
            verbose=verbose,
        )

    def read_prompt_template(self, file_path: str) -> str:
        prompt_template = io_util.read_file(file_path)
        return prompt_template

    def convert_str_to_dict(self, str_json_result):
        try:
            converted_dict = json.loads(str_json_result)
            return converted_dict
        except json.JSONDecodeError as e:
            raise ValueError(f"str_json_result={str_json_result}(err={str(e)})")


    def convert_message_log_to_text(self, message_log):
        user_message = ""
        chat_history = ""

        input_message_dict = message_log[-1]
        if input_message_dict['role'].lower() == 'user':
            user_message += f"{input_message_dict['content']}\n"
        else:
            pass

        uesr_memory = message_log[:-1]
        for message_dict in uesr_memory:
            if message_dict['role'].lower() == 'system':
                continue

            chat_history += f"{message_dict['content']}\n"


        return user_message, chat_history

    def convert_langchaine_to_openai_response(self, response_dict):
        new_response_dict = {}
        temp_content_dict = {}
        if 'result_answer' in response_dict:
            response_text = response_dict['result_answer']
            temp_content_dict['content'] = str(response_text)
        else:
            pass

        if 'function_call' in response_dict and response_dict['function_call']:
            function_call_data = {'name': response_dict['function_name'],
                                  'arguments': response_dict['arguments']}

            temp_content_dict['function_call'] = function_call_data
            # response_text = f"response_dict={response_dict}"
        else:
            pass

        message_dict = {'message': temp_content_dict}

        new_response_dict['choices'] = [
            message_dict
        ]
        new_response_dict['context'] = response_dict
        return new_response_dict