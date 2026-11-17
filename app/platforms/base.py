from abc import ABC, abstractmethod
from app.schemas import PlatformResult

class BasePlatform(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def post(self, message: str) -> PlatformResult:
        pass
