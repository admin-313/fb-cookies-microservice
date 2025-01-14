import asyncio
from facebook.services.fb_web_driver import FBWebDriver
from facebook.exceptions import FBWebdriverHasNotBeenInstanciatedException
from facebook.config import FakeUserAgentConfig, ProxyConfig
from seleniumwire import webdriver  # type: ignore


class GeckodriverFBWebDriverImpl(FBWebDriver):
    _firefox_driver: webdriver.Firefox | None = None

    async def run_facebook_parser(self) -> str:
        try:
            self._set_options()

            if isinstance(self._firefox_driver, webdriver.Firefox):
                self._firefox_driver.get("https://api.ipify.org?format=json")
                await asyncio.sleep(6)
            else:
                raise FBWebdriverHasNotBeenInstanciatedException(
                    "The driver failed to be instanciated"
                )

        finally:
            if self._firefox_driver:
                self._firefox_driver.quit()

        return ""

    def _set_options(self) -> None:
        options_selenium: webdriver.FirefoxOptions = self.get_selenium_options()
        options_seleniumwire: dict[str, dict[str, str | None] | bool] = (
            self.get_seleniumwire_options()
        )
        self._firefox_driver = webdriver.Firefox(
            seleniumwire_options=options_seleniumwire, options=options_selenium
        )

    def get_selenium_options(self) -> webdriver.FirefoxOptions:
        user_agent: str = self.get_random_user_agent()

        gecko_options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
        gecko_options.set_preference(
            name="general.useragent.override", value=user_agent
        )
        gecko_options.accept_insecure_certs = True
        gecko_options.set_preference("security.tls.version.min", 1)
        gecko_options.set_preference("security.tls.version.max", 4)
        gecko_options.set_preference("network.security.ports.banned.override", "443")

        return gecko_options

    def get_seleniumwire_options(self) -> dict[str, dict[str, str | None] | bool]:
        proxy_options = self.get_socks5_proxy_config()
        ssl_options = {
            "verify_ssl": False,
            "suppress_connection_errors": True,
            "accept_untrusted_certs ": True,
        }

        return proxy_options | ssl_options

    def get_random_user_agent(self) -> str:
        return FakeUserAgentConfig.get_fake_ua_firefox()

    def get_socks5_proxy_config(self) -> dict[str, dict[str, str | None]]:
        return ProxyConfig.get_socks5_proxy_config()
