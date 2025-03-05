import requests
from ChatBar import load_yaml

key = load_yaml.GetApiGroup().get_sf_key()


def chat_with_model(model_name, conversation_history):
    url = "https://api.siliconflow.cn/v1/chat/completions"

    payload = {
        "model": model_name,
        "messages": conversation_history,
        "stream": True,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response
