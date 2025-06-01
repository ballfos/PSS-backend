# app/crud.py
from datetime import datetime, timezone

# import uuid # uuid は不要に
from typing import List, Optional
from zoneinfo import ZoneInfo

from supabase import Client

from app.utils import is_different_date_jst


def read_members(
    client: Client,
) -> List[dict]:
    response = client.table("members").select("*").execute()
    return response.data


def update_member(
    client: Client,
    id: str,
    in_room: bool,
    with_points: bool = False,
) -> Optional[dict]:
    """
    メンバーの在室状況を更新する関数

    ポイント更新を行う場合のみ updated_at を更新する

    Args:
        client (Client): Supabase クライアント
        id (str): メンバーのID
        in_room (bool): 在室状況
        with_points (bool): ポイント更新を行うかどうか
    Returns:
        Optional[dict]: 更新されたメンバー情報、存在しない場合は None
    """

    # メンバー情報を取得
    member = client.table("members").select("*").eq("id", id).execute()
    if not member.data:
        return None
    member = member.data[0]

    # 在室状況の更新
    json = {
        "in_room": in_room,
    }
    if with_points and in_room:
        updated_at = member.get("updated_at", None)
        if updated_at and is_different_date_jst(datetime.fromisoformat(updated_at)):
            # 日付が異なる場合はポイントを加算
            points = member.get("points", 0) + 1
        else:
            # 日付が同じ場合はポイントを加算しない
            points = member.get("points", 0)

        json["points"] = points
        json["updated_at"] = datetime.now(timezone.utc).isoformat()

    response = client.table("members").update(json).eq("id", id).execute()
    if response.data:
        return response.data[0]
    return None
