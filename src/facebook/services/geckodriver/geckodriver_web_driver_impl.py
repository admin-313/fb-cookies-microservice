import asyncio
import re
from pydantic import ValidationError
from seleniumwire import webdriver  # type: ignore
from facebook.services.fb_web_driver import FBWebDriver
from facebook.config import FakeUserAgentConfig, GetJSONConfig, ProxyConfig
from facebook.utils import CookieStringParser
from facebook.schemas import JSONFBWebdriverConfig, ParserResponce
from facebook.exceptions import (
    FBWebdriverHasNotBeenInstanciated,
    Socks5ProxyParseFail,
    FBDriverJSParseException,
)

class GeckodriverFBWebDriverImpl(FBWebDriver):
    _firefox_driver: webdriver.Firefox | None = None
    _parsed_result: ParserResponce | None = None
    _json_config: JSONFBWebdriverConfig

    async def run_facebook_parser(self) -> ParserResponce:
        try:
            result: dict[str, str] = {}
            self._load_json_config()
            options: dict[
                str, webdriver.FirefoxOptions | dict[str, dict[str, str | None] | bool]
            ] = self.get_webdriver_options()
            # Connects to proxy and sets ua
            self._firefox_driver = webdriver.Firefox(**options)
            self._firefox_driver.get("https://facebook.com")
            self._set_cookies_from_config()

            self._firefox_driver.get(self._json_config.adsmanager_link)
            html: str = self._firefox_driver.page_source
            cookies: list[dict[str, str]] = self._firefox_driver.get_cookies() # type: ignore
            
            result["access_token"] = self.get_accesstoken(html)
            result["cookie"] = self.get_cookie(cookies)

            return ParserResponce.model_validate(result)

        except ValidationError as ve:
            raise FBDriverJSParseException(
                f"Could not validate obtained data via JS parsing {str(ve)}"
            )

        finally:
            if self._firefox_driver:
                await asyncio.sleep(2)
                self._firefox_driver.quit()

    def get_webdriver_options(
        self,
    ) -> dict[str, webdriver.FirefoxOptions | dict[str, dict[str, str | None] | bool]]:
        return {
            "seleniumwire_options": self._get_seleniumwire_options(),
            "options": self._get_selenium_options(),
        }

    def get_accesstoken(self, page_source: str) -> str:
        if not self._firefox_driver:
            raise FBWebdriverHasNotBeenInstanciated("Driver not initialized")
        
        regexp_pattern = r'window\.__accessToken="([^"]+)"'
        match = re.search(regexp_pattern, page_source)
        
        if not match:
            raise FBDriverJSParseException("Access token not found in page source")
            
        return match.group(1)

    def get_cookie(self, cookies: list[dict[str, str]]) -> str:
        if self._firefox_driver:

            return ";".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        else:
            raise FBWebdriverHasNotBeenInstanciated(
                "Can't parse access token via an unexistent driver"
            )

    def _load_json_config(self) -> JSONFBWebdriverConfig:
        self._json_config = GetJSONConfig.get_json_config()
        return self._json_config

    def _get_selenium_options(self) -> webdriver.FirefoxOptions:
        user_agent: str = self._get_user_agent()

        gecko_options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
        gecko_options.set_preference(
            name="general.useragent.override", value=user_agent
        )

        gecko_options.accept_insecure_certs = True
        gecko_options.page_load_strategy = "eager"
        gecko_options.set_preference("security.tls.version.min", 1)
        gecko_options.set_preference("security.tls.version.max", 4)
        gecko_options.set_preference("network.security.ports.banned.override", "443")
        gecko_options.set_preference("network.http.referer.defaultPolicy", 2)
    
        return gecko_options

    def _get_cookies(self) -> dict[str, str]:
        if self._json_config:
            cookie_str: str = self._json_config.cookie
            cookies_list: dict[str, str] = CookieStringParser.parse_cookie_string(
                cookie_str=cookie_str
            )

            return cookies_list
        else:
            return {}

    def _set_cookies_from_config(self) -> None:
        if not self._firefox_driver:
            raise FBWebdriverHasNotBeenInstanciated(
                "Can't set cookies for an unexistent driver"
            )
        else:
            cookies: dict[str, str] = self._get_cookies()
            if cookies:
                for k, v in cookies.items():
                    # I ignore pylance here because selenium wire did not provide type hints to this method.
                    # It is supposed to only accept str values tho so method is not expected to fail here.
                    self._firefox_driver.add_cookie({"name": k, "value": v, "domain": ".facebook.com", "secure": True, "path": "/"})  # type: ignore

    def _get_seleniumwire_options(self) -> dict[str, dict[str, str | None] | bool]:
        proxy_options = self._get_socks5_proxy_config()
        ssl_options = {
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
            return self._json_config.user_agent

        else:
            return FakeUserAgentConfig.get_fake_ua_firefox()

    def _get_socks5_proxy_config(self) -> dict[str, dict[str, str | None]]:
        if self._json_config:
            return ProxyConfig.get_proxy_config(proxy_url=self._json_config.proxy)

        else:
            raise Socks5ProxyParseFail("No proxy config was provided")
