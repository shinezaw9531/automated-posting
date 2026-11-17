import httpx
from datetime import datetime, timezone
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult
from app.config import settings

class MastodonPlatform(BasePlatform):
    @property
    def name(self) -> str:
        return "Mastodon"

    async def post(self, message: str) -> PlatformResult:
        if not settings.MASTODON_ACCESS_TOKEN:
            return PlatformResult(platform=self.name, status="failed", error="Missing Mastodon Access Token.")

        url = f"{settings.MASTODON_API_BASE_URL}/api/v1/statuses"
        headers = {
            "Authorization": f"Bearer {settings.MASTODON_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {"status": message}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    now = datetime.now(timezone.utc)
                    return PlatformResult(
                        platform=self.name,
                        status="success",
                        posted_url=data.get("url"),
                        public_access=True,
                        date=now.strftime("%Y-%m-%d"),
                        time=now.strftime("%H:%M:%S"),
                        error=None,
                    )
                return PlatformResult(platform=self.name, status="failed", error=f"API error: {response.text}")
        except Exception as e:
            return PlatformResult(platform=self.name, status="failed", error=str(e))
