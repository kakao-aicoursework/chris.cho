import time

from ui.chat_interface import ChatInterface
from config.open_api_config import initialize_openai_api
#from bot.openai_chat_processor import OpenAIChatProcessor
from bot.openai_chat_processor_llm import OpenAIChatProcessorLanChain as OpenAIChatProcessor
from bot.conversation_manager import ConversationManager
# OpenAI API 초기화
initialize_openai_api()

import os
# 환경 변수 설정
os.environ['ALLOW_RESET'] = 'True'


def init_chat_processor_and_conversation_manager(gpt_model ="gpt-3.5-turbo"):
    from functions import garbage_weather_functions as function_module
    functions = []
    available_functions = {}
    init_memory = []

    for db_name in ['sample_kakao_channel_guides', 'sample_kakao_sync_guides']:
        if db_name == 'sample_kakao_sync_guides':
            from functions import simple_kakao_sync_guides_functions as function_module
        elif db_name == 'sample_kakao_channel_guides':
            from functions import simple_kakao_channel_guides_functions as function_module

        functions += function_module.functions
        available_functions.update(function_module.available_functions)
        #init_memory.append(function_module.default_system_log_dict)
        init_memory = [function_module.default_system_log_dict]

    # 채팅 프로세스초기화
    chat_processor = OpenAIChatProcessor(gpt_model,
                                         functions=functions,
                                         available_functions=available_functions)  # 실제 모델 이름으로 대체

    # 대화 관리자 초기화
    conversation_manager = ConversationManager(init_memory=init_memory)

    return chat_processor, conversation_manager
def old_init_chat_processor_and_conversation_manager(db_name, gpt_model ="gpt-3.5-turbo"):
    if db_name == 'sample_kakao_sync_guides':
        from functions import simple_kakao_sync_guides_functions as function_module
    elif db_name == 'sample_kakao_channel_guides':
        from functions import simple_kakao_channel_guides_functions as function_module
    else:
        raise ValueError(f"not supported db_name={db_name}")

    # 채팅 프로세스초기화
    chat_processor = OpenAIChatProcessor(gpt_model,
                                         functions=function_module.functions,
                                         available_functions=function_module.available_functions)  # 실제 모델 이름으로 대체

    # 대화 관리자 초기화
    conversation_manager = ConversationManager(init_memory=[function_module.default_system_log_dict])

    return chat_processor, conversation_manager


def init_database():
    from data.data_parser import DataParser
    from data.chroma_db_manager import ChromaVectorDBManager

    db_manager = ChromaVectorDBManager()
    for db_name, local_path_path in zip(['sample_kakao_sync_guides', 'sample_kakao_channel_guides'],
                                        ['./input/project_data_카카오싱크.txt', './input/project_data_카카오톡채널.txt']):

        db_manager.init_and_get_create_collection(db_name)
        parsed_data = DataParser().parse_file_for_kakao_guide_text(local_path_path)
        db_manager.insert_data(parsed_data)

    return db_manager

# 비즈니스 로직을 별도의 함수로 정의
def process_user_input(user_input, callback, DEBUG=True, DETAIL_DEBUG=True):
    # 여기서 비동기적으로 처리 로직을 수행
    from functions import simple_kakao_channel_guides_functions as function_module

    # 단기 기억 메모리 설정
    message_log = conversation_manager.get_long_term_memory()

    if DEBUG:
        max_size = conversation_manager.get_max_memory_size()
        debug_message = (f"[DEBUG] <long_term_memory_queue_size (cur/max)={len(message_log)}/{max_size}>\n")
        if DETAIL_DEBUG:#get_total_content_len
            debug_message += (f"[DETAIL_DEBUG] <total_message_len={conversation_manager.get_total_content_len()}>"
                              f"[DETAIL_DEBUG] get_long_term_memory <message_log={message_log}>\n")
    else:
        pass

    message_log.append({'role': 'user', 'content': f'{user_input}'})

    if DEBUG:
        start_time = time.time()

    (response,
     is_function_call_enabled,
     function_name) = chat_processor.process_chat_with_function(message_log)

    if DEBUG:
        dur_time_sec = round(time.time() - start_time, 1)
        debug_message += (f"[DEBUG] <dur_time_sec={dur_time_sec}>\n"
                         f"[DEBUG] <is_function_call_enabled={is_function_call_enabled}>\n"
                         f"[DEBUG] <function_name={function_name}>\n"
                         f"\n")
    else:
        debug_message = None

    response_content = callback(response, debug_message, DEBUG)
    conversation_manager.manage_conversation(user_input, response_content)

# ChatInterface에서 사용할 콜백 함수
def on_send(user_input):
    global chat_interface
    def callback(response, debug_message, DEBUG):
        response_message = response['choices'][0]['message']
        message_content = response_message['content']
        if DEBUG:
            bot_message = (f"{debug_message}" + message_content)
            print(f"user_input:{user_input} ==> response_message_content:{message_content}")
        else:
            bot_message = message_content

        chat_interface.display_bot_message(message=bot_message)
        return message_content

    chat_interface.show_loading_popup()

    process_user_input(user_input, callback)

    chat_interface.close_loading_popup()


def main():
    global chat_interface, chat_processor, db_manager, conversation_manager
    db_manager = init_database()
    (chat_processor,
     conversation_manager) = init_chat_processor_and_conversation_manager()

    chat_interface = ChatInterface(send_callback=on_send)
    chat_interface.run()

if __name__ == "__main__":
    main()