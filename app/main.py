import os
from typing import Annotated

import dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client, create_client

from app.crud import read_members, update_member
from app.schemas import MemberUpdate
from app.slack import send_slack_message
from app.utils import sort_members_by_grade

# 環境変数の読み込み
dotenv.load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")
DEVICE_AUTH_TOKENS = os.getenv("DEVICE_AUTH_TOKENS", "").split(",")

# Supabase クライアントの初期化
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI アプリケーションの初期化
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

http_bearer = HTTPBearer(auto_error=False)


@app.patch("/members/{id}")
async def patch_member(
    id: str,
    member_update: MemberUpdate,
    authorization: Annotated[
        HTTPAuthorizationCredentials | None, Depends(http_bearer)
    ] = None,
):
    """
    メンバーの在室状況を更新するエンドポイント

    認証トークンが存在する場合は points のインクリメント処理を追加で行う
    """

    with_points = False
    if authorization:
        if authorization.credentials in DEVICE_AUTH_TOKENS:
            with_points = True
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization token.")

    # メンバーの在室状況を更新
    updated_member = update_member(supabase, id, member_update.in_room, with_points)
    if not updated_member:
        raise HTTPException(status_code=404, detail=f"Member with id {id} not found.")
    # Slack への通知
    send_slack_message(updated_member["name"], updated_member["in_room"])

    sorted_members = sort_members_by_grade(updated_member)

    return {
        "message": "Member status updated successfully",
        "member": sorted_members,
    }


@app.get("/members")
async def get_members():
    members = read_members(supabase)
    sorted_members = sort_members_by_grade(members)

    return {"members": sorted_members}
