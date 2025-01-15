import json
from typing import Any
from fake_useragent import UserAgent
from pydantic import ValidationError
from facebook.schemas import JSONFBWebdriverConfig
from facebook.exceptions import FBWebdriverInvalidConfigProvided

JSON_CONFIG: str = "../config.json"


class ProxyConfig:
    @staticmethod
    def get_proxy_config(proxy_url: str) -> dict[str, dict[str, str | None]]:
        return {
            "proxy": {
                "http": proxy_url,
                "https": proxy_url,
                "no_proxy": "localhost,ENDPOINT",
            }
        }


class FakeUserAgentConfig:
    @staticmethod
    def get_fake_ua_firefox() -> str:
        ua = UserAgent(browsers="Firefox", os="Windows")
        return ua.random


class GetJSONConfig:
    @staticmethod
    def get_json_config() -> dict[str, str]:
        content: dict[Any, Any]
        with open(JSON_CONFIG, "r") as json_file:
            content = json.load(json_file)

        try:
            JSONFBWebdriverConfig.model_validate(content)
            return content
        except ValidationError as v_e:
            raise FBWebdriverInvalidConfigProvided(v_e)
