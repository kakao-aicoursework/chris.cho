from data.chroma_db_manager import ChromaVectorDBManager

_tag = '카카오싱크와 카카오채널'

class KakaoChannelInfoRetriever:
    def __init__(self):
        pass
    def get_info(self, str_text, n_results=10):
        db_manger = ChromaVectorDBManager('sample_kakao_sync_guides')
        query_result_dict = db_manger.query_data(query_texts=[f"{str_text}"],
                                                      n_results=n_results)
        answer = self.parse_doc(query_result_dict)
        return answer

    def parse_doc(self, query_result_dict, max_len=2048):
        modified_target_ids = []
        for i, str_document in enumerate(query_result_dict['documents'][0]):
            modified_target_ids.append(f"{str_document}")

        if len(modified_target_ids) == 0:
            raise ValueError(f"query_result_dict['documents'][0]={query_result_dict['documents'][0]}")

        str_targets = "\n".join(modified_target_ids)
        if max_len is not None:
            str_targets = str_targets[:max_len]

        return str_targets

def get_kakao_sync_info(**kwargs):
    keyword = kwargs.get('topic', '')  # 'keyword' 키가 없으면 '기본값'을 사용
    meta_context = kwargs.get('additional_info', None)

    if meta_context is not None:
        str_text = f"{keyword}\n{meta_context}"
    else:
        str_text = f"{keyword}"

    retriever = KakaoChannelInfoRetriever()
    return retriever.get_info(str_text)

_function_metadata = {
    "name": "get_kakao_sync_info",
    "description": f"{_tag}과 관련된 정보를 제공합니다.예를 들어, f{_tag} 도입에 필요한 검수 및 설정 등에 대한 질문에 답변합니다.",
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

default_message_log_dict = {'role': 'user', 'content': f'{_tag}이 무엇인가요?'}
default_message_log_dict_rev = {'role': 'user', 'content': f'{_tag}의 도입 방법 알려줘 '}



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
                {get_base_system_prompt(_tag)}
            '''}