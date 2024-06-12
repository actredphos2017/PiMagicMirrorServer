import json
from datetime import datetime


def compose(compose_id: str, params=None):
    if params is None:
        params = {}
    return {"id": compose_id, "params": params}


def compose_structure(left: list[dict], right: list[dict]):
    return {"left": left, "right": right}


def single_note(content: str, create_time: int = int(datetime.now().timestamp() * 1000)):
    return {"content": content, "create_time": create_time}


def note(notes: list[dict]):
    return {"notes": notes}


def single_schedule(name: str, content: str = "", date: int = int(datetime.now().timestamp() * 1000)):
    return {"name": name, "content": content, "date": date}


def schedule_list(schedules: list[dict]):
    return {"schedules": schedules}


def custom_settings(_compose_structure: dict, _note: dict, _schedule_list: dict):
    return {"compose_structure": _compose_structure, "note": _note, "schedule_list": _schedule_list}


def get_default_custom_settings():
    return custom_settings(
        _compose_structure=compose_structure(
            left=[compose("clock"), compose("calendar")],
            right=[compose("weather")],
        ),
        _note=note([
            single_note("在这里可以创建你的记事")
        ]),
        _schedule_list=schedule_list([
            single_schedule("开会")
        ]),
    )


def get_default_custom_settings_string():
    return json.dumps(get_default_custom_settings())
