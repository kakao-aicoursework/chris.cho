import threading

from ui.chat_interface import ChatInterface
from config.open_api_config import initialize_openai_api

from bot.openai_chat_processor import OpenAIChatProcessor
# OpenAI API 초기화
initialize_openai_api()

# 비즈니스 로직을 별도의 함수로 정의
def process_user_input(user_input, callback):
    # 여기서 비동기적으로 처리 로직을 수행
    message_log = [{'role': 'user', 'content': f'{user_input}'}]
    response = chat_processor.process_chat(message_log)
    callback(response)

# ChatInterface에서 사용할 콜백 함수
def on_send(user_input):
    chat_interface.show_popup("처리 중입니다...")

    def callback(response):
        message = response.choices[0].message.content
        print(f"user_input:{user_input} ==> {message}")

        chat_interface.display_bot_message(message=message)
        chat_interface.close_popup()

    threading.Thread(target=process_user_input, args=(user_input, callback), daemon=True).start()


def main():
    global chat_interface, chat_processor

    chat_processor = OpenAIChatProcessor("gpt-3.5-turbo")
    chat_interface = ChatInterface(send_callback=on_send)
    chat_interface.run()

if __name__ == "__main__":
    main()