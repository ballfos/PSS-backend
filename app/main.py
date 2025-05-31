import os

import dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import Client, create_client

from app.crud import get_sql_members, set_status
from app.schemas import MemberUpdate

dotenv.load_dotenv()
# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# Create a Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


app = FastAPI()


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
