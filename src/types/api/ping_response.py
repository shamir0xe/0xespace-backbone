from typing import Optional
from pydantic import BaseModel


class PingResponse(BaseModel):
    remaining_time: Optional[int] = None
