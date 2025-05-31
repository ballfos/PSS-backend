import os

import dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import Client, create_client

from app.crud import get_sql_members, set_status
from app.schemas import MemberUpdate

# 環境変数の読み込み
dotenv.load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")

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

@app.patch("/members/{id}")
async def update_status(id: str, member_update: MemberUpdate):
    """
    Update the in_room status of a member.
    """
    # Update the member's status in the database
    updated_member = set_status(supabase, id, member_update.in_room)

    if not updated_member:
        raise HTTPException(status_code=404, detail=f"Member with id {id} not found.")

    return {"message": "Member status updated successfully", "member": updated_member}


@app.get("/members")
async def get_members():
    members = get_sql_members(supabase)

    return {"members": members}
