from data.chroma_db_manager import ChromaVectorDBManager

_DEBUG = True
class KakaoInfoRetriever:
    def __init__(self, db_name):
        self.db_manger = ChromaVectorDBManager(db_name)
        self.db_name = db_name

    def get_info(self, str_text, n_results=10):
        result_queries = self.db_manger.query_data(query_texts=[f"{str_text}"],
                                                      n_results=n_results)
        answer = self.parse_doc(result_queries)
        return answer

    def parse_doc(self, result_queries, max_len=2048):
        modified_target_ids = []
        for i, str_document in enumerate(result_queries):
            modified_target_ids.append(f"{str_document}")

        if len(modified_target_ids) == 0:
            raise ValueError(f"result_queries={result_queries}")

        str_targets = "\n".join(modified_target_ids)
        if max_len is not None:
            str_targets = str_targets[:max_len]

        return str_targets



def get_kakao_search_results(db_type, **kwargs):
    keyword = kwargs.get('topic', '')  # 'keyword' 키가 없으면 '기본값'을 사용
    meta_context = kwargs.get('additional_info', None)

    if meta_context is not None:
        str_text = f"{keyword}\n{meta_context}"
    else:
        str_text = f"{keyword}"

    retriever = KakaoInfoRetriever(db_type)
    result = retriever.get_info(str_text)
    if _DEBUG:
        print(f"{db_type} -> keyword={keyword} -> search result from vector db = {result}")

    return result

