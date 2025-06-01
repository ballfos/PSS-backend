from datetime import datetime
from zoneinfo import ZoneInfo


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


def sort_members_by_grade(members):
    # ソート順を定義
    grade_order = {"professor": 0, "M2": 1, "M1": 2, "B4": 3}

    # ソート関数を適用
    sorted_members = sorted(
        members, key=lambda member: grade_order.get(member["grade"], float("inf"))
    )

    return sorted_members
