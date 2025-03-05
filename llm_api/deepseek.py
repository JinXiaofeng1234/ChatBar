# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
from ChatBar import load_yaml

api_key = load_yaml.GetApiGroup().get_deep_seek_key()


def chat_with_ds(model_name, conversation_history):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    try:
        stream_response = client.chat.completions.create(
            model=model_name,
            messages=conversation_history,
            stream=True
        )
        return stream_response
    except Exception as e:
        print(e, '网络请求失败')
        return None


if __name__ == "__main__":
    # chat_with_ds('deepseek-chat')
    pass
