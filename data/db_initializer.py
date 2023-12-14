def init_database():
    from data.data_parser import DataParser
    from data.chroma_db_manager import ChromaVectorDBManager

    db_manager = ChromaVectorDBManager()
    for db_name, local_path_path in zip(['sample_kakao_sync_guides', 'sample_kakao_channel_guides'],
                                        ['./input/project_data_카카오싱크.txt', './input/project_data_카카오톡채널.txt']):

        db_manager.init_and_get_create_collection(db_name)
        parsed_data = DataParser().parse_file_for_kakao_guide_text(local_path_path)
        db_manager.insert_data(parsed_data)

    return
