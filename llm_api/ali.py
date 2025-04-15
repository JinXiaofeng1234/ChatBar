from openai import OpenAI
import load_yaml

api_key = load_yaml.GetApiGroup().get_qwen_api_key()


def chat_with_qw(conversation_history, model_name="qwen-plus"):
    try:
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
    except Exception as e:
        print(e, '请求建立失败')
        return None
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=conversation_history,
            stream=True,
            stream_options={"include_usage": True}
        )
    except Exception as e:
        print(e, '大模型回复中断')
        return None
    # for chunk in completion:
    #     print(chunk.model_dump_json())
    return completion


if __name__ == "__main__":
    chat_with_qw([{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': '你是谁？'}])
