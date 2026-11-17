import asyncio
from typing import List
from app.schemas import PlatformResult
from app.platforms.twitter import TwitterPlatform
from app.platforms.linkedin import LinkedInPlatform
from app.platforms.devto import DevToPlatform
from app.platforms.mastodon import MastodonPlatform
from app.platforms.reddit import RedditPlatform

class PostingService:
    def __init__(self):
        self.platforms = [
            TwitterPlatform(),
            LinkedInPlatform(),
            DevToPlatform(),
            MastodonPlatform(),
            RedditPlatform(),
        ]

    async def broadcast(self, message: str) -> List[PlatformResult]:
        tasks = [platform.post(message) for platform in self.platforms]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_results = []
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                processed_results.append(
                    PlatformResult(
                        platform=self.platforms[i].name,
                        status="failed",
                        error=str(res),
                    )
                )
            else:
                processed_results.append(res)

        return processed_results
