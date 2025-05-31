from typing import List, Optional

from pydantic import BaseModel, Field


class MemberUpdate(BaseModel):
    in_room: bool = Field(..., description="In room status")
