import json
import time


def get_date_time(pattern):
    # 获取当前时间戳
    now = int(time.time())
    # 转换为本地时间结构体
    time_array = time.localtime(now)
    # 格式化日期
    if pattern == 'file':
        standard_style_time = time.strftime("%Y-%m-%d %H_%M_%S", time_array)
    else:
        standard_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return standard_style_time


def read_txt(file_name):
    txt_file = open(file_name, encoding='utf-8')
    content = txt_file.read()
    txt_file.close()
    return content


def save_ls_txt(ls, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        for line in ls:
            f.write(line + '\n')
    f.close()


def save_memory_json(dic_data, path):
    # 将字典写入 JSON 文件
    with open(f'{path}saving/saving-{get_date_time(pattern="file")}.json', 'w', encoding='utf-8') as json_file:
        json.dump(dic_data, json_file, ensure_ascii=False, indent=4)
    json_file.close()
    print("记忆已经保存")


def save_json(dic_data, file_name, path):
    # 将字典写入 JSON 文件
    with open(f'{path}{file_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(dic_data, json_file, ensure_ascii=False, indent=4)
    json_file.close()
    print("已经保存json文件")


def read_json(file_name):
    with open(file_name, encoding='utf-8') as user_file:
        file_contents = user_file.read()
    parsed_json = json.loads(file_contents)
    user_file.close()
    return parsed_json


def save_conversation_history(dic_ls):
    history_ls = list()
    history = dic_ls[1:]
    for dic in history:
        for key, value in dic.items():
            history_ls.append(f'{key}:')
            history_ls.append(value)
    # 使用 range() 函数遍历列表
    for i in range(1, len(history_ls), 2):
        history_ls[i] = history_ls[i] + ';'
    sub_lists = ["".join(history_ls[i:i + 4]) for i in range(0, len(history_ls), 4)]
    save_ls_txt(sub_lists, 'memory.txt')


if __name__ == "__main__":
    data = [{"name": "Alice"},
            {"age": '30'},
            {"city": "New York"},
            {"city": "New York"},
            {"city": "New York"}
            ]
    save_conversation_history(data)