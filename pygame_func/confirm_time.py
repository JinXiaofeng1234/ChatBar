from datetime import datetime, time


def get_current_time_period():
    # 获取当前时间
    current_time = datetime.now().time()

    # 定义时间段的边界
    periods = [
        {
            'name': '白天',
            'start': time(6, 0, 0),
            'end': time(12, 0, 0),
            'description': ('morning',)
        },
        {
            'name': '中午',
            'start': time(12, 0, 0),
            'end': time(14, 0, 0),
            'description': ('noon',)
        },
        {
            'name': '傍晚',
            'start': time(14, 0, 0),
            'end': time(18, 0, 0),
            'description': ('sunset',)
        },
        {
            'name': '晚上',
            'start': time(18, 0, 0),
            'end': time(0, 0, 0),
            'description': ('evening_light_on', 'evening_light_off')
        }
    ]

    # 判断当前时间属于哪个时间段
    for period in periods:
        # 特殊处理跨午夜的情况
        if period['name'] == '晚上':
            if current_time >= period['start'] or current_time < time(6, 0, 0):
                return period
        else:
            if period['start'] <= current_time < period['end']:
                return period

    # 如果没有匹配的时间段（理论上不会发生）
    return {
        'name': '未知',
        'description': '无法确定当前时间段'
    }


if __name__ == "__main__":
    # 获取并打印当前时间段
    current_period = get_current_time_period()
    print(f"当前时间：{datetime.now().strftime('%H:%M:%S')}")
    print(f"当前时间段：{current_period['name']}")
    print(f"描述：{current_period['description']}")
