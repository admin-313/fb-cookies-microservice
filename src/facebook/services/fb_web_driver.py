from abc import ABC, abstractmethod
from typing import Any
from facebook.schemas import ParserResponce

class FBWebDriver(ABC):
    @abstractmethod
    async def run_facebook_parser(self) -> ParserResponce:
        pass

    @abstractmethod
    def get_accesstoken(self) -> str:
        pass
    
    @abstractmethod
    def get_cookie(self) -> str:
        pass

    @abstractmethod
    def get_webdriver_options(self) -> dict[str, Any]:
        pass