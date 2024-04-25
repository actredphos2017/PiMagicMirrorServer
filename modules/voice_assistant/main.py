import json
import time
import wave
from typing import Callable
from urllib import request, parse

import pyaudio
from tqdm import tqdm

from api_key_loader import BAIDU_SPEECH_SECRET, BAIDU_SPEECH_API
from pipe import Pipe, Notification

notifyPipe: Pipe
log: Callable


def init_module(pipe: Pipe):
    # 模块初始化
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "语音助手")


def simulation_assistant():
    log("模拟开始语音助手")
    notifyPipe.send("ASSISTANT_BEGIN")

    time.sleep(1)

    log("模拟语音识别过程")
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今",
        "end": False
    })
    time.sleep(0.2)
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今天",
        "end": False
    })
    time.sleep(0.2)
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今天天气",
        "end": False
    })
    time.sleep(0.2)
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今天天气怎么",
        "end": False
    })
    time.sleep(0.2)
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今天天气怎么样",
        "end": False
    })
    time.sleep(0.5)
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今天天气怎么样",
        "end": True
    })

    time.sleep(2)

    log("模拟语音助手回应")
    notifyPipe.send("ASSISTANT_ANSWER", {
        "content": "杭州市今天天气小雨转阴，气温13到20摄氏度，出门注意带伞哦",
    })

    time.sleep(5)

    log("模拟结束语音助手")
    notifyPipe.send("ASSISTANT_CLOSE")


def usage():
    log("设置便签")
    notifyPipe.send("ASSISTANT_SET_NOTE", {
        "content": "购买西红柿"
    })
    log("添加日程")
    notifyPipe.send("ASSISTANT_ADD_SCHEDULE", {
        "content": "开会",
        "time": "2025-07-21T14:00:00",
        "prompt": "下午"
    })


def demo():
    notifyPipe.send("ASSISTANT_BEGIN")
    # 实例化一个PyAudio对象
    pa = pyaudio.PyAudio()
    # 打开声卡，设置 采样深度为16位、声道数为1、采样率为16、输入、采样点缓存数量为2048
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
    # 新建一个列表，用来存储采样到的数据
    record_buf = []
    count = 0
    for i in tqdm(range(8 * 5)):
        audio_data = stream.read(2048)  # 读出声卡缓冲区的音频数据
        record_buf.append(audio_data)  # 将读出的音频数据追加到record_buf列表
        count += 1
        print('*')
    wf = wave.open('01.wav', 'wb')  # 创建一个音频文件，名字为“01.wav"
    wf.setnchannels(1)  # 设置声道数为2
    wf.setsampwidth(2)  # 设置采样深度为
    wf.setframerate(16000)  # 设置采样率为16000
    # 将数据写入创建的音频文件
    wf.writeframes("".encode().join(record_buf))
    # 写完后将文件关闭
    wf.close()
    # 停止声卡
    stream.stop_stream()
    # 关闭声卡
    stream.close()
    # 终止pyaudio
    pa.terminate()


def get_token():
    API_Key = BAIDU_SPEECH_API  # 官网获取的API_Key
    Secret_Key = BAIDU_SPEECH_SECRET  # 为官网获取的Secret_Key
    # 拼接得到Url
    Url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_Key}&client_secret={Secret_Key}"
    try:
        resp = request.urlopen(Url)
        result = json.loads(resp.read().decode('utf-8'))
        # 打印access_token
        print("access_token:", result['access_token'])
        return result['access_token']
    except Exception as err:
        print('token http response http code : ' + str(err))


def recognize():
    token = get_token()
    # 2、打开需要识别的语音文件
    speech_data = []
    with open("01.wav", 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        print('file 01.wav length read 0 bytes')

    # 3、设置Url里的参数
    params = {'cuid': "12345678python",  # 用户唯一标识，用来区分用户，长度为60字符以内。
              'token': token,  # 我们获取到的 Access Token
              'dev_pid': 1537}  # 1537 表示识别普通话
    # 将参数编码
    params_query = parse.urlencode(params)
    # 拼接成一个我们需要的完整的完整的url
    Url = 'http://vop.baidu.com/server_api' + "?" + params_query

    # 4、设置请求头
    headers = {
        'Content-Type': 'audio/wav; rate=16000',  # 采样率和文件格式
        'Content-Length': length
    }

    # 5、发送请求，音频数据直接放在body中
    # 构建Request对象
    req = request.Request(Url, speech_data, headers)
    # 发送请求
    res_f = request.urlopen(req)
    result = json.loads(res_f.read().decode('utf-8'))
    print(result)
    try:
        content = result['result'][0]
    except KeyError:
        content = "你说啥？"
    print("识别结果:", content)

    notifyPipe.send("ASSISTANT_ASK", {
        "content": content,
        "end": True
    })


def output():
    time.sleep(2)
    token = get_token()
    # 2、将需要合成的文字做2次urlencode编码
    TEXT = "原神，启动"
    notifyPipe.send("ASSISTANT_ANSWER", {
        "content": TEXT
    })
    tex = parse.quote_plus(TEXT)  # 两次urlencode
    # 3、设置文本以及其他参数
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
        time.sleep(3)
        notifyPipe.send("ASSISTANT_WAITING")
        time.sleep(5)
        notifyPipe.send("ASSISTANT_CLOSE")


def main(pipe: Pipe):
    init_module(pipe)
    log('启动！')
    # 主代码从这里开始
    #demo()
    recognize()
    #output()