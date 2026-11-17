import httpx
from datetime import datetime, timezone
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult
from app.config import settings

class LinkedInPlatform(BasePlatform):
    @property
    def name(self) -> str:
        return "LinkedIn"

    async def post(self, message: str) -> PlatformResult:
        if not settings.LINKEDIN_ACCESS_TOKEN or not settings.LINKEDIN_PERSON_URN:
            return PlatformResult(platform=self.name, status="failed", error="Missing LinkedIn credentials.")

        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {settings.LINKEDIN_ACCESS_TOKEN}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        }
        payload = {
            "author": settings.LINKEDIN_PERSON_URN,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": message},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                if response.status_code in [200, 201]:
                    post_urn = response.headers.get("x-restli-id", "")
                    now = datetime.now(timezone.utc)
                    return PlatformResult(
                        platform=self.name,
                        status="success",
                        posted_url=f"https://www.linkedin.com/feed/update/{post_urn}" if post_urn else "https://www.linkedin.com/feed/",
                        public_access=True,
                        date=now.strftime("%Y-%m-%d"),
                        time=now.strftime("%H:%M:%S"),
                        error=None,
                    )
                return PlatformResult(platform=self.name, status="failed", error=f"API error: {response.text}")
        except Exception as e:
            return PlatformResult(platform=self.name, status="failed", error=str(e))
