import requests


# 调用加法API
def call_ai_api(content):
    response = requests.get(f"http://localhost:8000/ai_predict", params={"text":content})
    return response.json()

# 测试API
if __name__ == "__main__":
    while True:
        user_input = input('请输入要预测的文本:')
        if user_input:
            # 测试加法API
            pre_result = call_ai_api(user_input)
            print(f"预测结果: {pre_result['result']['class']}")