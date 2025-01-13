import os
from fake_useragent import UserAgent


class ProxyConfig:
    @staticmethod
    def get_socks5_proxy_config() -> dict[str, dict[str, str | None]]:
        socks_proxy: str | None = os.getenv("PROXY_URL")
        return {
            "proxy": {
                "http": socks_proxy,
                "https": socks_proxy,
                "no_proxy": "localhost,ENDPOINT",
            }
        }


class FakeUserAgentConfig:
    @staticmethod
    def get_fake_ua_firefox() -> str:
        ua = UserAgent(browsers="Firefox", os="Windows")
        return ua.random
