# 부모 디렉토리에 있는 모듈들을 import 하기 위한 부분########
#import path_configurator
#path_configurator.add_parent_directory_to_path()
###################################################
import logging
from config.open_api_config import initialize_openai_api
from data.db_initializer import init_database
from bot import response_generator
import os
# 환경 변수 설정
os.environ['ALLOW_RESET'] = 'True'


logger = logging.getLogger("SkillServerMain")

initialize_openai_api()
(chat_processor,
 conversation_manager) = response_generator.init_chat_processor_and_conversation_manager()
init_database()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-16s %(levelname)-8s %(message)s ",
    datefmt="%Y-%m-%d %H:%M:%S"
)

from chat_skill_server.api import app

if __name__ == "__main__":
    pass