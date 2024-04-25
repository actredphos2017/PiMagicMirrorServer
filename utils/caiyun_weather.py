import json

import requests

from orm import LocalStorage

import datetime

current_longitude = "120.35"
current_latitude = "30.31"
caiyun_api_token = "mkhvpq9w0AsN6gjl"


def get_comprehensive_url(token: str, longitude, latitude):
    return f"https://api.caiyunapp.com/v2.6/TAkhjf8d1nlSlspN/{longitude},{latitude}/weather?alert=true&dailysteps=3&hourlysteps=24&token={token}"


def get_weather() -> dict | int:
    """
    :return: dict 天气查询结果 , int 天气查询失败后的代码
    """
    old_weather = LocalStorage.get("weather")
    if old_weather:
        old_data: dict = json.loads(old_weather)
        if old_data['server_time'] + 900 > datetime.datetime.now().timestamp():
            return old_data

    response = requests.get(get_comprehensive_url(caiyun_api_token, current_longitude, current_latitude))
    match response.status_code:
        case 200:
            respData = response.text
            LocalStorage.set("weather", respData)
            return dict(json.loads(respData))
        case _:
            return response.status_code

