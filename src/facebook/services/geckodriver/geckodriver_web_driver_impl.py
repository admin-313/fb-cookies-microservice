from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from facebook.services.service import FBWebDriver
from facebook.config import FakeUserAgentConfig, ProxyConfig


class GeckodriverWebDriverImpl(FBWebDriver):
    _firefox_driver: webdriver.Firefox

    def run_facebook_parser(self) -> str:
        try:
            options: webdriver.FirefoxOptions = self.get_options()
            self._firefox_driver = webdriver.Firefox(options=options)
            self._firefox_driver.get("https://am.i.mullvad.net/")
        finally:
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
        return FakeUserAgentConfig.get_fake_ua()

    def get_proxy_config(self) -> Proxy:
        proxy_link: str = ProxyConfig.get_proxy_link()
        proxy_config: Proxy = Proxy(
            {"proxyType": ProxyType.MANUAL, "socksProxy": proxy_link}  # type: ignore
        )

        return proxy_config
