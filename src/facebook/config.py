import os

from fake_useragent import UserAgent
from dotenv import load_dotenv

load_dotenv()


class ProxyConfig:
    @staticmethod
    def get_proxy_link() -> str:
        proxy_ulr: str | None = os.getenv("PROXY_URL")
        if proxy_ulr:
            return proxy_ulr
        else:
            raise ValueError("The proxy value can't be empty!")


class FakeUserAgentConfig:
    @staticmethod
    def get_fake_ua_firefox() -> str:
        ua = UserAgent(browsers="Firefox", os="Windows")
        return ua.random
