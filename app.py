import time

from ui.chat_interface import ChatInterface
from config.open_api_config import initialize_openai_api
from bot.openai_chat_processor import OpenAIChatProcessor
# OpenAI API 초기화
initialize_openai_api()

def init_chat_processor(gpt_model = "gpt-3.5-turbo"):
    from functions import simple_kakao_channel_guides_functions as function_module

    # function_call을 사용하는 테스트
    #message_log = function_module.default_message_log
    # chat_processor = OpenAIChatProcessor("gpt-3.5-turbo")
    chat_processor = OpenAIChatProcessor(gpt_model,
                                         functions=function_module.functions,
                                         available_functions=function_module.available_functions)  # 실제 모델 이름으로 대체

    return chat_processor

def init_database(local_path_path = './input/project_data_카카오톡채널.txt'):
    import os
    from data.data_parser import DataParser
    from data.chroma_db_manager import ChromaVectorDBManager

    # 환경 변수 설정
    os.environ['ALLOW_RESET'] = 'True'

    db_manager = ChromaVectorDBManager('sample_kakao_channel_guides')
    db_manager.reset()
    db_manager.get_or_create_collection('sample_kakao_channel_guides')

    parsed_data = DataParser().parse_file_for_kakao_guide_text(local_path_path)
    db_manager.insert_data(parsed_data)
    return db_manager

# 비즈니스 로직을 별도의 함수로 정의
def process_user_input(user_input, callback, DEBUG=False):
    # 여기서 비동기적으로 처리 로직을 수행
    from functions import simple_kakao_channel_guides_functions as function_module

    message_log = []
    message_log.append(function_module.default_system_log_dict)
    message_log.append({'role': 'user', 'content': f'{user_input}'})

    if DEBUG:
        start_time = time.time()


    (response,
     is_function_call_enabled,
     function_name) = chat_processor.process_chat_with_function(message_log)

    if DEBUG:
        dur_time_sec = round(time.time() - start_time, 1)
    else:
        dur_time_sec = None

    callback(response, is_function_call_enabled, dur_time_sec, DEBUG)

# ChatInterface에서 사용할 콜백 함수
def on_send(user_input):
    global chat_interface
    def callback(response, is_function_call_enabled, dur_time_sec, DEBUG):
        message = response.choices[0].message.content
        if DEBUG:
            message = (f"[DEBUG] <dur_time_sec={dur_time_sec}>"
                       f"<is_function_call_enabled={is_function_call_enabled}>\n"
                       + message)
            print(f"user_input:{user_input} ==> response_message:{message}")
        else:
            pass

        chat_interface.display_bot_message(message=message)

    chat_interface.show_loading_popup()

    process_user_input(user_input, callback)

    chat_interface.close_loading_popup()


def main():
    global chat_interface, chat_processor, db_manager
    db_manager = init_database()
    chat_processor = init_chat_processor()

    chat_interface = ChatInterface(send_callback=on_send)
    chat_interface.run()

if __name__ == "__main__":
    main()