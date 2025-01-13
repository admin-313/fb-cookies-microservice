import asyncio
from facebook.services.fb_web_driver import FBWebDriver
from facebook.config import FakeUserAgentConfig, ProxyConfig
from seleniumwire import webdriver  # type: ignore


class GeckodriverFBWebDriverImpl(FBWebDriver):
    _firefox_driver: webdriver.Firefox | None = None

    async def run_facebook_parser(self) -> str:
        try:
            options_selenium: webdriver.FirefoxOptions = self.get_selenium_options()
            options_seleniumwire: dict[str, dict[str, str | None]] = (
                self.get_seleniumwire_options()
            )
            self._firefox_driver = webdriver.Firefox(
                seleniumwire_options=options_seleniumwire, options=options_selenium
            )
            self._firefox_driver.get("https://api.ipify.org?format=json")
            await asyncio.sleep(60)
        except Exception as e:
            print(e)
        finally:
            if self._firefox_driver:
                self._firefox_driver.quit()

        return ""

    def get_selenium_options(self) -> webdriver.FirefoxOptions:
        user_agent: str = self.get_random_user_agent()

        gecko_options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
        gecko_options.set_preference(
            name="general.useragent.override", value=user_agent
        )

        return gecko_options

    def get_seleniumwire_options(self) -> dict[str, dict[str, str | None]]:
        return self.get_socks5_proxy_config()

    def get_random_user_agent(self) -> str:
        return FakeUserAgentConfig.get_fake_ua_firefox()
    
    def get_socks5_proxy_config(self) -> dict[str, dict[str, str | None]]:
        return ProxyConfig.get_socks5_proxy_config()