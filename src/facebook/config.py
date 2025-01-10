import os

from fake_useragent import UserAgent
from dotenv import load_dotenv

load_dotenv()


def get_proxy_link() -> str:
    proxy_ulr: str | None = os.getenv("PROXY_URL")
    if proxy_ulr:
        return proxy_ulr
    else:
        raise ValueError("The proxy value can't be empty!")


class FakeUserAgent:
    @staticmethod
    def get_fake_ua() -> str:
        ua = UserAgent(browsers="Firefox", os="Windows")
        return ua.random
