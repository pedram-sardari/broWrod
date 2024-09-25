from datetime import timezone, datetime

from pydantic import BaseModel, Field


class DateTime(BaseModel):
    """
    Fields: created_at, updated_at
    """
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 description="Record creation time")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 description="Record last updated time")
