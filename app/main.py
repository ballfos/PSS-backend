import os

import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import Client, create_client

from app.crud import get_sql_members

dotenv.load_dotenv()
# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# Create a Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


app = FastAPI()


@app.put("/members/{id}")
async def update_status(id: int):

    return {"message": f"Member {id} status updated successfully."}


@app.get("/members")
async def get_members():
    members = get_sql_members(supabase)

    return {"members": members}
