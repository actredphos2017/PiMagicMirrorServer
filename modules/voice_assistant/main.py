from __future__ import annotations

import threading
import time
import wave
from typing import Callable
from urllib import request, parse

import numpy as np
import pyaudio
import requests
from tqdm import tqdm

from api_key_loader import BAIDU_SPEECH_SECRET, BAIDU_SPEECH_API
from utils.define_module import define_module
from modules.voice_assistant import snowboydecoder
from utils.pipe import Pipe, Notification
from utils.caiyun_weather import get_weather
from utils.eylink_gpt import chat

notifyPipe: Pipe
log: Callable

detector = snowboydecoder.HotwordDetector("MagicMirror.pmdl", sensitivity=0.5)

interrupted = False
weather_map = {
    "CLEAR_DAY": "晴（白天）",
    "CLEAR_NIGHT": "晴（夜间）",
    "PARTLY_CLOUDY_DAY": "多云（白天）",
    "PARTLY_CLOUDY_NIGHT": "多云（夜间）",
    "CLOUDY": "阴",
    "LIGHT_HAZE": "轻度雾霾",
    "MODERATE_HAZE": "中度雾霾",
    "HEAVY_HAZE": "重度雾霾",
    "LIGHT_RAIN": "小雨",
    "MODERATE_RAIN": "中雨",
    "HEAVY_RAIN": "大雨",
    "STORM_RAIN": "暴雨",
    "FOG": "雾",
    "LIGHT_SNOW": "小雪",
    "MODERATE_SNOW": "中雪",
    "HEAVY_SNOW": "大雪",
    "STORM_SNOW": "暴雪",
    "DUST": "浮尘",
    "SAND": "沙尘",
    "WIND": "大风"
}


def interrupt_callback():
    global interrupted
    return interrupted


def init_module(pipe: Pipe):
    # 模块初始化
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "ASSISTANT")


def usage():
    log("Set Note")
    notifyPipe.send("ASSISTANT_SET_NOTE", {
        "content": "购买西红柿"
    })
    log("Add Schedule")
    notifyPipe.send("ASSISTANT_ADD_SCHEDULE", {
        "content": "开会",
        "time": "2025-07-21T14:00:00",
        "prompt": "下午"
    })


def calculate_volume(audio_data) -> list[float]:
    # 将二进制数据转换为numpy数组
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    audio_arrays = np.split(audio_array, 8)
    return list(np.nan_to_num(np.array(map(
        lambda aa: np.sqrt(np.mean(np.nan_to_num(aa, nan=0) ** 2)),
        audio_arrays
    )), nan=0))


def record(stream: pyaudio.Stream):
    notifyPipe.send("ASSISTANT_BEGIN")
    # 新建一个列表，用来存储采样到的数据
    record_buf = []
    count = 0
    flag = True
    audio_data: bytes | None = None

    def check_volume():
        while flag:
            time.sleep(0.1)
            if audio_data is not None:
                notifyPipe.send("ASSISTANT_ASK_VOLUME", {"volume": calculate_volume(audio_data)})

    threading.Thread(target=check_volume).start()
    for _ in tqdm(range(8 * 5)):
        audio_data = stream.read(2048)  # 读出声卡缓冲区的音频数据
        record_buf.append(audio_data)  # 将读出的音频数据追加到record_buf列表
        count += 1

    flag = False
    wf = wave.open('01.wav', 'wb')  # 创建一个音频文件，名字为“01.wav"
    wf.setnchannels(1)  # 设置声道数为2
    wf.setsampwidth(2)  # 设置采样深度为
    wf.setframerate(16000)  # 设置采样率为16000
    # 将数据写入创建的音频文件
    wf.writeframes("".encode().join(record_buf))
    wf.close()


def get_token():
    # 拼接得到Url
    try:
        result = requests.get(
            f"https://aip.baidubce.com/oauth/2.0/token?"
            f"grant_type=client_credentials&"
            f"client_id={BAIDU_SPEECH_API}&"
            f"client_secret={BAIDU_SPEECH_SECRET}"
        ).json()
        # 打印access_token
        print("access_token:", result['access_token'])
        return result['access_token']
    except Exception as err:
        print('token http response http code : ' + str(err))


def is_weather_query(content: str) -> bool:
    weather_keywords = ["天气", "温度", "下雨", "下雪", "风速", "湿度", "气候"]
    return any(keyword in content for keyword in weather_keywords)


def is_note_query(content: str) -> bool:
    note_keywords = ["", "温度", "下雨", "下雪", "风速", "湿度", "气候"]
    return any(keyword in content for keyword in note_keywords)

def is_date_query(content: str) -> bool:
    date_keywords = ["天气", "温度", "下雨", "下雪", "风速", "湿度", "气候"]
    return any(keyword in content for keyword in date_keywords)

def recognize() -> int:
    token = get_token()
    # 2、打开需要识别的语音文件
    speech_data = []
    with open("01.wav", 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        print('file 01.wav length read 0 bytes')

    # 3、设置Url里的参数
    params = {
        'cuid': "12345678python",
        'token': token,
        'dev_pid': 1537
    }
    # 将参数编码
    params_query = parse.urlencode(params)
    # 拼接成一个我们需要的完整的完整的url

    result = requests.post(
        f'http://vop.baidu.com/server_api?{params_query}',
        data=speech_data,
        headers={
            'Content-Type': 'audio/wav; rate=16000',  # 采样率和文件格式
            'Content-Length': str(length)
        }
    ).json()
    print(result)
    try:
        content = result['result'][0]
        log("Recognize Result:", content)

        notifyPipe.send("ASSISTANT_ASK", {
            "content": content,
            "end": True
        })

        if is_weather_query(content):
            weather_info = get_weather()
            if isinstance(weather_info, dict):
                description = weather_map[weather_info['result']['realtime']['skycon']]
                temp = weather_info['result']['realtime']['temperature']
                humidity = weather_info['result']['realtime']['humidity'] * 100
                wind_speed = weather_info['result']['realtime']['wind']['speed']
                forcast = weather_info['result']['forecast_keypoint']
                answer = f"当前天气{description}，气温{temp}度，湿度{int(humidity)}%，风速是{wind_speed}米每秒。{forcast}"
            else:
                answer = "获取天气信息失败。"
        else:
            answer = chat(content)
        return output(answer)
    except:
        return output()


def output(TEXT: str | None = None, hints: list[str] | None = None) -> int:
    if hints is None:
        hints = []
    if TEXT is None:
        notifyPipe.send("ASSISTANT_ANSWER", {
            "content": "Sorry.I don't get you.",
            "hints": hints
        })
        return 0
    elif len(TEXT) >= 20:
        notifyPipe.send("ASSISTANT_ANSWER", {
            "content": TEXT,
            "hints": hints
        })
        return 1
    token = get_token()
    tex = parse.quote_plus(TEXT)
    params = {'tok': token,  # 开放平台获取到的开发者access_token
              'tex': tex,  # 合成的文本，使用UTF-8编码。小于2048个中文字或者英文数字
              'per': 4,  # 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
              'spd': 5,  # 语速，取值0-15，默认为5中语速
              'pit': 5,  # 音调，取值0-15，默认为5中语调
              'vol': 5,  # 音量，取值0-15，默认为5中音量
              'aue': 6,  # 下载的文件格式, 3为mp3格式(默认); 4为pcm-16k; 5为pcm-8k; 6为wav（内容同pcm-16k）
              'cuid': "7749py",  # 用户唯一标识
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数
    # 4、将参数编码，然后放入body，生成Request对象
    data = parse.urlencode(params)
    req = request.Request("http://tsn.baidu.com/text2audio", data.encode('utf-8'))
    # 5、发送post请求
    f = request.urlopen(req)
    result_str = f.read()
    # 6、将返回的header信息取出并生成一个字典
    headers = dict((name.lower(), value) for name, value in f.headers.items())
    # 7、如果返回的header里有”Content-Type: audio/wav“信息，则合成成功
    if "audio/wav" in headers['content-type']:
        print("tts success")
        # 合成成功即将数据存入文件
        with open("result.wav", 'wb') as of:
            of.write(result_str)
    notifyPipe.send("ASSISTANT_ANSWER", {
        "content": TEXT,
        "hints": hints
    })
    return 2


def play_audio(stream, filename):
    wf = wave.open(filename, 'rb')
    while True:
        data = wf.readframes(2048)
        if data == b"":
            break
        stream.write(data)
    time.sleep(0.01)
    wf.close()


close_assistant_timer: threading.Timer | None = None


def close_assistant():
    global close_assistant_timer
    notifyPipe.send("ASSISTANT_CLOSE")
    close_assistant_timer = None


def wait_for_close_assistant():
    global close_assistant_timer
    notifyPipe.send("ASSISTANT_WAITING")
    close_assistant_timer = threading.Timer(5, close_assistant)


def interrupt_close_assistant():
    if close_assistant_timer is not None:
        try:
            close_assistant_timer.cancel()
        except:
            pass


def detected_callback():
    interrupt_close_assistant()
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, output=True, frames_per_buffer=2048)
    record(stream)
    result = recognize()
    if result == 2:
        play_audio(stream, "result.wav")
    elif result == 1:
        play_audio(stream, "tooLong.wav")
    else:
        play_audio(stream, "error.wav")
    stream.stop_stream()
    stream.close()
    wait_for_close_assistant()


@define_module("ASSISTANT")
def main(pipe: Pipe):
    init_module(pipe)
    log('START!')
    while True:
        log("Start Listen!")
        try:
            detector.start(detected_callback=detected_callback,
                           interrupt_check=interrupt_callback,
                           sleep_time=0.03)
        finally:
            detector.terminate()
