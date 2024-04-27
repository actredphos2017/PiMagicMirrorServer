from __future__ import annotations

import requests

from api_key_loader import EYLINK_GPT_API


def chat(words: str, role: str = "user") -> str | None:
    response = requests.post(
        "https://gtapi.xiaoerchaoren.com:8932/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {EYLINK_GPT_API}"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": role,
                    "content": words
                }
            ],
            "stream": False
        }
    )

    try:
        return list(map(lambda a: a["message"]["content"], response.json()["choices"]))[0]
    except:
        return None


if __name__ == '__main__':
    print(chat("帮我出一个杭州旅游规划"))
