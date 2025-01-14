from abc import ABC, abstractmethod
from typing import Any

class FBWebDriver(ABC):
    @abstractmethod
    async def run_facebook_parser(self) -> str:
        pass

    @abstractmethod
    def parse_token_from_html(self, html: str) -> str:
        pass
    
    @abstractmethod
    def get_webdriver_options(self) -> dict[str, Any]:
        pass