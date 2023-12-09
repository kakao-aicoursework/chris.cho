from data.abstract_vector_db_manager import AbstractVectorDBManager

def parse_doc(query_result_dict):
    modified_target_ids = []
    for i, str_document in enumerate(query_result_dict['documents'][0]):
        modified_target_ids.append(f"{str_document}")

    if len(modified_target_ids) == 0:
        raise ValueError(f"query_result_dict['documents'][0]={query_result_dict['documents'][0]}")

    str_targets = "\n".join(modified_target_ids)
    return str_targets

def answer_kakao_channel_query(db_manger:AbstractVectorDBManager, **kwargs):
    """
    사용자의 주요 키워드를 기반으로 어떠한 질의에도 답변을 제공합니다.

    :param keyword: 질의의 주요 키워드
    :param context: 질의를 세밀하게 조정하기 위한 추가적인 맥락 (선택적)
    :return: 질의에 대한 답변
    """
    keyword = kwargs.get('keyword', '')  # 'keyword' 키가 없으면 '기본값'을 사용
    meta_context = kwargs.get('meta_context', None)

    if meta_context is not None:
        str_text = f"{keyword}\n{meta_context}"
    else:
        str_text = f"{keyword}"

    # 여기에 데이터 소스에서 정보를 검색하고 질의에 대한 답변
    query_result_dict = db_manger.query_data(query_texts=[f"{str_text}"], n_results=10)
    ret = parse_doc(query_result_dict)

    return ret

main_tag = '카카오톡 채널'
available_functions = {
            "answer_any_query": answer_kakao_channel_query,  # 여기서 get_current_weather는 사전에 정의된 함수
            "answer_any_query2": answer_kakao_channel_query,
            "answer_kakao_channel_query":answer_kakao_channel_query
}

_function_metadata_rev1 = {
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

_function_metadata_rev2 = {
            "name": "answer_any_query2",
            "description": f"사용자의 대화 내용 중에 <{main_tag}>가 포함된 내용과 질문이나 질의 형태면, 해당 함수를 무조건 호출합니다.",
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

_function_metadata_rev3 = {
  "name": "answer_kakao_channel_query",
  "description": "이 함수는 사용자의 질문이 '카카오톡 채널'과 관련된 내용일 경우에만 호출됩니다. 이를 통해 카카오톡 채널에 특화된 맞춤형 응답을 제공합니다.",
  "parameters": {
    "type": "object",
    "properties": {
      "keyword": {
        "type": "string",
        "description": "질의의 주요 키워드로, 이 경우 '카카오톡 채널'에 관련된 키워드만 해당됩니다."
      },
      "meta_context": {
        "type": "string",
        "description": "질의에 추가적인 문맥을 제공합니다. '카카오톡 채널'과 관련된 추가 정보를 포함할 수 있습니다."
      }
    },
    "required": ["keyword"]
  },
  "trigger_condition": "keyword.contains('카카오톡 채널')"
}





#functions = [_function_metadata_rev1, _function_metadata_rev2]
functions = [_function_metadata_rev3]

default_message_log_dict = {'role': 'user', 'content': '카카오톡 채널이 무엇인가요?'}
default_message_log_dict_rev = {'role': 'user', 'content': '카카오톡 채널 API 중, REST API 주소좀 알려줘 '}

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

default_init_message_log = [
        {
            "role": "system",
            "content": f'''
                {get_base_prompt(main_tag)}
            '''
        },
        default_message_log_dict
    ]

