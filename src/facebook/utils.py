class CookieStringParser:
    @staticmethod
    def parse_cookie_string(cookie_str: str) -> dict[str, str]:
        pairs: list[str] = cookie_str.split(";")
        cookie_dict: dict[str, str] = {}

        for pair in pairs:
            splitted_pair: list[str] | None = pair.split("=") if "=" in pair else None
            if splitted_pair and len(splitted_pair) == 2:
                cookie_dict[splitted_pair[0]] = splitted_pair[1]

        return cookie_dict
