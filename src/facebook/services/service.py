from selenium.webdriver.common.proxy import Proxy
from abc import ABC, abstractmethod

class WebDriver(ABC):
    @abstractmethod
    def get_facebook_data(self) -> str:
        pass
    
    @abstractmethod
    def get_options(self) -> str:
        pass

    @abstractmethod
    def get_user_agent(self) -> str:
        pass

    @abstractmethod
    def get_proxy_config(self) -> Proxy:
        pass