import json

import requests

from orm import Session, KeyValuePairStorage

import datetime

current_longitude = "120.35"
current_latitude = "30.31"
caiyun_api_token = "mkhvpq9w0AsN6gjl"


def get_comprehensive_url(token: str, longitude, latitude):
    return f"https://api.caiyunapp.com/v2.6/TAkhjf8d1nlSlspN/{longitude},{latitude}/weather?alert=true&dailysteps=14&hourlysteps=24&token={token}"


def request_for_comprehensive() -> dict | int:
    with Session() as session:
        old_weather: KeyValuePairStorage | None = session.query(KeyValuePairStorage).get("weather")
        if old_weather:
            old_data: dict = json.loads(old_weather.value)
            if old_data['server_time'] + 900 > datetime.datetime.now().timestamp():
                return old_data

    response = requests.get(get_comprehensive_url(caiyun_api_token, current_longitude, current_latitude))
    match response.status_code:
        case 200:
            respData = response.text
            with Session() as session:
                target_column = session \
                    .query(KeyValuePairStorage) \
                    .filter_by(key="weather")
                if target_column.count() == 0:
                    session.add(KeyValuePairStorage(key="weather", value=respData))
                else:
                    target_column.update({KeyValuePairStorage.value: respData})
                session.commit()
            return dict(json.loads(respData))
        case _:
            return response.status_code
