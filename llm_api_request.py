import sys
import ollama
import json

sys.path.append('llm_api')

import baidu
import ali
import deepseek
import siliconflow


def chat_with_model(conversation_history, model=0):
    tokens = 0
    full_response = ""
    json_content = None
    print("Assistant: ", end="", flush=True)
    if model == 0:
        # 创建流式响应
        stream = ollama.chat(
            model='qwen2.5:14b-instruct-q6_K',  # 或者你使用的其他模型名称
            messages=conversation_history,
            stream=True
        )

        # 处理流式响应
        for chunk in stream:
            if chunk.get('done') is False:
                content = chunk['message']['content']
                print(content, end="", flush=True)
                full_response += content

        print("\n")  # 换行

    if model == 1:
        erin_response = baidu.main(conversation_history=conversation_history)
        if erin_response is None:
            return None
        for line in erin_response.iter_lines():
            try:
                line_str = line.decode("UTF-8")
                if line_str.startswith("data: "):
                    response_dic = json.loads(line_str[6:])
                    content = response_dic["result"]
                    print(content, end="", flush=True)
                    full_response += content
                    tokens = response_dic['usage']["total_tokens"]
            except Exception as e:
                print(e)
        print("\n")  # 换行

    if model == 2:
        qwen_response = ali.chat_with_qw(conversation_history=conversation_history)
        if qwen_response is None:
            return None
        for chunk in qwen_response:
            try:
                json_content = json.loads(chunk.model_dump_json())
                content = json_content['choices'][0]['delta']['content']
                print(content, end="", flush=True)
                full_response += content
            except Exception as e:
                ...
        if json_content:
            tokens = json_content['usage']['total_tokens']
        print("\n")  # 换行

    if model == 3:
        ds_response = deepseek.chat_with_ds('deepseek-chat', conversation_history=conversation_history)
        if ds_response is None:
            return None
        for chunk in ds_response:
            try:
                json_content = json.loads(chunk.model_dump_json())
                content = json_content['choices'][0]['delta']['content']
                print(content, end="", flush=True)
                full_response += content
            except Exception as e:
                ...
        if json_content:
            tokens = json_content['usage']['total_tokens']
        print("\n")  # 换行

    if model == 4:
        ds_response = deepseek.chat_with_ds('deepseek-reasoner', conversation_history=conversation_history)
        if ds_response is None:
            return None
        for chunk in ds_response:
            try:
                json_content = json.loads(chunk.model_dump_json())
                content = json_content['choices'][0]['delta']['content']
                print(content, end="", flush=True)
                full_response += content
            except Exception as e:
                ...
        if json_content:
            tokens = json_content['usage']['total_tokens']
        print("\n")  # 换行

    if model == 5:
        qwen_response = ali.chat_with_qw(conversation_history=conversation_history, model_name='qwen-max')
        if qwen_response is None:
            return None
        for chunk in qwen_response:
            try:
                json_content = json.loads(chunk.model_dump_json())
                content = json_content['choices'][0]['delta']['content']
                print(content, end="", flush=True)
                full_response += content
            except Exception as e:
                ...
        if json_content:
            tokens = json_content['usage']['total_tokens']
        print("\n")  # 换行

    if model == 6:
        silicon_response = siliconflow.chat_with_model('Qwen/Qwen2.5-72B-Instruct-128K',
                                                       conversation_history)
        if silicon_response is None:
            return None
        for line in silicon_response.iter_lines():
            try:
                line_json = json.loads(line.decode("UTF-8")[6:])
                content = line_json['choices'][0]['delta']['content']
                print(content, end='', flush=True)
                full_response += content
                tokens = line_json['usage']['total_tokens']
            except Exception:
                ...
        print('\n')

    if model == 'vision':
        # 创建流式响应
        stream = ollama.chat(
            model='minicpm-v:8b-2.6-q8_0',  # 或者你使用的其他模型名称
            messages=conversation_history,
            stream=True
        )

        # 处理流式响应
        for chunk in stream:
            if chunk.get('done') is False:
                content = chunk['message']['content']
                print(content, end="", flush=True)
                full_response += content

        print("\n")  # 换行
    return full_response, tokens


# 主对话循环
if __name__ == "__main__":
    back_tuple = ('', 0)
    # 初始化对话历史
    conversation_history = []
    # conversation_history = [{
    #     'role': 'user',
    #     'content': '图片中有什么?',
    #     'images': [r"C:\Users\Cara  al sol\Pictures\Camera Roll\Simone de Beauvoir.jpg"]
    # }]
    # print("输入 'quit' 结束对话")
    while True:
        # chat_with_model(conversation_history, 2)
        # break
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            for i in conversation_history:
                print(i)
            print(back_tuple[1])
            break
        # 将用户输入添加到对话历史
        conversation_history.append({"role": "system", "content": user_input})
        back_tuple = chat_with_model(conversation_history, model=6)
        response = back_tuple[0]
        # 将助手的回复添加到对话历史
        conversation_history.append({"role": "assistant", "content": response})
