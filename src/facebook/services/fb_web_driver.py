from abc import ABC, abstractmethod


class FBWebDriver(ABC):
    @abstractmethod
    async def run_facebook_parser(self) -> str:
        pass

    @abstractmethod
    def parse_token_from_html(self, html: str) -> str:
        pass
