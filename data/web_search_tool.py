import os
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper

GOOGLE_API_KEY = None
GOOGLE_CSE_ID = None

def initialize_google_api(key_file_path = './config/google_key.txt' ):
    # 파일에서 API 키 읽기
    with (open(key_file_path, 'r') as file):
        session = file.read()
        return session.split(";")
    raise ValueError(f"key_file_path={key_file_path}")

(GOOGLE_API_KEY,
 GOOGLE_CSE_ID) = initialize_google_api()
search = GoogleSearchAPIWrapper(
    google_api_key=os.getenv("GOOGLE_API_KEY",GOOGLE_API_KEY),
    google_cse_id=os.getenv("GOOGLE_CSE_ID",GOOGLE_CSE_ID)
)

search_tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=search.run,
)

def query_web_search(llm_chat_processor, user_message: str) -> str:
    context = {"user_message": user_message}
    context["related_web_search_results"] = search_tool.run(user_message)

    has_value = llm_chat_processor.search_value_check_chain.run(context)

    print(has_value)
    if has_value == "Y":
        return llm_chat_processor.search_compression_chain.run(context)
    else:
        return ""