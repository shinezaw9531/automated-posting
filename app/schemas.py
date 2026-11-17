from pydantic import BaseModel, Field, field_validator
import re
from typing import List, Optional

class PostRequest(BaseModel):
    message: str = Field(..., description="Message to post, max 200 characters with exactly 1 CTA link.")

    @field_validator("message")
    @classmethod
    def validate_message_constraints(cls, v: str) -> str:
        if len(v) > 200:
            raise ValueError("Message must not exceed 200 characters.")

        url_pattern = re.compile(r"https?://[^\s]+")
        urls = url_pattern.findall(v)

        if len(urls) != 1:
            raise ValueError(f"Message must contain exactly one CTA link. Found {len(urls)} link(s).")

        return v

class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None

class PostResponse(BaseModel):
    success: bool
    results: List[PlatformResult]
