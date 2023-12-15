import os
import re
from data.chroma_db_manager import ChromaVectorDBManager
class DataParser:
    '''
    비정형 참고 데이터를 파싱하는 클래스입니다.
    '''
    def parse_file_for_kakao_guide_text(self, file_path, DEBUG=True):
        '''
        1) #으로 title 수준의 구분을 진행
        2) #내에 숫자가 있는 경우 sub-title 수준의 구분을 진행


        데이터 기준 예시(카카오 싱크)
        -> table 기준 : 카카오 싱크
        -> id(index) 기준 : # + . -> <title + sub-title>
        -> docuement 기준 : <title + sub-title>
        if 질의가 카카오 싱크에 대해서 왔어..
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
        splited_result = input_txt.split("\n#")
        for i, mainsection_text in enumerate(splited_result):
            #str_key = f"{name}_{i}_"
            # 먼저 숫자와 점으로 시작하는 모든 위치를 찾습니다.
            str_key = f"{i}_"
            str_key += mainsection_text.split("\n")[0]

            matches = list(re.finditer(r'\d+\.', mainsection_text))
            if matches:
                pre_match = matches[0]
                for j, cur_match in enumerate(matches[1:]):
                    start_pos = pre_match.start()
                    end_pos = cur_match.start()
                    subsection_text = mainsection_text[start_pos:end_pos].strip()
                    pre_match = cur_match

                    number_with_dot = cur_match.group()
                    str_key += f"_{number_with_dot}"
                    document = f"{str_key}-{subsection_text}"

                    ids.append(str_key)
                    documents.append(document)
                    if DEBUG:
                        print(
                            f"index={i}-{j}, title(len={len(str_key)})={str_key} | document(len={len(document)})=\n {document}")

            else:
                document = f"{mainsection_text}"
                ids.append(str_key)
                documents.append(document)

                if DEBUG:
                    print(f"index={i}, title(len={len(str_key)})={str_key} | document(len={len(document)})=\n {document}")


        return documents, ids, None