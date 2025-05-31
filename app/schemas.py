from typing import List, Optional

from pydantic import BaseModel, Field


class MemberUpdate(BaseModel):
    in_room: bool = Field(..., description="In room status")


class pointsUpdate(BaseModel):
    points: int = Field(..., description="Points to increment")
    updated_at: str = Field(..., description="Timestamp of the update")
