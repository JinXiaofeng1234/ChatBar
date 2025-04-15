import base64
import requests
import json
from load_yaml import GetApiGroup

sk_group = GetApiGroup().get_baidu_speech_keys()
API_KEY = sk_group[0]
SECRET_KEY = sk_group[1]


def speech_recognition(speech_base64):
    url = "https://vop.baidu.com/pro_api"

    try:
        token = get_access_token()
    except Exception as e:
        print(e)
        return None

    # speech 可以通过 get_file_content_as_base64("C:\fakepath\序列 01_1.mp3",False) 方法获取
    payload = json.dumps({
        "format": "pcm",
        "rate": 16000,
        "channel": 1,
        "cuid": "mrHbViZk9UvbW7I12ChUvklefDDCFWYx",
        "dev_pid": 80001,
        "speech": speech_base64,
        "len": len(base64.b64decode(speech_base64)),
        "token": token
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        print(f'百度语音识别失败:{e}')
        return None

    return response.json()


def get_audio_content_as_base64(audio_data):
    base64_data = base64.b64encode(audio_data).decode('utf-8')
    return base64_data


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    try:
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))
    except Exception as e:
        print(f'百度语音api鉴权错误:{e}')
