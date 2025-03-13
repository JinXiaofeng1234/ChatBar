import requests
import json
import load_yaml

sk_group = load_yaml.GetApiGroup().get_erin_keys()
API_KEY = sk_group[0]  # "482ecSxmh5aRPZgFCKz0jyGi"\
SECRET_KEY = sk_group[1]  # "18sEP5QKUtxvK0PqZZnrpuAzxmXkGLlz"


def main(conversation_history):
    token = get_access_token()
    if token:
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-turbo-128k?access_token=" \
              + get_access_token()
    else:
        print('Net Work Error')
        return

    payload = json.dumps({
        "messages": conversation_history,
        "disable_search": False,
        "enable_citation": False,
        "stream": True
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, stream=True)
        return response
    except Exception as e:
        print(e)
        return None


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    try:
        access_token = str(requests.post(url, params=params).json().get("access_token"))
        return access_token
    except Exception as e:
        print(e)
