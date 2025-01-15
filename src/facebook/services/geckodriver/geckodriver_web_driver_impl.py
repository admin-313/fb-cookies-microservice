import asyncio
from seleniumwire import webdriver  # type: ignore
from facebook.services.fb_web_driver import FBWebDriver
from facebook.exceptions import (
    FBWebdriverCouldNotParseToken,
    FBWebdriverHasNotBeenInstanciatedException,
)
from facebook.config import FakeUserAgentConfig, GetJSONConfig, ProxyConfig
from facebook.utils import CookieStringParser


class GeckodriverFBWebDriverImpl(FBWebDriver):
    _firefox_driver: webdriver.Firefox | None = None
    _json_config: dict[str, str] | None = None

    async def run_facebook_parser(self) -> str:
        parsed_result: list[str] | None = None

        try:
            self._load_json_config()

            options: dict[
                str, webdriver.FirefoxOptions | dict[str, dict[str, str | None] | bool]
            ] = self.get_webdriver_options()
            self._firefox_driver = webdriver.Firefox(**options)

            self._firefox_driver.get("https://api.ipify.org?format=json")
            self._set_cookies_from_config()
            await asyncio.sleep(6)

        finally:
            if self._firefox_driver:
                self._firefox_driver.quit()
        if parsed_result:
            return parsed_result
        else:
            raise FBWebdriverCouldNotParseToken("Could not parse the token!")

    def get_webdriver_options(
        self,
    ) -> dict[str, webdriver.FirefoxOptions | dict[str, dict[str, str | None] | bool]]:
        return {
            "seleniumwire_options": self._get_seleniumwire_options(),
            "options": self._get_selenium_options(),
        }

    def parse_token_from_html(self, html: str) -> str:
        return super().parse_token_from_html(html)

    def _load_json_config(self) -> dict[str, str]:
        self._json_config = GetJSONConfig.get_json_config()
        return self._json_config

    def _get_selenium_options(self) -> webdriver.FirefoxOptions:
        user_agent: str = self._get_user_agent()

        gecko_options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
        gecko_options.set_preference(
            name="general.useragent.override", value=user_agent
        )
        gecko_options.accept_insecure_certs = True
        gecko_options.set_preference("security.tls.version.min", 1)
        gecko_options.set_preference("security.tls.version.max", 4)
        gecko_options.set_preference("network.security.ports.banned.override", "443")

        return gecko_options

    def _get_cookies(self) -> dict[str, str]:
        if self._json_config:
            cookie_str: str = self._json_config["cookie"]
            cookies_list: dict[str, str] = CookieStringParser.parse_cookie_string(
                cookie_str=cookie_str
            )

            return cookies_list
        else:
            return {}

    def _set_cookies_from_config(self) -> None:
        if not self._firefox_driver:
            raise FBWebdriverHasNotBeenInstanciatedException(
                "Can't set cookies for an unexistent driver"
            )
        else:
            cookies: dict[str, str] = self._get_cookies()
            if cookies:
                for k, v in cookies:
                    # I ignore pylance here because selenium wire did not provide type hints to this method.
                    # It is supposed to only accept str values tho so method is not expected to fail here.
                    self._firefox_driver.add_cookie({"name": k, "value": v})  # type: ignore

    def _get_seleniumwire_options(self) -> dict[str, dict[str, str | None] | bool]:
        proxy_options = self._get_socks5_proxy_config()
        ssl_options = {
            "verify_ssl": False,
            "suppress_connection_errors": True,
            "accept_untrusted_certs ": True,
        }

        return proxy_options | ssl_options

    def _get_user_agent(self, is_random: bool = False) -> str:
        """returns user agent

        Args:
            is_random (bool, optional): Is true uses random user agent. Defaults to False.

        Returns:
            str: User agent
        """
        if not is_random and self._json_config:
            return self._json_config["user_agent"]

        else:
            return FakeUserAgentConfig.get_fake_ua_firefox()

    def _get_socks5_proxy_config(self) -> dict[str, dict[str, str | None]]:
        return ProxyConfig.get_proxy_config()
