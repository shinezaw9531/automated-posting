import httpx
from datetime import datetime, timezone
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult
from app.config import settings

class TwitterPlatform(BasePlatform):
    @property
    def name(self) -> str:
        return "X (Twitter)"

    async def post(self, message: str) -> PlatformResult:
        if not settings.TWITTER_BEARER_TOKEN:
            return PlatformResult(platform=self.name, status="failed", error="Missing Twitter Bearer Token.")

        url = "https://api.twitter.com/2/tweets"
        headers = {
            "Authorization": f"Bearer {settings.TWITTER_BEARER_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {"text": message}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                if response.status_code == 201:
                    data = response.json().get("data", {})
                    tweet_id = data.get("id")
                    now = datetime.now(timezone.utc)
                    return PlatformResult(
                        platform=self.name,
                        status="success",
                        posted_url=f"https://x.com/i/web/status/{tweet_id}" if tweet_id else None,
                        public_access=True,
                        date=now.strftime("%Y-%m-%d"),
                        time=now.strftime("%H:%M:%S"),
                        error=None,
                    )
                return PlatformResult(platform=self.name, status="failed", error=f"API error: {response.text}")
        except Exception as e:
            return PlatformResult(platform=self.name, status="failed", error=str(e))
