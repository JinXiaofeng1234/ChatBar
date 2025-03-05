import yaml

try:
    with open('api_key.yaml', 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        # print(data)
except yaml.YAMLError as e:
    print(f"YAML解析错误: {e}")
except FileNotFoundError:
    print("文件未找到")


class GetApiGroup:
    def __init__(self):
        self.data = data

    def get_recho_api(self):
        return self.data['RECHO_KEY']

    def get_fish_audio_key(self):
        return self.data['Fish_Audio_Key']

    def get_baidu_speech_keys(self):
        return (self.data['BaiDu_Speech_Recog']['API_KEY'],
                self.data['BaiDu_Speech_Recog']['SECRET_KEY'])

    def get_gaode_weather_key(self):
        return self.data['Gaode_weather_key']

    def get_erin_keys(self):
        return (self.data['Erin']['API_KEY'],
                self.data['Erin']['SECRET_KEY'])

    def get_qwen_api_key(self):
        return self.data['QWen_API_KEY']

    def get_kimi_search_key(self):
        return self.data['KIMI_SEARCH_API_KEY']

    def get_deep_seek_key(self):
        return self.data['DEEP_SEEK_API_KEY']

    def get_sf_key(self):
        return self.data['Silicon-Flow_API_KEY']


if __name__ == "__main__":
    t = GetApiGroup()
    print(t.get_recho_api())
    # 测试示例
    print("RECHO API:", t.get_recho_api())
    print("Fish Audio Key:", t.get_fish_audio_key())
    baidu_api_key, baidu_secret_key = t.get_baidu_speech_keys()
    print(f"百度语音识别 API_KEY: {baidu_api_key}, SECRET_KEY: {baidu_secret_key}")
    print("高德天气 Key:", t.get_gaode_weather_key())
    erin_api_key, erin_secret_key = t.get_erin_keys()
    print(f"Erin API_KEY: {erin_api_key}, SECRET_KEY: {erin_secret_key}")
    print("QWen API Key:", t.get_qwen_api_key())
    print("KIMI Search Key:", t.get_kimi_search_key())
    print(t.get_deep_seek_key())
