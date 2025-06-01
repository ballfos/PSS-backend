import json
import os

import dotenv
import requests

# Bot トークン（xoxb-で始まるトークン）
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_NAME = os.getenv("SLACK_CHANNEL_NAME")


def send_slack_message(name: str, status: bool):

    message = f"{name} さんが{'入室' if status else '退室'}しました!"

    message_data = {
        "channel": CHANNEL_NAME,
        "text": message,
        "mrkdwn": True,  # Markdown の有効化
    }

    # API のエンドポイント
    url = "https://slack.com/api/chat.postMessage"

    # ヘッダーの設定
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8",
    }

    # リクエストを送信
    response = requests.post(url, headers=headers, data=json.dumps(message_data))

    # レスポンスを確認
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("ok"):
            print("メッセージを送信しました！")
        else:
            print("エラー:", response_json.get("error"))
    else:
        print("HTTP リクエスト失敗:", response.status_code)
