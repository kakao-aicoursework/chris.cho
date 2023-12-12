from functions.kakao_info_retriever import KakaoInfoRetriever

global_tag = '카카오싱크와 카카오채널'

def get_kakao_sync_info(**kwargs):
    keyword = kwargs.get('topic', '')  # 'keyword' 키가 없으면 '기본값'을 사용
    meta_context = kwargs.get('additional_info', None)

    if meta_context is not None:
        str_text = f"{keyword}\n{meta_context}"
    else:
        str_text = f"{keyword}"

    retriever = KakaoInfoRetriever('sample_kakao_sync_guides')
    return retriever.get_info(str_text)

_function_metadata = {
    "name": "get_kakao_sync_info",
    "description": f"{global_tag}과 관련된 정보를 제공합니다.예를 들어, f{global_tag} 도입에 필요한 검수 및 설정 등에 대한 질문에 답변합니다.",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "질문의 주제나 관심사, 예: '검수', '설정', '도입'"
            },
            "additional_info": {
                "type": "string",
                "description": "질문에 대한 추가적인 정보 또는 구체적인 세부 사항"
            }
        },
        "required": ["topic"]
    }
}


available_functions = {
            "get_kakao_sync_info": get_kakao_sync_info
}

functions = [_function_metadata]

default_message_log_dict = {'role': 'user', 'content': f'{global_tag}이 무엇인가요?'}
default_message_log_dict_rev = {'role': 'user', 'content': f'{global_tag}의 도입 방법 알려줘 '}



def get_base_system_prompt(tag):
    ret =  f'''
    당신은 지상 최고의 {tag} 챗봇 전문가입니다. 
    당신을 소개할 때, 항상 '{tag} 전문가'로 명시하세요. 
    {tag}과 관련된 질문이 들어오면 중복없이 매우 상세한 답변 부탁드립니다.
    또한 {tag}과 관련없는 질문에 대해서는 "그쪽 분야는 잘 모르겠습니다."라고 답변해주세요. 
    소개 후에는 사용자에게 "도움이 필요하신 것이 있나요?"라고 물어보며 답변할 준비를 하세요.
    '''
    return ret

default_system_log_dict = {
            "role": "system",
            "content": f'''
                {get_base_system_prompt(global_tag)}
            '''}