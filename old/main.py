import os
import json
import openai
import tkinter as tk
import pandas as pd
from tkinter import scrolledtext
import tkinter.filedialog as filedialog

# API 키가 저장된 파일의 경로
key_file_path = '../config/openai_key.txt'  # 실제 경로로 대체하세요

# 파일에서 API 키 읽기
with open(key_file_path, 'r') as file:
    openai_api_key = file.read().strip()

# OpenAI 라이브러리에 API 키 설정
openai.api_key = openai_api_key


def get_context_prompt(user_input, qeury):
    return (f"<context>''' "
            f"{qeury}"
            f"'''</context>\n"
            f"=============\n"
            f"<user_input>{user_input}</user_input>")
def answer_any_query(**kwargs):
    """
    사용자의 주요 키워드를 기반으로 어떠한 질의에도 답변을 제공합니다.

    :param keyword: 질의의 주요 키워드
    :param context: 질의를 세밀하게 조정하기 위한 추가적인 맥락 (선택적)
    :return: 질의에 대한 답변
    """
    keyword = kwargs.get('keyword', '')  # 'keyword' 키가 없으면 '기본값'을 사용
    meta_context = kwargs.get('keyword', None)

    if meta_context is not None:
        str_text = f"{keyword}\n{meta_context}"
    else:
        str_text = f"{keyword}"

    # 여기에 데이터 소스에서 정보를 검색하고 질의에 대한 답변
    query_result_dict = collection.query(
    query_texts=[f"{str_text}"],
    n_results=10)

    ret =  parse_doc(query_result_dict)
    print(f"!!!! answer_any_query --> ret={ret}")

    return ret

def parse_doc(query_result_dict):
    modified_target_ids = []
    for i, str_document in enumerate(query_result_dict['documents'][0]):
        modified_target_ids.append(f"{str_document}")

    if len(modified_target_ids) == 0:
        raise ValueError(f"query_result_dict['documents'][0]={query_result_dict['documents'][0]}")

    str_targets = "\n".join(modified_target_ids)
    return str_targets


def get_base_prompt(tag, DEBUG=True):
    ret =  f'''
    당신은 지상 최고의 {tag} 챗봇 전문가입니다. 
    당신을 소개할 때, 항상 '{tag} 전문가'로 명시하세요. 
    {tag}과 관련된 질문이 들어오면, 질문에서 주요 keyword를 추출한 후 'answer_any_query' 함수를 호출하여 질의를 처리합니다. 
    만약 상단에 <context>의 항목에 내용이 있는 경우, 해당 내용을 참고해서 답변 바랍니다.
    또한 카카오톡 채널과 관련되지 않는 질문에 대해서는 "그쪽 분야는 잘 모르겠습니다."라고 답변해주세요. 
    소개 후에는 사용자에게 "도움이 필요하신 것이 있나요?"라고 물어보며 답변할 준비를 하세요.
    '''
    if DEBUG:
        print(f"{ret}")
    return ret

#get_base_prompt()
def init_database(input_path = './data/카카오톡채널.txt',
                  db_name = 'kakao-channel',
                  DEBUG=False):
    # 1. 데이터 파일(project_data_카카오톡채널.txt)을 로딩하여 데이터를 생성한다
    dirname, basename = os.path.split(input_path)
    name, ext = os.path.splitext(basename)

    input_txt = ""
    with open(input_path, 'r') as f:
        input_txt = f.read()

    # 2. 수집된 데이터를 정형화 시킨다.
    '''
    1) #으로 전반적인 데이터를 구분한다(docuement)
        만약 좀 더 고도화 한다면?
        - 단순히 공란으로 단어 단위로 구분하여 집어 넣는다
        - 300~500 토큰 단위로 넣어서 집어 넣는다

    2) 예외적인 #에 대해서는 좀 더 상세히 처리한다
        - 더 효과적인 활용 방법
        - 지원하는 기능
    '''
    import chromadb
    client = chromadb.PersistentClient()
    client.delete_collection(name=db_name)

    collection = client.get_or_create_collection(
        name=db_name
    )

    ids = []
    documents = []
    splited_result = input_txt.split("#")
    for i, sub_txt in enumerate(splited_result):
        str_key = f"{name}_{i}_"
        str_key += sub_txt.split("\n")[0]

        document = f"{str_key}:{sub_txt}"
        if DEBUG:
            print(f"index={i}, key={str_key} document ::->\n {document}")

        ids.append(str_key)
        documents.append(document)

    # DB 저장
    collection.add(
        documents=documents,
        ids=ids
    )
    pass

    return name, collection



# response에 CSV 형식이 있는지 확인하고 있으면 저장하기
def send_message(message_log, functions, gpt_model="gpt-3.5-turbo", temperature=0.1, DEBUG=True):
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=message_log,
        temperature=temperature,
        functions=functions,
        function_call='auto',
    )

    response_message = response["choices"][0]["message"]

    if not response_message.get("function_call"):
        if DEBUG:
            print(f"not function_call!!!!!!!!!!response_message={response_message.content}")

    else:
        if DEBUG:
            print("function_call!!!!!!!!!!")

        available_functions = {
            "answer_any_query": answer_any_query,
        }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        # 사용하는 함수에 따라 사용하는 인자의 개수와 내용이 달라질 수 있으므로
        # **function_args로 처리하기
        if DEBUG:
            print(f"function_args={function_args}")

        function_response = fuction_to_call(**function_args)
        function_response = get_context_prompt("", function_response)

        # 함수를 실행한 결과를 GPT에게 보내 답을 받아오기 위한 부분
        message_log.append(response_message)  # GPT의 지난 답변을 message_logs에 추가하기
        message_log.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # 함수 실행 결과도 GPT messages에 추가하기
        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=message_log,
            temperature=temperature,
        )  # 함수 실행 결과를 GPT에 보내 새로운 답변 받아오기
    return response.choices[0].message.content


def main(main_tag, DEBUG=True):
    message_log = [
        {
            "role": "system",
            "content": f'''
                {get_base_prompt(main_tag)}
            '''
        }
    ]

    functions = [
        {
            "name": "answer_any_query",
            "description": f"사용자의 <{main_tag}>관련된 주요 키워드를 기반으로 어떠한 질의에도 답변을 제공합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "The main keyword around which the query is centered."
                    },
                    "meta_context": {
                        "type": "string",
                        "description": "Additional context to refine the query."
                    },
                },
                "required": ["keyword"]
            }
        }
    ]
    if DEBUG:
        print(f"init_message_log={message_log}")

    def show_popup_message(window, message):
        popup = tk.Toplevel(window)
        popup.title("")

        # 팝업 창의 내용
        label = tk.Label(popup, text=message, font=("맑은 고딕", 12))
        label.pack(expand=True, fill=tk.BOTH)

        # 팝업 창의 크기 조절하기
        window.update_idletasks()
        popup_width = label.winfo_reqwidth() + 20
        popup_height = label.winfo_reqheight() + 20
        popup.geometry(f"{popup_width}x{popup_height}")

        # 팝업 창의 중앙에 위치하기
        window_x = window.winfo_x()
        window_y = window.winfo_y()
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        popup_x = window_x + window_width // 2 - popup_width // 2
        popup_y = window_y + window_height // 2 - popup_height // 2
        popup.geometry(f"+{popup_x}+{popup_y}")

        popup.transient(window)
        popup.attributes('-topmost', True)

        popup.update()
        return popup

    def on_send(DEBUG=True):
        user_input = user_entry.get()

        user_entry.delete(0, tk.END)

        if user_input.lower() == "quit":
            window.destroy()
            return

        #query = answer_any_query(user_input)
        new_user_input = user_input#get_context_prompt(user_input, query)
        if DEBUG:
            print(f"new_user_input={new_user_input}")


        message_log.append({"role": "user", "content": new_user_input})
        conversation.config(state=tk.NORMAL)  # 이동
        conversation.insert(tk.END, f"You: {user_input}\n", "user")  # 이동
        thinking_popup = show_popup_message(window, "처리중...")
        window.update_idletasks()
        # '생각 중...' 팝업 창이 반드시 화면에 나타나도록 강제로 설정하기
        response = send_message(message_log, functions)
        thinking_popup.destroy()

        message_log.append({"role": "assistant", "content": response})

        # 태그를 추가한 부분(1)
        conversation.insert(tk.END, f"gpt assistant: {response}\n", "assistant")
        conversation.config(state=tk.DISABLED)
        # conversation을 수정하지 못하게 설정하기
        conversation.see(tk.END)

    window = tk.Tk()
    window.title("GPT AI")

    font = ("맑은 고딕", 10)

    conversation = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg='#f0f0f0', font=font)
    # width, height를 없애고 배경색 지정하기(2)
    conversation.tag_configure("user", background="#c9daf8")
    # 태그별로 다르게 배경색 지정하기(3)
    conversation.tag_configure("assistant", background="#e4e4e4")
    # 태그별로 다르게 배경색 지정하기(3)
    conversation.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    # 창의 폭에 맞추어 크기 조정하기(4)

    input_frame = tk.Frame(window)  # user_entry와 send_button을 담는 frame(5)
    input_frame.pack(fill=tk.X, padx=10, pady=10)  # 창의 크기에 맞추어 조절하기(5)

    user_entry = tk.Entry(input_frame)
    user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)

    send_button = tk.Button(input_frame, text="Send", command=on_send)
    send_button.pack(side=tk.RIGHT)

    window.bind('<Return>', lambda event: on_send())
    window.mainloop()


if __name__ == "__main__":
    tag, collection = init_database()
    main(tag)

'''
1. 데이터 파일(project_data_카카오톡채널.txt)을 로딩하여 데이터를 생성한다 
2. 수집된 데이터를 정형화 시킨다. 
3. chatGPT api를 이용하여 질의 응답이 가능한 모델을 구성한다. 
4. 질의는 prompt Engineering을 이용하여 효율성을 높인다.
'''