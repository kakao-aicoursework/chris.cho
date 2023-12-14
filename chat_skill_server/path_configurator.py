# path_configurator.py

import sys
import os

def add_parent_directory_to_path():
    """
    Adds the parent directory of the current script to the sys.path list.
    This allows the script to import modules from the parent directory.
    """
    # 현재 스크립트의 디렉토리 경로를 얻습니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 상위 디렉토리 경로를 얻습니다.
    parent_dir = os.path.dirname(current_dir)

    # 상위 디렉토리를 모듈 검색 경로의 시작 부분에 추가합니다.
    sys.path.insert(0, parent_dir)
