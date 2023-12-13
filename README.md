# chris.cho의 프로젝트 저장소입니다.
### AI Chatbot with LangChain(+OpenAI) and Chroma Vector DB

## 개요
- 파이썬 기반의 LangChain(+openai)이 적용된 AI 챗봇 어플리케이션입니다. 
- 현재 2번째 미션(chatGPT API -> LangChain library)까지 적용된 버전입니다.
## 주요 특징
- LangChain의 `LLMChain`과  `ChatPromptTemplate` 을 활용 했습니다.
- 기존 chatGPT API의 입출력부(함수 호출부 포함)을 호한할 수 있는 컨셉을 적용 하였습니다.

## 설치 방법
[![Python 3.9+](https://img.shields.io/badge/Python-3.11-3776AB)](https://www.python.org/downloads/release/python-380/)

시작하기 전에, 다음 명령어를 실행하여 필요한 패키지들을 설치하세요:

```bash
pip install -r requirement.txt
```

## 사용 방법
어플리케이션을 실행하려면, 다음의 명령어를 사용합니다


```bash
python app.py
```

## 구조
프로젝트의 주요 디렉토리와 파일들은 다음과 같습니다:

* `bot/`: 챗봇의 핵심 로직(openai, langchain)과 대화 관리자.
* `prompt_template/`: 챗봇이 사용하는 프롬프트 템플릿들.
* `functions/`: 날씨 정보, 카카오 채널, 싱크 관련 API 쿼리 등의 함수 호출(function call) 모듈.
* `ui/`: 챗 UI 인터페이스 관련 코드.
* `data/`: 벡터 DB 및 파싱 스크립트등의 데이터 처리 관련 모듈 
* `input/`: 과제에 주어진 입력 데이터 파일들.
* `tests/`: 챗봇의 기능들을 테스트하기 위한 스크립트 코드.