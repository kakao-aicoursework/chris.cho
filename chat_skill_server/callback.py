from chat_skill_server.dto import ChatbotRequest
import requests
import logging
from bot import response_generator

SYSTEM_MSG = "당신은 카카오 서비스 제공자입니다."
logger = logging.getLogger("Callback")


def callback(response, debug_message, DEBUG=False):
    response_message = response['choices'][0]['message']
    message_content = response_message['content']
    return message_content

def callback_handler(request: ChatbotRequest) -> dict:

    # ===================== start =================================
    output_text = response_generator.process_user_input(request.userRequest.utterance, callback)
    print(output_text)

   # 참고링크 통해 payload 구조 확인 가능
    payload = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": output_text
                    }
                }
            ]
        }
    }
    # ===================== end =================================
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/ai_chatbot_callback_guide
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format
    url = request.userRequest.callbackUrl

    if url:
        requests.post(url=url, json=payload, verify=False)