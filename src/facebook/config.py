from dotenv import load_dotenv
import os

load_dotenv()


def get_proxy_link() -> str:
    proxy_ulr: str | None = os.getenv("PROXY_URL")
    if proxy_ulr:
        return proxy_ulr
    else:
        raise ValueError("The proxy value can't be empty!")
