from functions.kakao_info_retriever import get_kakao_search_results
import constants

global_tag = constants.KAKAO_SOCIAL_ROLE

_DEBUG=True
def get_kakao_social_api_info(**kwargs):
    return get_kakao_search_results(constants.KAKAO_SOCIAL_GUIDES, **kwargs)

_function_metadata = {
    "name": "get_kakao_social_api_info",
    "description": f"{global_tag} API의 기능, 사용법, 이용 정책 및 기타 관련 정보에 대한 질문에 답변합니다. 예를 들어, 프로필 API, 친구 정보, 피커 사용법, 사용 권한 신청 방법, 쿼터 제한, 프로필 공개 설정, 친구 정보 제공 조건 등에 대한 질문에 답변할 수 있습니다.",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "질문의 주제나 관심사. 예: '프로필 API', '친구 정보', '피커 사용법', '사용 권한 신청', '쿼터 제한', '프로필 공개 설정', '친구 정보 제공 조건'"
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
            "get_kakao_social_api_info": get_kakao_social_api_info
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