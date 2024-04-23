import requests

current_longitude = "120.35"
current_latitude = "30.31"
caiyun_api_token = "mkhvpq9w0AsN6gjl"


def get_comprehensive_url(token: str, longitude, latitude):
    return f"https://api.caiyunapp.com/v2.6/TAkhjf8d1nlSlspN/{longitude},{latitude}/weather?alert=true&dailysteps=14&hourlysteps=24&token={token}"


def request_for_comprehensive() -> dict | int:
    response = requests.get(get_comprehensive_url(caiyun_api_token, current_longitude, current_latitude))
    match response.status_code:
        case 200:
            return dict(response.json())
        case _:
            return response.status_code
