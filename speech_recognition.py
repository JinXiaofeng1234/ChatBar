import time

from baidu_speech_recog import speech_recognition, get_audio_content_as_base64
import pyaudio
import numpy as np

# 音频参数
CHUNK = 1024
RATE = 16000
FORMAT = pyaudio.paInt16
SPEECH_THRESHOLD = 500  # 人声阈值，根据需要调整
SILENCE_THRESHOLD = 5  # 静音阈值，根据需要调整
AUTO_FLAG = True
stream = None

try:
    p = pyaudio.PyAudio()

    # 打开音频流
    stream = p.open(format=FORMAT,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
except OSError as e:
    if e.errno == -9996:
        print("错误: 无效的输入设备（没有默认输出设备）。请检查音频设备设置。")
    else:
        print(f"发生其他错误: {e}")

except Exception as e:
    print(f"发生未预期的错误: {e}")


def voice_recognition(model_flag=AUTO_FLAG):
    if not stream:
        print('未检测到麦克风')
        return None
    try:
        print("等待说话...")
        while True:  # 持续监听
            frames = []
            # 检查是否有声音
            data = stream.read(CHUNK)
            volume = np.abs(np.frombuffer(data, dtype=np.int16)).mean()
            # print(volume)

            # 如果检测到声音，开始录音
            if volume > SPEECH_THRESHOLD:
                print(f"{volume}:检测到声音，开始录音...")
                frames.append(data)

                # 继续录音直到检测到静音
                while True:
                    data = stream.read(CHUNK)
                    frames.append(data)
                    volume = np.abs(np.frombuffer(data, dtype=np.int16)).mean()

                    # 如果音量小于阈值，结束录音
                    if volume < SILENCE_THRESHOLD:
                        break

                        # 处理录音数据
                print("录音结束，开始识别...")
                audio_data = b''.join(frames)
                b64_data = get_audio_content_as_base64(audio_data)
                try:
                    res = speech_recognition(b64_data)
                except Exception as e:
                    print(f'语音识别错误:{e}')
                    return None
                print(res)
                # print(audio_data)
                print("等待说话...")
                if not model_flag:
                    return res

    except KeyboardInterrupt:
        print("\n监听被终止")


def close_stream():
    if stream:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    res = voice_recognition(model_flag=False)
    if res:
        print(res['result'][0])
