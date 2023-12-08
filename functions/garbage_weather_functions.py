import json
def get_current_weather(location, unit="fahrenheit"):
    weather_info = {
        "location": location,
        "temperature": "24",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

available_functions = {
            "get_current_weather": get_current_weather,  # 여기서 get_current_weather는 사전에 정의된 함수
}

weather_function_metadata = {
    "name": "get_current_weather",
    "description": "특정 지역의 날씨를 알려줍니다.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "지역이름 eg. 서울, 부산, 제주도",
            },
            "unit": {"type": "string", "enum": ["섭씨", "화씨"]},
        },
        "required": ["location"],
    },
}


functions = [weather_function_metadata]

default_message_log_dict = {'role': 'user', 'content': '지금 서울날씨를 섭씨로 알려줘'}


