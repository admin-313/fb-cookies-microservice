import asyncio
import os
from facebook.services.fb_web_driver import FBWebDriver
from facebook.config import FakeUserAgentConfig
from seleniumwire import webdriver  # type: ignore


class GeckodriverFBWebDriverImpl(FBWebDriver):
    _firefox_driver: webdriver.Firefox

    async def run_facebook_parser(self) -> str:
        try:
            options: webdriver.FirefoxOptions = self.get_options()
            self._firefox_driver = webdriver.Firefox(seleniumwire_options=options)
            self._firefox_driver.get("https://am.i.mullvad.net/")
            await asyncio.sleep(60)
        finally:
            if self._firefox_driver:
                self._firefox_driver.quit()

        return ""

    def get_options(self) -> webdriver.FirefoxOptions:
        proxy_config: dict[str, dict[str, str | None]] = self.get_socks5_proxy_config()
        user_agent: str = self.get_user_agent()

        gecko_options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
        gecko_options.proxy = proxy_config
        gecko_options.set_preference(
            name="general.useragent.override", value=user_agent
        )

        return gecko_options

    def get_user_agent(self) -> str:
        return FakeUserAgentConfig.get_fake_ua_firefox()

    def get_socks5_proxy_config(self) -> dict[str, dict[str, str | None]]:
        socks_proxy: str | None= os.getenv("PROXY_URL")
        return {
            "proxy": {
                "http": socks_proxy,
                "https": socks_proxy,
                "no_proxy": "localhost,ENDPOINT",
            }
        }
