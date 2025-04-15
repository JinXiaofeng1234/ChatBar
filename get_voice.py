import os.path
import threading
import requests
import json
from pydub import AudioSegment
from pydub.playback import play
from files_sort import list_files_sorted_by_time
from typing import Literal, Optional, List
from typing_extensions import Annotated
import httpx
import ormsgpack
from pydantic import BaseModel, conint
from load_yaml import GetApiGroup

RECHO_ROLE_ID = 'market:5088f41c-3ede-46d7-891d-a75970c17eac'
RECHO_KEY = GetApiGroup().get_recho_api()

Fish_Audio_Key = GetApiGroup().get_fish_audio_key()
Fish_role_Key = '537c26bf48244f1cbe03cc57696acba9'


class ServeReferenceAudio(BaseModel):
    audio: bytes
    text: str


class ServeTTSRequest(BaseModel):
    text: str
    chunk_length: Annotated[int, conint(ge=100, le=300, strict=True)] = 200
    # Audio format
    format: Literal["wav", "pcm", "mp3"] = "mp3"
    mp3_bitrate: Literal[64, 128, 192] = 128
    # References audios for in-context learning
    references: List[ServeReferenceAudio] = []
    # Reference id
    # For example, if you want use https://fish.audio/m/7f92f8afb8ec43bf81429cc1c9199cb1/
    # Just pass 7f92f8afb8ec43bf81429cc1c9199cb1
    reference_id: Optional[str] = Fish_role_Key
    # Normalize text for en & zh, this increase stability for numbers
    normalize: bool = True
    # Balance mode will reduce latency to 300ms, but may decrease stability
    latency: Literal["normal", "balanced"] = "normal"


def get_voice(content, prompt_id, main_path, sound_text='', role_id='', model='recho', ):
    if model == 'recho':
        url = "https://v1.reecho.cn/api/tts/simple-generate"

        payload = json.dumps({
            "voiceId": RECHO_ROLE_ID,
            "text": 'text',
            "texts": [
                content
            ],
            "promptId": prompt_id,
            "randomness": 98,
            "stability_boost": 256,
            "probability_optimization": 93,
            "break_clone": True,
            "sharpen": False,
            "flash": False,
            "stream": False,
            "srt": False,
            "seed": -1,
            "dictionary": [
                {}
            ],
            "model": "reecho-neural-voice-001",
            "origin_audio": False
        })
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json',
            'Authorization': RECHO_KEY
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload).json()
        except Exception as e:
            print(f'语音内容api请求有问题:{e}')
            return
        try:
            print(response)
            audio_url = response['data']['audio']
        except Exception as e:
            print(f'语音生成出现问题:{e}')
            return

        if audio_url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                              '537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Content-Type': 'application/json',
                'Authorization': RECHO_KEY
            }
            file_name = audio_url.split('/')[-1]
            # 发送 HTTP 请求并获取响应
            response = requests.get(url=audio_url, headers=headers)
            audio_file_path = f'tmp_audio/{file_name}'
            # 检查请求是否成功
            if response.status_code == 200:
                # 将响应内容写入文件
                with open(audio_file_path, "wb") as file:
                    file.write(response.content)
                print(f"文件 '{file_name}' 已保存到当前目录。")
            else:
                print(f"下载失败, 错误码: {response.status_code}")
                return
    elif model == 'fish':
        audio_file_path = f'{main_path}tmp_audio/text.mp3'
        try:
            request = ServeTTSRequest(
                text=content,
                references=[
                    ServeReferenceAudio(
                        audio=open(f"{main_path}example_sound/example_sound.mp3", "rb").read(),
                        text=sound_text,
                    )
                ],
                reference_id=role_id
            )
        except Exception as e:
            print(e)
            print("fish audio创建请求失败")
            return

        try:
            # 在代码开头添加代理设置
            proxies = {
                "http://": "http://192.168.1.11:7892",  # 根据你的VPN端口修改
                "https://": "http://192.168.1.11:7892"
            }

            with httpx.Client(proxies=proxies, verify=False) as client:
                with open(audio_file_path, "wb") as f:
                    with client.stream(
                            "POST",
                            "https://api.fish.audio/v1/tts",
                            content=ormsgpack.packb(request, option=ormsgpack.OPT_SERIALIZE_PYDANTIC),
                            headers={
                                "authorization": Fish_Audio_Key,
                                "content-type": "application/msgpack",
                                "model": "speech-1.6",  # Specify which TTS model to use
                            },
                            timeout=None,
                    ) as response:
                        for chunk in response.iter_bytes():
                            f.write(chunk)
        except Exception as e:
            print(e)
            print('语音合成失败.')
            return

        if os.path.exists(audio_file_path):
            audio = AudioSegment.from_file(audio_file_path)
            play(audio)


def play_voice_async(content, model_name, path, text, role_key, prompt_id='default', ):
    def voice_thread():
        get_voice(content, prompt_id, path, text, role_key, model=model_name)

    threading.Thread(target=voice_thread, daemon=True).start()


def play_sound_async(file_path):
    def play_sound_thread(path):
        path = rf'{path}tmp_audio'
        sound_files = list_files_sorted_by_time(path)
        if not sound_files:
            return
        try:
            if len(sound_files) == 1:
                audio = AudioSegment.from_file(sound_files[0])
            else:
                audio = AudioSegment.from_file(sound_files[-1])
        except Exception as e:
            print(e)
            return
        play(audio)

    threading.Thread(target=play_sound_thread, args=(file_path,), daemon=True).start()


if __name__ == "__main__":
    # play_voice_async('你好啊，我是纳西妲，你在干什么啊？', model_name='fish', path='role_cards/樱井惠/')
    get_voice('你是谁？！怎么出现在我家门口？', prompt_id='default', main_path='role_cards/樱井惠/',
              sound_text="初次见面，我已经关注你很久了。我叫纳西妲，别看我像个孩子，我比任何一个大人都了解这个世界，"
                         "所以，我可以用我的知识换取你路上的见闻吗？不知道干什么的话，要不要让我带你去转转啊？"
                         "又有心事吗？我来陪你一起想吧！", role_id=Fish_role_Key, model='fish')
    # get_voice("それは...そうでしょうか。でも、少し気になります。もし何かお困りのことがあれば、お手伝いできるかもしれませんよ。"
    #           , prompt_id='default', main_path='role_cards/朝武芳乃/',
    #           sound_text="え、あ、有地さん、何してるんですか？竹刀まで持って……不審者でもいましたか？それは構わないと思いますが……"
    #                      "こんな時間から？下手したら有地さんが不審者にされますよ？まあ、夜に参る人なんてそういないとは思いますが……"
    #                      "それが……お父さんや茉子からは今日ぐらいは休んでいいんじゃないかと言われて.その言葉に従って休んではみたものの"
    #                      "……どうにもこうにも落ち着かなくて", role_id='f9381286cf6642d88e905221d032dc5b', model='fish')
