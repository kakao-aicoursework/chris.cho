import constants

def get_function_call_info(db_name):
    if db_name == constants.KAKAO_SYNC_GUIDES:
        from functions import simple_kakao_sync_guides_functions as function_module
    elif db_name == constants.KAKAO_CHANNEL_GUIDES:
        from functions import simple_kakao_channel_guides_functions as function_module
    elif db_name == constants.KAKAO_SOCIAL_GUIDES:
        from functions import simple_kakao_social_guides_functions as function_module
    else:
        raise ValueError(f"not supported db_name={db_name}")

    return (function_module.functions,
            function_module.available_functions,
            function_module.global_tag, function_module.default_system_log_dict)

