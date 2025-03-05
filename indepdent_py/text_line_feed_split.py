import re


class TextLineFeed:
    def __init__(self, text):
        self.text = text

    def type_judge(self):
        if type(self.text) == str:
            split_ls = self.string_process()
        else:
            split_ls = self.ls_process()
        return split_ls

    def string_process(self):
        ls = [chunk for chunk in self.text.split('\n') if chunk]
        return ls

    def ls_process(self):
        new_ls = []
        for chunk in self.text:
            if '\n' in chunk:
                ls = [i for i in chunk.split('\n') if i]
            else:
                ls = [chunk]
            new_ls += ls
        return new_ls


def clean_llm_response(text: str) -> str:
    """
    清理大模型回复中的动作表情描述
    支持清理：
    - 中文括号（）
    - 英文括号()
    - 中文方括号【】
    - 英文方括号[]
    - 书名号《》
    """
    # 匹配所有类型的括号及其内容
    pattern = r'[\(（].*?[\)）]|[\[【].*?[\]】]|《.*?》'

    # 替换所有匹配到的内容为空字符串
    cleaned_text = re.sub(pattern, '', text)

    # 去除可能产生的多余空格
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text


if __name__ == "__main__":
    #     text_ls = TextLineFeed(["""+ 晚安，金晓锋。愿宁静与美好伴随你入梦。
    #
    # 我们明天再见吧。祝你""", '有个好梦。']).type_judge()
    #     print(text_ls)
    # 使用示例
    responses = [
        "你好啊！今天\n\n天气\n真不错！",
        "让我想想（ 思考中 ）这个问题的答案是42",
        "【开心】很高兴见到你！(鞠躬行礼)",
        "《 开心》这是一个【有趣的】(有意思的)问题",
        "这个嘛（歪头思考）...（沉思）...我觉得可以"
    ]

    for response in responses:
        cleaned = clean_llm_response(response)
        print(f"原文: {response}")
        print(f"处理后: {cleaned}")
        print('\n' in cleaned)
        print("-" * 50)
