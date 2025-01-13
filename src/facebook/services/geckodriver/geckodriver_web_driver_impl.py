import asyncio
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from facebook.services.fb_web_driver import FBWebDriver
from facebook.config import FakeUserAgentConfig, ProxyConfig


class GeckodriverFBWebDriverImpl(FBWebDriver):
    _firefox_driver: webdriver.Firefox

    async def run_facebook_parser(self) -> str:
        try:
            options: webdriver.FirefoxOptions = self.get_options()
            self._firefox_driver = webdriver.Firefox(options=options)
            self._firefox_driver.get("https://am.i.mullvad.net/")
            await asyncio.sleep(60)
        finally:
            if self._firefox_driver:
                self._firefox_driver.quit()

        return ""

    def get_options(self) -> webdriver.FirefoxOptions:
        proxy_config: Proxy = self.get_proxy_config()
        user_agent: str = self.get_user_agent()

        gecko_options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
        gecko_options.proxy = proxy_config
        gecko_options.set_preference(
            name="general.useragent.override", value=user_agent
        )

        return gecko_options

    def get_user_agent(self) -> str:
        return FakeUserAgentConfig.get_fake_ua_firefox()

    def get_proxy_config(self) -> Proxy:
        # I'm writing this comment here to tell future developer who stumbles upon this that
        # Neither Chromium nor Geckodriver support SOCKSv5 Private(auth) proxies.
        # We mad because of this yet we have no other options but to use https at this point.
        # For some reason browser engines devs don't want to implements this
        # since on the github of those projects it's already been a while since the
        # pull requests with private socksv5 additions have been proposed.
        # I kindly ask you to keep this comment here so noone will spend hours of
        # his time figuring out how to migrate to socksv5 from http. Thank you for
        # paying your attention to this project and have a great rest of your day
        proxy_link: str = ProxyConfig.get_proxy_link()
        proxy_config: Proxy = Proxy(
            {"proxyType": ProxyType.MANUAL, "httpProxy": proxy_link}  # type: ignore
        )

        return proxy_config
