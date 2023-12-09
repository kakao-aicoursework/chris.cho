from data.chroma_db_manager import ChromaVectorDBManager
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