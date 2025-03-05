import requests
# from bs4 import BeautifulSoup
import html5lib
from kimi_search import main as kimi_scarp
from load_yaml import GetApiGroup


def format_weather_info(json_data):
    # 获取实时天气信息
    live_weather = json_data[0]['lives'][0]
    # 获取预报天气信息
    forecast_weather = json_data[1]['forecasts'][0]['casts']

    # 格式化实时天气信息
    current_weather = f"""  
当前天气情况：  
    城市: {live_weather['province']}{live_weather['city']}  
    天气: {live_weather['weather']}  
    温度: {live_weather['temperature']}℃  
    风向: {live_weather['winddirection']}风  
    风力: {live_weather['windpower']}级  
    湿度: {live_weather['humidity']}%  
    报告时间: {live_weather['reporttime']}  
    """

    # 格式化未来天气预报
    forecast_str = "\n未来天气预报："
    for day in forecast_weather:
        week_map = {'1': '周一', '2': '周二', '3': '周三', '4': '周四', '5': '周五', '6': '周六', '7': '周日'}
        forecast_str += f"""  
        {day['date']} {week_map[day['week']]}:  
        白天: {day['dayweather']}, {day['daytemp']}℃, {day['daywind']}风{day['daypower']}级  
        夜间: {day['nightweather']}, {day['nighttemp']}℃, {day['nightwind']}风{day['nightpower']}级  
        """

    return current_weather + forecast_str


class WebScarp:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        }

    @staticmethod
    def search_get(kw):
        try:
            res_txt = kimi_scarp(search_prompt=kw)
            return res_txt
        except Exception as e:
            print(e, "请检查网络")
            return None

    def autonavi_weather_forecast(self):
        api_key = GetApiGroup().get_gaode_weather_key()
        weather_facts_url = f'https://restapi.amap.com/v3/weather/weatherInfo?' \
                            f'city=330100&extensions=base&key={api_key}'
        weather_forecast_url = f'https://restapi.amap.com/v3/weather/weatherInfo?' \
                               f'city=330100&extensions=all&key={api_key}'
        res_ls = []
        url_ls = [weather_facts_url, weather_forecast_url]
        for url in url_ls:
            try:
                res_json = requests.get(url, headers=self.headers)
                res_ls.append(res_json.json())
            except Exception as e:
                print(f"报错:{e},网络出现问题,请检查是不是开vpn了,如果不是在重新试一下")
                return None
        return format_weather_info(res_ls)


if __name__ == "__main__":
    test = WebScarp()
    # print(test.autonavi_weather_forecast())
    print(test.search_get('奥斯曼帝国为什么解体'))
