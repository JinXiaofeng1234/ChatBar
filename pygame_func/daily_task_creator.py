import random
from datetime import datetime, timedelta, date
from datetime import time as datetime_time  # 重命名避免冲突
import time as time_module  # 如果你需要time模块，将其重命名

# Data from the JSON file
data = {
    "actions_ls": [
        "家庭茶道练习", "和服整理与熨烫", "传统料理烹饪", "手工编织", "家庭布艺制作", "书法练习", "插花艺术",
        "家庭园艺",
        "传统乐器练习（如三味线）", "家庭缝纫", "和果子制作", "传统节日装饰", "家庭清洁与整理", "家庭祭祀祭品制作",
        "打扫房间", "擦拭地板", "整理榻榻米", "洗衣服", "晾晒衣物", "洗碗", "准备晚餐", "收拾厨房", "整理家庭衣物",
        "换洗床上用品", "照料家庭花草", "整理家庭杂物"
    ],
    "breakfast_ls": ["白米饭", "味噌汤", "烤鱼", "煎蛋", "纳豆", "腌黄瓜", "海苔", "豆腐", "茶", "煮青豆"],
    "lunch_ls": ["便当（饭团）", "炸猪排", "乌冬面", "蔬菜沙拉", "煎鸡肉", "冷荞麦面", "天妇罗", "煮鱼", "蒸饺子",
                 "酱黄瓜"],
    "dinner_ls": ["寿喜烧", "火锅", "刺身", "烤鸡肉串", "煮牛肉", "茄子炒肉", "海鲜烩饭", "炒面", "煎豆腐",
                  "蔬菜天妇罗"],
    "midnight_snack": ["拉面", "煎饺", "章鱼小丸子", "炸鸡", "烤鱿鱼", "关东煮", "煎饼", "三明治", "炒年糕", "煮虾"]
}


def generate_schedule(data):
    # Start time for the schedule
    # 获取当前日期
    current_date = date.today()
    # 创建一个新的日期时间，保留当前日期，时间设置为6:00
    start_time = datetime.combine(current_date, datetime_time(6, 0))
    schedule = {}

    # Add breakfast
    breakfast_food = random.sample(data["breakfast_ls"], 4)
    schedule[start_time] = f"{start_time.strftime('%H:%M')} - 早餐: ({','.join(breakfast_food)})"
    start_time += timedelta(hours=1)

    # Add random activities until lunch
    for _ in range(4):  # 4 activities before lunch
        action = random.choice(data["actions_ls"])
        schedule[start_time] = f"{start_time.strftime('%H:%M')} - {action}"
        start_time += timedelta(hours=1)

        # Add lunch
    lunch_food = random.sample(data["lunch_ls"], 2)
    schedule[start_time] = f"{start_time.strftime('%H:%M')} - 午餐: ({','.join(lunch_food)})"
    start_time += timedelta(hours=1)

    # Add random activities until dinner
    for _ in range(5):  # 5 activities before dinner
        action = random.choice(data["actions_ls"])
        schedule[start_time] = f"{start_time.strftime('%H:%M')} - {action}"
        start_time += timedelta(hours=1)

        # Add dinner
    dinner_food = random.sample(data["dinner_ls"], 2)
    schedule[start_time] = f"{start_time.strftime('%H:%M')} - 晚餐: ({','.join(dinner_food)})"
    start_time += timedelta(hours=1)

    # Add random activities until midnight snack
    for _ in range(3):  # 3 activities before midnight snack
        action = random.choice(data["actions_ls"])
        schedule[start_time] = f"{start_time.strftime('%H:%M')} - {action}"
        start_time += timedelta(hours=1)

        # Add midnight snack
    midnight_snack_food = random.choice(data["midnight_snack"])
    schedule[start_time] = f"{start_time.strftime('%H:%M')} - 夜宵: {midnight_snack_food}"

    start_time += timedelta(hours=1)
    schedule[start_time] = f"{start_time.strftime('%H:%M')} - 睡觉"

    start_time += timedelta(hours=7)
    schedule[start_time] = f"{start_time.strftime('%H:%M')} - 起床"

    return schedule


def find_nearest_interval(arr, x):
    # 如果 x 小于数组最小值
    if x <= arr[0]:
        return arr[0], arr[1]

        # 如果 x 大于数组最大值
    if x >= arr[-1]:
        return arr[-2], arr[-1]

        # 遍历查找最近的区间
    for i in range(len(arr) - 1):
        if arr[i] <= x <= arr[i + 1]:
            return arr[i], arr[i + 1]

            # 如果没找到（理论上不会发生）
    return None


def create_daily_schedule(data_dic, daily_flag, dic_schedule=None):
    # 获取当前时间戳
    now = int(time_module.time())
    # 转换为本地时间结构体
    time_array = datetime.fromtimestamp(now)
    # time_array = datetime(2024, 12, 23, 11, 00)
    if not dic_schedule:
        # Generate and print the schedule
        daily_schedule = generate_schedule(data_dic)
    else:
        daily_schedule = {datetime.fromisoformat(k): v for k, v in dic_schedule.items()}

    daily_task_string = ";".join([item[1] for item in daily_schedule.items()])
    # print(daily_task_string)
    time_ls = [key for key in daily_schedule.keys()]
    nearest_array = find_nearest_interval(time_ls, time_array)

    interval_time = nearest_array[1] - time_array

    string_ls = list()

    string_a = f'现在是:{time_array}'

    if not daily_flag:
        string_b = f'你今天的日程是:{daily_task_string}'
        string_ls.append(string_b)
    string_c = f'你正在进行的事项:{daily_schedule[nearest_array[0]]}'

    string_ls.append(string_a)

    string_ls.append(string_c)

    if (interval_time.total_seconds() / 60) < 10:
        string_d = f'你马上就要干下一项事项了,即{daily_schedule[nearest_array[1]]}'
        string_ls.append(string_d)

    return daily_schedule, "\n".join(string_ls)


def get_date():
    # 获取当前时间戳
    now = int(time_module.time())
    # 转换为本地时间结构体
    time_array = datetime.fromtimestamp(now)

    # 只获取年月日部分
    date_only = time_array.date()
    return date_only


if __name__ == "__main__":
    print(create_daily_schedule(data_dic=data, daily_flag=False))
