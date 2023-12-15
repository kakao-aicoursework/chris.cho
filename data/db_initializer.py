def init_database():
    from data.data_parser import DataParser
    from data.chroma_db_manager import ChromaVectorDBManager
    import constants

    db_manager = ChromaVectorDBManager()
    for db_name, local_path_path in zip([constants.KAKAO_SYNC_GUIDES,
                                         constants.KAKAO_CHANNEL_GUIDES,
                                         constants.KAKAO_SOCIAL_GUIDES],
                                        [constants.KAKAO_SYNC_GUIDES_PATH,
                                         constants.KAKAO_CHANNEL_GUIDES_PATH,
                                         constants.KAKAO_SOCIAL_GUIDES_PATH
                                         ]):

        db_manager.init_and_get_create_collection(db_name)
        parsed_data = DataParser().parse_file_for_kakao_guide_text(local_path_path)
        db_manager.insert_data(parsed_data)

    return
