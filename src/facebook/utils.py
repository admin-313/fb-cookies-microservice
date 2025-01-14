class CookieStringParser:
    @staticmethod
    def parse_cookie_string(cookie_str: str) -> dict[str, str]:
        pairs: list[str] = cookie_str.split(';')
        cookie_dict: dict[str, str] = {}
        
        for pair in pairs:
            key, value = pair.strip().split('=', 1)
            cookie_dict[key] = value

        return cookie_dict