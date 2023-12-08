import os
from data.chroma_db_manager import ChromaVectorDBManager
class DataParser:
    '''
    비정형 참고 데이터를 파싱하는 클래스입니다.
    '''
    def parse_file_for_kakao_channel(self, file_path, DEBUG=False):
        '''
        주어진 파일 경로에서 데이터를 읽고 파싱합니다.
         1) #으로 전반적인 데이터를 구분한다(docuement)
            만약 좀 더 고도화 한다면?
            - 단순히 공란으로 단어 단위로 구분하여 집어 넣는다
            - 300~500 토큰 단위로 넣어서 집어 넣는다

        2) 예외적인 #에 대해서는 좀 더 상세히 처리한다
            - 더 효과적인 활용 방법
            - 지원하는 기능
        '''
        input_txt = ""
        with open(file_path, 'r') as f:
            input_txt = f.read()

        if len(input_txt) == 0:
            return None, None, None

        dirname, basename = os.path.split(file_path)
        name, ext = os.path.splitext(basename)
        name = name.split("_")[-1]

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

        return documents, ids, None