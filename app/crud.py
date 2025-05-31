# app/crud.py
from datetime import datetime, timezone

# import uuid # uuid は不要に
from typing import List, Optional

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
            }
        )
        .eq("id", id)
        .execute()
    )
    print(response.data)

    return response.data
