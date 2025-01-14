import asyncio
from seleniumwire import webdriver  # type: ignore
from facebook.services.fb_web_driver import FBWebDriver
from facebook.exceptions import FBWebdriverCouldNotParseToken
from facebook.config import FakeUserAgentConfig, ProxyConfig


class GeckodriverFBWebDriverImpl(FBWebDriver):
    _firefox_driver: webdriver.Firefox | None = None

    async def run_facebook_parser(self) -> str:
        parsed_result: list[str] | None = None

        try:
            options: dict[
                str, webdriver.FirefoxOptions | dict[str, dict[str, str | None] | bool]
            ] = self._get_all_options()
            self._firefox_driver = webdriver.Firefox(**options)
            self._firefox_driver.get("https://api.ipify.org?format=json")
            await asyncio.sleep(6)

        finally:
            if self._firefox_driver:
                self._firefox_driver.quit()
        if parsed_result:
            return parsed_result
        else:
            raise FBWebdriverCouldNotParseToken("Could not parse the token!")

    def _get_all_options(
        self,
    ) -> dict[str, webdriver.FirefoxOptions | dict[str, dict[str, str | None] | bool]]:
        return {
            "seleniumwire_options": self._get_seleniumwire_options(),
            "options": self._get_selenium_options(),
        }

    def _get_selenium_options(self) -> webdriver.FirefoxOptions:
        user_agent: str = self._get_random_user_agent()

        gecko_options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
        gecko_options.set_preference(
            name="general.useragent.override", value=user_agent
        )
        gecko_options.accept_insecure_certs = True
        gecko_options.set_preference("security.tls.version.min", 1)
        gecko_options.set_preference("security.tls.version.max", 4)
        gecko_options.set_preference("network.security.ports.banned.override", "443")

        return gecko_options

    def _get_seleniumwire_options(self) -> dict[str, dict[str, str | None] | bool]:
        proxy_options = self._get_socks5_proxy_config()
        ssl_options = {
            "verify_ssl": False,
            "suppress_connection_errors": True,
            "accept_untrusted_certs ": True,
        }

        return proxy_options | ssl_options

    def _get_random_user_agent(self) -> str:
        return FakeUserAgentConfig.get_fake_ua_firefox()

    def _get_socks5_proxy_config(self) -> dict[str, dict[str, str | None]]:
        return ProxyConfig.get_socks5_proxy_config()
