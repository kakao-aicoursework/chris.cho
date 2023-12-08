from ui.chat_interface import ChatInterface
from config.open_api_config import initialize_openai_api

# OpenAI API 초기화
initialize_openai_api()

def on_send(user_input):
    # 여기에 사용자 입력 처리 로직을 추가하세요.
    print(f"Processing: {user_input}")

def main():
    chat_interface = ChatInterface(send_callback=on_send)
    chat_interface.run()

if __name__ == "__main__":
    main()