import httpx
from datetime import datetime, timezone
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult
from app.config import settings

class DevToPlatform(BasePlatform):
    @property
    def name(self) -> str:
        return "DEV.to"

    async def post(self, message: str) -> PlatformResult:
        if not settings.DEVTO_API_KEY:
            return PlatformResult(platform=self.name, status="failed", error="Missing DEV.to API Key.")

        url = "https://dev.to/api/articles"
        headers = {
            "api-key": settings.DEVTO_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "article": {
                "title": message[:50] + ("..." if len(message) > 50 else ""),
                "body_markdown": message,
                "published": True,
                "tags": ["python", "fastapi", "automation"],
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                if response.status_code in [200, 201]:
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
