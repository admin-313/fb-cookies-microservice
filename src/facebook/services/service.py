from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.options import ArgOptions
from abc import ABC, abstractmethod


class FBWebDriver(ABC):
    @abstractmethod
    def run_facebook_parser(self) -> str:
        pass

    @abstractmethod
    def get_options(self) -> ArgOptions:
        pass

    @abstractmethod
    def get_user_agent(self) -> str:
        pass

    @abstractmethod
    def get_proxy_config(self) -> Proxy:
        pass
