import httpx
from datetime import datetime, timezone
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult
from app.config import settings

class RedditPlatform(BasePlatform):
    @property
    def name(self) -> str:
        return "Reddit"

    async def post(self, message: str) -> PlatformResult:
        if not settings.REDDIT_CLIENT_ID or not settings.REDDIT_PASSWORD:
            return PlatformResult(platform=self.name, status="failed", error="Missing Reddit credentials.")

        auth_url = "https://www.reddit.com/api/v1/access_token"
        auth_data = {
            "grant_type": "password",
            "username": settings.REDDIT_USERNAME,
            "password": settings.REDDIT_PASSWORD,
        }
        auth_headers = {"User-Agent": settings.REDDIT_USER_AGENT}

        try:
            async with httpx.AsyncClient() as client:
                token_res = await client.post(
                    auth_url,
                    data=auth_data,
                    auth=(settings.REDDIT_CLIENT_ID, settings.REDDIT_CLIENT_SECRET),
                    headers=auth_headers,
                    timeout=10.0,
                )
                if token_res.status_code != 200:
                    return PlatformResult(platform=self.name, status="failed", error="Reddit authentication failed.")

                access_token = token_res.json().get("access_token")
                post_url = "https://oauth.reddit.com/api/submit"
                headers = {
                    "Authorization": f"bearer {access_token}",
                    "User-Agent": settings.REDDIT_USER_AGENT,
                }
                payload = {
                    "api_type": "json",
                    "kind": "self",
                    "sr": f"u_{settings.REDDIT_USERNAME}",
                    "title": message[:100],
                    "text": message,
                }

                post_res = await client.post(post_url, data=payload, headers=headers, timeout=10.0)
                if post_res.status_code == 200:
                    post_data = post_res.json().get("json", {}).get("data", {})
                    now = datetime.now(timezone.utc)
                    return PlatformResult(
                        platform=self.name,
                        status="success",
                        posted_url=post_data.get("url", f"https://www.reddit.com/user/{settings.REDDIT_USERNAME}"),
                        public_access=True,
                        date=now.strftime("%Y-%m-%d"),
                        time=now.strftime("%H:%M:%S"),
                        error=None,
                    )
                return PlatformResult(platform=self.name, status="failed", error=f"Post error: {post_res.text}")
        except Exception as e:
            return PlatformResult(platform=self.name, status="failed", error=str(e))
