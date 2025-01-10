from fake_useragent import UserAgent

class FakeUserAgent:
    @staticmethod
    def get_fake_ua() -> str:
        ua = UserAgent(browsers="Firefox", os="Windows")
        return ua.random