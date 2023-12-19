from data.db_initializer import init_database
from bot import response_generator
from ui.chat_interface import ChatInterface



import os
# 환경 변수 설정
os.environ['ALLOW_RESET'] = 'True'


# ChatInterface에서 사용할 콜백 함수
def on_send(user_input):
    global chat_interface
    def callback(response, debug_message, DEBUG):
        try:
            response_message = response['choices'][0]['message']
            message_content = response_message['content']
        except KeyError:
            print(f"KeyError response={response}")
            raise KeyError

        if DEBUG:
            bot_message = (f"<DEBUG_INFO\n{debug_message}\n/DEBUG_INFO>\n" + message_content)
            print(f"user_input:{user_input} ==> response_message_content:{message_content}")
        else:
            bot_message = message_content

        chat_interface.display_bot_message(message=bot_message)
        return message_content

    chat_interface.show_loading_popup()

    response_generator.process_user_input(user_input, callback)

    chat_interface.close_loading_popup()


def main():
    global chat_interface, chat_processor, conversation_manager
    init_database()

    (chat_processor,
     conversation_manager) = response_generator.init_chat_processor_and_conversation_manager()

    chat_interface = ChatInterface(send_callback=on_send)
    chat_interface.run()

if __name__ == "__main__":
    main()