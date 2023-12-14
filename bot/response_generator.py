import time

#from bot.openai_chat_processor import OpenAIChatProcessor
from bot.langchain_chat_processor import LanChainChatProcessor as ChatProcessor
from bot.conversation_manager import ConversationManager

_DEBUG_MODE=False #디버그 정보(응답시간, 함수명, 함수 호출 여부 등) 표시 유무
_DETAIL_DEBUG_MODE=False #메모리안에 들어 있는 구체적인 내용

def process_user_input(user_input, callback, DEBUG=_DEBUG_MODE, DETAIL_DEBUG=_DETAIL_DEBUG_MODE):
    # 여기서 비동기적으로 처리 로직을 수행
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

    if callback is None:
        response_message = response['choices'][0]['message']
        response_content = response_message['content']
    else:
        response_content = callback(response, debug_message, DEBUG)

    conversation_manager.manage_conversation(user_input, response_content)
    return response_content


def init_chat_processor_and_conversation_manager(gpt_model ="gpt-3.5-turbo"):
    global chat_processor
    global conversation_manager

    (functions,
     available_functions,
     init_memory,
     str_function_concept) = _init_function_call_info(db_name='sample_kakao_sync_guides')
    # 채팅 프로세스초기화

    chat_processor = ChatProcessor(gpt_model,
                                   functions=functions,
                                   available_functions=available_functions,
                                   init_memory=init_memory,
                                   init_tag = str_function_concept)  # 실제 모델 이름으로 대체

    # 대화 관리자 초기화
    conversation_manager = ConversationManager(init_memory=init_memory)

    return chat_processor, conversation_manager

def _init_function_call_info(db_name, is_multi_function=False):
    functions = []
    available_functions = {}
    init_memory = []
    str_function_concept = ""

    if not is_multi_function:
        if db_name == 'sample_kakao_sync_guides':
            from functions import simple_kakao_sync_guides_functions as function_module
        elif db_name == 'sample_kakao_channel_guides':
            from functions import simple_kakao_channel_guides_functions as function_module
        else:
            raise ValueError(f"not supported db_name={db_name}")

        functions = [function_module.functions]
        available_functions.update(function_module.available_functions)
        init_memory = [function_module.default_system_log_dict]
        str_function_concept += f"{function_module.global_tag}"


    else:
        for db_name in ['sample_kakao_channel_guides', 'sample_kakao_sync_guides']:
            if db_name == 'sample_kakao_sync_guides':
                from functions import simple_kakao_sync_guides_functions as function_module
            elif db_name == 'sample_kakao_channel_guides':
                from functions import simple_kakao_channel_guides_functions as function_module

            functions.append(function_module.functions)
            available_functions.update(function_module.available_functions)
            #init_memory.append(function_module.default_system_log_dict)
            init_memory = [function_module.default_system_log_dict]
            str_function_concept += f"{function_module.global_tag},"
        str_function_concept = str_function_concept[:-1]

    return functions,available_functions, init_memory, str_function_concept