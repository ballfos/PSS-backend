# app/crud.py
from datetime import datetime, timezone

# import uuid # uuid は不要に
from typing import List, Optional
from zoneinfo import ZoneInfo

from supabase import Client


def get_sql_members(
    client: Client,
):
    response = client.table("members").select("*").execute()

    return response.data


def set_status(
    client: Client,
    id: str,
    status: bool,
):

    response = (
        client.table("members")
        .update(
            {
                "in_room": status,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        .eq("id", id)
        .execute()
    )
    print(response.data)

    return response.data


def update_points(
    client: Client,
    id: str,
    points: int,
    updated_at: str,
):
    print(updated_at)
    if is_different_date_jst(
        datetime.fromisoformat(updated_at).replace(tzinfo=timezone.utc)
    ):
        # 日付が異なる場合はポイントを加算
        response = (
            client.table("members")
            .update(
                {
                    "points": points + 1,
                }
            )
            .eq("id", id)
            .execute()
        )
    else:
        # 日付が同じ場合はポイントを加算しない
        response = (
            client.table("members")
            .update(
                {
                    "points": points,
                }
            )
            .eq("id", id)
            .execute()
        )

    return response.data


def is_different_date_jst(input_datetime: datetime) -> bool:
    """
    入力された標準時を日本時間に変換し、現在の日本時間と異なる日付である場合にTrueを返す。

    Args:
        input_datetime (datetime): 確認する日時（UTCや他のタイムゾーンでもOK）。

    Returns:
        bool: 日付が異なる場合True、それ以外の場合False。
    """
    # 日本時間に変換
    jst = ZoneInfo("Asia/Tokyo")
    input_date_jst = input_datetime.astimezone(jst).date()

    # 現在の日本時間を取得
    current_date_jst = datetime.now(jst).date()

    # 日付が異なる場合Trueを返す
    return current_date_jst != input_date_jst
